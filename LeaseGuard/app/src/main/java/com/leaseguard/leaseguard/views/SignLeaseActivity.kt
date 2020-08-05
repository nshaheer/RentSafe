package com.leaseguard.leaseguard.views

import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import com.leaseguard.leaseguard.R
import com.simplify.ink.InkView
import dagger.android.support.DaggerAppCompatActivity

/**
 * Simple implementation of signature drawing feature.
 * Use [InkView] to let user paint signature on to the screen.
 */
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

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_sign_lease, menu)
        return super.onCreateOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        return when (item?.itemId) {
            android.R.id.home -> {
                setResult(DaggerAppCompatActivity.RESULT_OK)
                finish()
                return true
            }
            R.id.action_sign -> {
                setResult(DaggerAppCompatActivity.RESULT_OK)
                finish()
                return true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}