package com.leaseguard.leaseguard.landing

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.leaseguard.leaseguard.R
import com.simplify.ink.InkView

class SignLeaseActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sign_lease)

        supportActionBar?.title = "Sign Lease"
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        val ink = findViewById(R.id.ink) as InkView
        ink.setColor(resources.getColor(android.R.color.black))
        ink.setMinStrokeWidth(1.5f)
        ink.setMaxStrokeWidth(6f)
    }
}