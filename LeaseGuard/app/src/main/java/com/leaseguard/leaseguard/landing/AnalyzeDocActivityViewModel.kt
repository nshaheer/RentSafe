package com.leaseguard.leaseguard.landing

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.models.RentIssue
import com.leaseguard.leaseguard.repositories.DocumentRepository
import javax.inject.Inject

class AnalyzeDocActivityViewModel @Inject constructor(private val documentRepository: DocumentRepository) : ViewModel() {
    val rentIsSafe = false
    val dummyDocument = LeaseDocument("Luxe Waterloo", "333 King Street N", 600, "May 1, 2017 - Aug 31, 2017", 2)
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

    var isLoading: MutableLiveData<Boolean> = MutableLiveData()
    var endActivity: MutableLiveData<Int> = MutableLiveData()
    var showSafeRent: MutableLiveData<Boolean> = MutableLiveData()
    var rentIssues: MutableLiveData<List<RentIssue>> = MutableLiveData()
    var leaseDetails: MutableLiveData<LeaseDocument> = MutableLiveData()

    fun doAnalysis() {
        isLoading.postValue(true)
        // TODO: Make an API call
        val thread = Thread(Runnable {
            Thread.sleep(2000)
            isLoading.postValue(false)
            showSafeRent.postValue(rentIsSafe)
            rentIssues.postValue(dummyIssues)
            leaseDetails.postValue(dummyDocument)
            documentRepository.addDocument(dummyDocument)
        })
        thread.start()
    }

    fun cancelAnalysis() {
        endActivity.postValue(0)
    }
}