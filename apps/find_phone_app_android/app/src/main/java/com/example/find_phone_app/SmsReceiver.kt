package com.example.find_phone_app

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.util.Log
import androidx.core.content.ContextCompat

class SmsReceiver : BroadcastReceiver() {
    private val TAG = "SmsReceiver"

    override fun onReceive(context: Context, intent: Intent) {
        if (Telephony.Sms.Intents.SMS_RECEIVED_ACTION != intent.action) return
        val msgs = Telephony.Sms.Intents.getMessagesFromIntent(intent)
        val body = msgs.joinToString(" ") { it.messageBody ?: "" }
        val trig = Prefs.phrase(context)
        val stop = Prefs.stopPhrase(context)

        Log.i(TAG, "SMS: ${body.take(120)}")
        when {
            body.contains(stop, true) ->
                ContextCompat.startForegroundService(context, Intent(context, RingService::class.java).apply { action = RingService.ACTION_STOP })
            body.contains(trig, true) ->
                ContextCompat.startForegroundService(context, Intent(context, RingService::class.java))
        }
    }
}
