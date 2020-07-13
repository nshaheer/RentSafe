package com.leaseguard.leaseguard.landing

import android.os.Bundle
import android.view.View
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
        floatingActionMenu.addItem("Google Drive", R.drawable.ic_folder,
                View.OnClickListener {
                    // TODO: open drive
                })
        floatingActionMenu.addItem("PDF", R.drawable.ic_pdf,
                View.OnClickListener {
                    // TODO: open pdf
                })
        floatingActionMenu.addItem("Library", R.drawable.ic_lib,
                View.OnClickListener {
                    // TODO: open library
                })
        floatingActionMenu.addItem("Photo", R.drawable.ic_camera,
                View.OnClickListener {
                    // TODO: open camera
                })
    }

    override fun getViewModel(): SafeRentActivityViewModel {
        return safeRentViewModel
    }
}