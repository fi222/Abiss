package com.example.find_phone_app

import android.app.Notification
import android.content.Intent
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import android.util.Log
import androidx.core.content.ContextCompat   // <- correct import

class NotifySvc : NotificationListenerService() {
    private val TAG = "NotifySvc"

    // Gmail + WhatsApp + Telegram + Signal
    private val allowedPkgs = setOf(
        "com.google.android.gm",
        "com.whatsapp",
        "com.whatsapp.w4b",
        "org.telegram.messenger",
        "org.thunderdog.challegram",
        "org.thoughtcrime.securesms"
    )

    companion object { private var lastAt = 0L; private var lastHash = 0 }

    override fun onNotificationPosted(sbn: StatusBarNotification) {
        val pkg = sbn.packageName ?: return
        if (!allowedPkgs.contains(pkg)) return

        val content = flatten(sbn)
        val trig = Prefs.phrase(this)
        val stop = Prefs.stopPhrase(this)

        if (content.contains(stop, true)) {
            Log.i(TAG, "Stop trigger matched from $pkg")
            ContextCompat.startForegroundService(
                applicationContext,
                Intent(applicationContext, RingService::class.java).apply { action = RingService.ACTION_STOP }
            )
            return
        }
        if (!content.contains(trig, true)) return

        val now = System.currentTimeMillis()
        val h = (pkg + ":" + content.take(200) + ":" + sbn.id + ":" + sbn.postTime).hashCode()
        if (now - lastAt < 8000 && h == lastHash) { Log.i(TAG, "Debounced duplicate from $pkg"); return }
        lastAt = now; lastHash = h

        Log.i(TAG, "Trigger matched from $pkg")
        ContextCompat.startForegroundService(
            applicationContext,
            Intent(applicationContext, RingService::class.java)
        )
    }

    private fun flatten(sbn: StatusBarNotification): String {
        val e = sbn.notification.extras
        val chunks = mutableListOf<String>()
        fun add(x: CharSequence?) { if (!x.isNullOrBlank()) chunks += x.toString() }
        fun addArr(a: Array<CharSequence>?) { if (a != null) for (c in a) add(c) }

        add(e.getCharSequence(Notification.EXTRA_TITLE))
        add(e.getCharSequence(Notification.EXTRA_TEXT))
        add(e.getCharSequence(Notification.EXTRA_SUB_TEXT))
        add(e.getCharSequence(Notification.EXTRA_INFO_TEXT))
        add(e.getCharSequence(Notification.EXTRA_BIG_TEXT))
        @Suppress("UNCHECKED_CAST")
        addArr(e.getCharSequenceArray(Notification.EXTRA_TEXT_LINES) as? Array<CharSequence>)
        val linesAny = e.get("android.textLines")
        if (linesAny is Array<*>) for (c in linesAny) add(c as? CharSequence)

        return chunks.joinToString("\n")
    }
}
