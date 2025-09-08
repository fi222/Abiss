package com.example.find_phone_app

import android.content.Context
import android.net.Uri

object Prefs {
    private const val FILE = "cfg"
    private const val K_PHRASE = "phrase"
    private const val K_STOP = "stop_phrase"
    private const val K_RING = "ring_uri"
    private const val K_VLC  = "use_vlc"

    fun phrase(c: Context) = c.getSharedPreferences(FILE, Context.MODE_PRIVATE)
        .getString(K_PHRASE, "ariphonefinder123")!!

    fun stopPhrase(c: Context) = c.getSharedPreferences(FILE, Context.MODE_PRIVATE)
        .getString(K_STOP, "aristopfinder123")!!

    fun ringUri(c: Context): Uri? =
        c.getSharedPreferences(FILE, Context.MODE_PRIVATE).getString(K_RING, null)?.let { Uri.parse(it) }

    fun setRingUri(c: Context, u: Uri) {
        c.getSharedPreferences(FILE, Context.MODE_PRIVATE).edit().putString(K_RING, u.toString()).apply()
    }

    fun useVlc(c: Context) = c.getSharedPreferences(FILE, Context.MODE_PRIVATE).getBoolean(K_VLC, false)
    fun setUseVlc(c: Context, v: Boolean) {
        c.getSharedPreferences(FILE, Context.MODE_PRIVATE).edit().putBoolean(K_VLC, v).apply()
    }

    fun setPhrase(c: Context, v: String) {
        c.getSharedPreferences(FILE, Context.MODE_PRIVATE).edit().putString(K_PHRASE, v).apply()
    }

    fun setStopPhrase(c: Context, v: String) {
        c.getSharedPreferences(FILE, Context.MODE_PRIVATE).edit().putString(K_STOP, v).apply()
    }
}
