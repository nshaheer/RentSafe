package com.leaseguard.leaseguard.landing

import android.content.DialogInterface
import android.util.Log
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import javax.inject.Inject

class AnalyzeDocActivityViewModel @Inject constructor() : ViewModel() {
    var isLoading: MutableLiveData<Boolean> = MutableLiveData()
    var endActivity: MutableLiveData<Int> = MutableLiveData()
    var warningText: MutableLiveData<List<String>> = MutableLiveData()

    fun doAnalysis() {
        Log.d("sang", "i am doing analysis")
        isLoading.postValue(true)
        // TODO: Make an API call
        val thread = Thread(Runnable {
            Thread.sleep(2000)
            isLoading.postValue(false)
            warningText.postValue(listOf("Rent deposit more than single month rent", "Pets prohibited"))
        })
        thread.start()
    }

    fun cancelAnalysis(dialogInterface: DialogInterface) {
        endActivity.postValue(0)
    }
}