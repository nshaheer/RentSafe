package com.leaseguard.leaseguard.landing

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.models.RentIssue
import com.leaseguard.leaseguard.repositories.DocumentRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import javax.inject.Inject

class AnalyzeDocActivityViewModel @Inject constructor(private val documentRepository: DocumentRepository) : ViewModel() {
    val rentIsSafe = false
    val dummyDocument = LeaseDocument(0,"Luxe Waterloo", "333 King Street N", 600, "May 1, 2017 - Aug 31, 2017", 2)
    val dummyIssues = listOf(
            RentIssue(
                    "Rent deposit more than single month rent",
                    "Rent Deposits",
                    "Landlords are only legally allowed to ask for a rent deposit equal to a single month rent"
            ),
            RentIssue(
                    "Pets prohibited",
                    "Pet Policies",
                    "Landlords are only able to prohibit pets if they cause significant property damage"
            )
    )

    var notifyAnalysisComplete = MutableLiveData<Int>()
    var analysisIsReady = MutableLiveData<Boolean>()

    // show uploading dialog when set to true
    var isUploading: MutableLiveData<Boolean> = MutableLiveData()
    // end activity when notified
    var endActivity: MutableLiveData<Int> = MutableLiveData()
    // determines whether or not the lease looks safe
    var showSafeRent: MutableLiveData<Boolean> = MutableLiveData()
    // populate the rent issues section
    var rentIssues: MutableLiveData<List<RentIssue>> = MutableLiveData()
    // populate ui with lease details
    var leaseDetails: MutableLiveData<LeaseDocument> = MutableLiveData()
    // if invalid document is provided, show error then exit
    var showErrorDialog: MutableLiveData<Int> = MutableLiveData()

    // TODO: If analysis is not yet ready, should show analyzing... screen
    fun useDocument(key: Int) {
        // Subtract 1 because auto-increment primary key starts at 1
        val document = documentRepository.getDocuments().value?.get(key - 1)
        document?.let {
            isUploading.postValue(false)
            analysisIsReady.postValue(true)
            leaseDetails.postValue(it)
        }?: run {
            showErrorDialog.postValue(0)
        }
    }

    fun surveyFinished(surveyResult: MutableList<Boolean?>) {
        // TODO: send the survey result using API
    }

    /**
     * Launching a new coroutine to insert the data in a non-blocking way
     */
    private fun insertDocument(leaseDocument: LeaseDocument) = viewModelScope.launch(Dispatchers.IO) {
        documentRepository.addDocument(leaseDocument)
    }

    /**
     * Upload the lease for analysis.
     */
    fun uploadLease() {
        isUploading.postValue(true)
        // TODO: Make an API call for uploading lease
        val thread = Thread(Runnable {
            Thread.sleep(5000)
            isUploading.postValue(false)
            analysisIsReady.postValue(false)    // analysis is not ready immediately
        })
        thread.start()
    }

    fun cancelAnalysis() {
        endActivity.postValue(0)
    }

    /**
     *
    showSafeRent.postValue(rentIsSafe)
    rentIssues.postValue(dummyIssues)
    leaseDetails.postValue(dummyDocument)
    insertDocument(dummyDocument)
     */
}