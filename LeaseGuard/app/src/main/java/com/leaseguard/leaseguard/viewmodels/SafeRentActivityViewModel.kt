package com.leaseguard.leaseguard.viewmodels

import android.net.Uri
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.repositories.DocumentRepository
import javax.inject.Inject

/**
 * ViewModel for [SafeRentActivity].
 */
class SafeRentActivityViewModel @Inject constructor(private val documentRepository: DocumentRepository) : ViewModel() {
    var startAnalyzeDocActivity: MutableLiveData<Int> = MutableLiveData()
    var documentUpdated: LiveData<List<LeaseDocument>> = documentRepository.getDocuments()
    fun onFileSelected(file : Uri?) {
        // start analyze activity
        documentRepository.setPdfUri(file)
        startAnalyzeDocActivity.postValue(0)
    }
}