package com.example.find_phone_app

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.content.pm.PackageManager
import android.media.*
import android.net.Uri
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.PowerManager
import android.view.KeyEvent
import androidx.core.app.NotificationCompat

class RingService : Service() {

    companion object { const val ACTION_STOP = "com.example.find_phone_app.STOP" }

    private var player: MediaPlayer? = null
    private var fallback: Ringtone? = null
    private var wake: PowerManager.WakeLock? = null
    private var am: AudioManager? = null
    private var focusReq: AudioFocusRequest? = null
    private val stopMs = 5 * 60 * 1000L
    private val handler by lazy { Handler(mainLooper) }
    private val stopRunnable = Runnable { stopSelf() }

    override fun onCreate() {
        super.onCreate()
        (getSystemService(NOTIFICATION_SERVICE) as NotificationManager).createNotificationChannel(
            NotificationChannel("ring", "Find Phone Ring", NotificationManager.IMPORTANCE_HIGH)
        )
        wake = (getSystemService(POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "findphone:ring").apply {
                setReferenceCounted(false); acquire(stopMs)
            }
        am = getSystemService(AUDIO_SERVICE) as AudioManager
    }

    private fun isPlaying(): Boolean = (player?.isPlaying == true) || (fallback != null)

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            stopEverything()
            stopSelf()
            return START_NOT_STICKY
        }
        if (isPlaying()) return START_NOT_STICKY

        val stopPi = PendingIntent.getService(
            this, 1, Intent(this, RingService::class.java).apply { action = ACTION_STOP },
            PendingIntent.FLAG_UPDATE_CURRENT or (if (Build.VERSION.SDK_INT >= 23) PendingIntent.FLAG_IMMUTABLE else 0)
        )
        val notif = NotificationCompat.Builder(this, "ring")
            .setSmallIcon(android.R.drawable.ic_lock_idle_alarm)
            .setContentTitle("Find Phone")
            .setContentText("Ringing…")
            .setOngoing(true)
            .addAction(0, "STOP", stopPi)
            .build()
        startForeground(42, notif)

        // Max volumes
        runCatching {
            am?.setStreamVolume(AudioManager.STREAM_MUSIC, am!!.getStreamMaxVolume(AudioManager.STREAM_MUSIC), 0)
            am?.setStreamVolume(AudioManager.STREAM_ALARM, am!!.getStreamMaxVolume(AudioManager.STREAM_ALARM), 0)
        }

        // Audio focus
        if (Build.VERSION.SDK_INT >= 26) {
            focusReq = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN)
                .setAudioAttributes(
                    AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_ALARM)
                        .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                        .build()
                ).build()
            am?.requestAudioFocus(focusReq!!)
        } else {
            @Suppress("DEPRECATION")
            am?.requestAudioFocus(null, AudioManager.STREAM_MUSIC, AudioManager.AUDIOFOCUS_GAIN)
        }

        val uri = Prefs.ringUri(this) ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
        val usedVlc = Prefs.useVlc(this) && tryStartVlc(uri)

        if (!usedVlc) {
            if (!startFromUri(uri)) startFallback(uri)
        }

        handler.removeCallbacks(stopRunnable)
        handler.postDelayed(stopRunnable, stopMs)
        return START_NOT_STICKY
    }

    private fun tryStartVlc(uri: Uri): Boolean {
        val pm: PackageManager = packageManager
        val hasVlc = runCatching { pm.getPackageInfo("org.videolan.vlc", 0); true }.getOrDefault(false)
        if (!hasVlc) return false

        val i = Intent(Intent.ACTION_VIEW).apply {
            setPackage("org.videolan.vlc")
            setDataAndType(uri, "audio/*")
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        return runCatching { startActivity(i); true }.getOrDefault(false)
    }

    private fun startFromUri(uri: Uri): Boolean = try {
        val p = MediaPlayer().apply {
            setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            isLooping = true
            setDataSource(this@RingService, uri)
            setOnErrorListener { _, _, _ -> stopSelf(); true }
            prepare()
            start()
        }
        player = p
        true
    } catch (_: Throwable) { false }

    private fun startFallback(uri: Uri) {
        val r = RingtoneManager.getRingtone(this, uri)
            ?: RingtoneManager.getRingtone(this, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM))
        r?.let {
            it.audioAttributes = AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_ALARM)
                .build()
            it.play()
            fallback = it
        }
    }

    private fun stopEverything() {
        handler.removeCallbacks(stopRunnable)

        runCatching { player?.stop(); player?.release() }; player = null
        runCatching { fallback?.stop() }; fallback = null

        if (Build.VERSION.SDK_INT >= 26) focusReq?.let { am?.abandonAudioFocusRequest(it) }
        else @Suppress("DEPRECATION") am?.abandonAudioFocus(null)

        // Stop external players too
        val downS = KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_MEDIA_STOP)
        val upS   = KeyEvent(KeyEvent.ACTION_UP,   KeyEvent.KEYCODE_MEDIA_STOP)
        runCatching { am?.dispatchMediaKeyEvent(downS); am?.dispatchMediaKeyEvent(upS) }
        val downP = KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_MEDIA_PAUSE)
        val upP   = KeyEvent(KeyEvent.ACTION_UP,   KeyEvent.KEYCODE_MEDIA_PAUSE)
        runCatching { am?.dispatchMediaKeyEvent(downP); am?.dispatchMediaKeyEvent(upP) }
    }

    override fun onDestroy() {
        stopEverything()
        if (wake?.isHeld == true) wake?.release()
        stopForeground(true)
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
