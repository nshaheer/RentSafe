package com.leaseguard.leaseguard.landing

import android.content.Intent
import android.os.Bundle
import android.view.View
import com.leaseguard.leaseguard.BaseActivity
import com.leaseguard.leaseguard.R
import kotlinx.android.synthetic.main.activity_saferent.*
import javax.inject.Inject

class SafeRentActivity : BaseActivity<SafeRentActivityViewModel>() {
    private val LIBRARY_CODE = 1

    @Inject
    lateinit var safeRentViewModel : SafeRentActivityViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_saferent)
        
        floatingActionMenu.addItem("Library", R.drawable.ic_lib,
                View.OnClickListener {
                    val intent = Intent()
                            .setType("*/*")
                            .setAction(Intent.ACTION_GET_CONTENT)
                    startActivityForResult(Intent.createChooser(intent, "Select a file"), LIBRARY_CODE)
                })
        floatingActionMenu.addItem("Photo", R.drawable.ic_camera,
                View.OnClickListener {
                    // TODO: open camera
                })
    }

    override fun getViewModel(): SafeRentActivityViewModel {
        return safeRentViewModel
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == LIBRARY_CODE && resultCode == RESULT_OK) {
            val resultFile = data?.data
            safeRentViewModel.onFileSelected(resultFile)
        }
    }
}