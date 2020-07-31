package com.leaseguard.leaseguard.landing

import android.net.Uri
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.leaseguard.leaseguard.api.SyncService
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.repositories.DocumentRepository
import javax.inject.Inject

class SafeRentActivityViewModel @Inject constructor(private val documentRepository: DocumentRepository) : ViewModel() {
    var startAnalyzeDocActivity: MutableLiveData<Int> = MutableLiveData()
    var documentUpdated: LiveData<List<LeaseDocument>> = documentRepository.getDocuments()
    fun onFileSelected(file : Uri?) {
        // TODO: save file to data layer (injected repository)
        // start analyze activity
        startAnalyzeDocActivity.postValue(0)
    }
}