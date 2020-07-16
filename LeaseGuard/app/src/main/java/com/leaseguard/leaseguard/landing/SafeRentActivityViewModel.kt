package com.leaseguard.leaseguard.landing

import android.net.Uri
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import javax.inject.Inject

class SafeRentActivityViewModel @Inject constructor() : ViewModel() {
    var startAnalyzeDocActivity: MutableLiveData<Int> = MutableLiveData()
    fun onFileSelected(file : Uri?) {
        // TODO: save file to data layer (injected repository)
        // start analyze activity
        startAnalyzeDocActivity.postValue(0)
    }
}