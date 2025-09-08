package com.example.find_phone_app

import android.content.Intent
import android.media.RingtoneManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity

class SettingsActivity : AppCompatActivity() {

    private lateinit var etPhrase: EditText
    private lateinit var etStop: EditText
    private lateinit var swVlc: Switch
    private lateinit var btnPick: Button
    private lateinit var btnSave: Button

    private val REQ_RING = 301

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        etPhrase = findViewById(R.id.etPhrase)
        etStop   = findViewById(R.id.etStopPhrase)
        swVlc    = findViewById(R.id.swUseVlc)
        btnPick  = findViewById(R.id.btnPickRingtone)
        btnSave  = findViewById(R.id.btnSave)

        etPhrase.setText(Prefs.phrase(this))
        etStop.setText(Prefs.stopPhrase(this))
        swVlc.isChecked = Prefs.useVlc(this)

        btnPick.setOnClickListener {
            val i = Intent(RingtoneManager.ACTION_RINGTONE_PICKER).apply {
                putExtra(RingtoneManager.EXTRA_RINGTONE_TYPE, RingtoneManager.TYPE_RINGTONE)
                putExtra(RingtoneManager.EXTRA_RINGTONE_SHOW_DEFAULT, true)
                putExtra(RingtoneManager.EXTRA_RINGTONE_SHOW_SILENT, false)
                Prefs.ringUri(this@SettingsActivity)?.let {
                    putExtra(RingtoneManager.EXTRA_RINGTONE_EXISTING_URI, it)
                }
            }
            startActivityForResult(i, REQ_RING)
        }

        btnSave.setOnClickListener {
            Prefs.setPhrase(this, etPhrase.text.toString().ifBlank { "ariphonefinder123" })
            Prefs.setStopPhrase(this, etStop.text.toString().ifBlank { "aristopfinder123" })
            Prefs.setUseVlc(this, swVlc.isChecked)
            Toast.makeText(this, "Saved.", Toast.LENGTH_SHORT).show()
            finish()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == REQ_RING && resultCode == RESULT_OK) {
            val picked: Uri? = if (Build.VERSION.SDK_INT >= 33)
                data?.getParcelableExtra(RingtoneManager.EXTRA_RINGTONE_PICKED_URI, Uri::class.java)
            else @Suppress("DEPRECATION")
                data?.getParcelableExtra(RingtoneManager.EXTRA_RINGTONE_PICKED_URI)

            if (picked != null) {
                Prefs.setRingUri(this, picked)
                Toast.makeText(this, "Ringtone selected.", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "No ringtone selected.", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
