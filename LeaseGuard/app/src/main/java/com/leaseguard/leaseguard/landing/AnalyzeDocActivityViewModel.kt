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
    val dummyDocument = LeaseDocument(0,"Luxe Waterloo", "333 King Street N", 800, "May 1, 2017 - Aug 31, 2017", 2)
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

    // show loading dialog when set to true
    var isLoading: MutableLiveData<Boolean> = MutableLiveData()
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

    fun useDocument(key: Int) {
        // Subtract 1 because auto-increment primary key starts at 1
        val document = documentRepository.getDocuments().value?.get(key - 1)
        document?.let {
            isLoading.postValue(false)
            leaseDetails.postValue(it)
        }?: run {
            showErrorDialog.postValue(0)
        }
    }

    /**
     * Launching a new coroutine to insert the data in a non-blocking way
     */
    private fun insertDocument(leaseDocument: LeaseDocument) = viewModelScope.launch(Dispatchers.IO) {
        documentRepository.addDocument(leaseDocument)
    }

    fun doAnalysis() {
        isLoading.postValue(true)
        // TODO: Make an API call
        val thread = Thread(Runnable {
            Thread.sleep(5000)
            isLoading.postValue(false)
            showSafeRent.postValue(rentIsSafe)
            rentIssues.postValue(dummyIssues)
            leaseDetails.postValue(dummyDocument)
            insertDocument(dummyDocument)
        })
        thread.start()
    }

    fun cancelAnalysis() {
        endActivity.postValue(0)
    }
}