package com.leaseguard.leaseguard.landing

import android.net.Uri
import androidx.lifecycle.ViewModel
import javax.inject.Inject

class SafeRentActivityViewModel @Inject constructor() : ViewModel() {
    fun onFileSelected(file : Uri?) {
        // TODO: send to server
    }
}