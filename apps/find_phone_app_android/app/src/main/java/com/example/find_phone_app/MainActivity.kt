package com.example.find_phone_app

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    private lateinit var textView: TextView
    private lateinit var startBtn: Button
    private lateinit var stopBtn: Button
    private lateinit var chooseButton: Button
    private lateinit var settingsBtn: Button

    private val REQ_PERMS = 100

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        textView = findViewById(R.id.textViewResult)
        startBtn = findViewById(R.id.buttonListen)
        stopBtn = findViewById(R.id.buttonStop)
        chooseButton = findViewById(R.id.buttonChooseRingtone)
        settingsBtn = findViewById(R.id.buttonSettings)

        textView.text = "Ready phrase: ${Prefs.phrase(this)}"
        requestNeededPermissions()

        startBtn.setOnClickListener {
            val i = Intent(this, RingService::class.java)
            ContextCompat.startForegroundService(this, i)
            Toast.makeText(this, "Ring started.", Toast.LENGTH_SHORT).show()
        }

        stopBtn.setOnClickListener {
            val stopIntent = Intent(this, RingService::class.java).apply { action = RingService.ACTION_STOP }
            startService(stopIntent)
            stopService(Intent(this, RingService::class.java))
            Toast.makeText(this, "Ring stopped.", Toast.LENGTH_SHORT).show()
        }

        // Open Settings (also handles ringtone)
        chooseButton.setOnClickListener { startActivity(Intent(this, SettingsActivity::class.java)) }
        settingsBtn.setOnClickListener { startActivity(Intent(this, SettingsActivity::class.java)) }
    }

    override fun onResume() {
        super.onResume()
        // Refresh UI after returning from Settings
        textView.text = "Ready phrase: ${Prefs.phrase(this)}"
    }

    private fun requestNeededPermissions() {
        val req = mutableListOf<String>()
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECEIVE_SMS) != PackageManager.PERMISSION_GRANTED)
            req += Manifest.permission.RECEIVE_SMS
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_SMS) != PackageManager.PERMISSION_GRANTED)
            req += Manifest.permission.READ_SMS
        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED)
            req += Manifest.permission.POST_NOTIFICATIONS
        if (req.isNotEmpty()) ActivityCompat.requestPermissions(this, req.toTypedArray(), REQ_PERMS)
    }
}
