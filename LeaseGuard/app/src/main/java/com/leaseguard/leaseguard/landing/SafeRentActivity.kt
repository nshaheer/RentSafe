package com.leaseguard.leaseguard.landing

import android.os.Bundle
import com.leaseguard.leaseguard.BaseActivity
import com.leaseguard.leaseguard.R
import kotlinx.android.synthetic.main.activity_saferent.*
import javax.inject.Inject

class SafeRentActivity : BaseActivity<SafeRentActivityViewModel>() {

    @Inject
    lateinit var safeRentViewModel : SafeRentActivityViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_saferent)
        pdfButton.setOnClickListener {

        }
    }

    override fun getViewModel(): SafeRentActivityViewModel {
        return safeRentViewModel
    }
}