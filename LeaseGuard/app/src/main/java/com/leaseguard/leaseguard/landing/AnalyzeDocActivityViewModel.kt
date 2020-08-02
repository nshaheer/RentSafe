package com.leaseguard.leaseguard.landing


import android.util.Base64
import android.util.Log
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.google.gson.JsonObject
import com.leaseguard.leaseguard.api.AnalysisService
import com.leaseguard.leaseguard.api.AnalysisServiceBuilder
import com.leaseguard.leaseguard.models.ApiResponse
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.models.RentIssue
import com.leaseguard.leaseguard.repositories.DocumentRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


import javax.inject.Inject

class AnalyzeDocActivityViewModel @Inject constructor(private val documentRepository: DocumentRepository) : ViewModel() {
    val rentIsSafe = false
    val dummyDocument = LeaseDocument("N/A","Luxe Waterloo", "333 King Street N", 600, "May 1, 2017 - Aug 31, 2017", 2, "", "", ByteArray(0))
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

    fun useDocument(key: String) {

        val document = documentRepository.getDocuments().value?.find { it.id == key }
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
        documentRepository.deleteAll()
        documentRepository.addDocument(leaseDocument)
    }

    @ExperimentalStdlibApi
    fun doAnalysis() {
        isLoading.postValue(true)
        // TODO: Make an API call
        val thread = Thread(Runnable {
            Thread.sleep(5000)
            isLoading.postValue(false)
            showSafeRent.postValue(rentIsSafe)
            rentIssues.postValue(dummyIssues)
            leaseDetails.postValue(dummyDocument)
            //insertDocument(dummyDocument)
        })
        thread.start()
        val analysisService = AnalysisServiceBuilder.createService(AnalysisService::class.java)
        //val leaseDocs = analysisService.sendPdf()

        analysisService.getLease().enqueue(object: Callback<ApiResponse> {
            override fun onResponse(call: Call<ApiResponse>, response: Response<ApiResponse>) {
                if (response.isSuccessful) {
                    // When data is available, populate LiveData
                     var jsonObject : JsonObject = response.body()?.lease ?: JsonObject()
                    jsonObject.get("Id")
                    Log.d("LEASE-RESPONSE", jsonObject.toString())
                    Log.d("LEASE", response.toString())
                    var thumbnail = jsonObject.get("Thumbnail").asString
                    thumbnail = thumbnail.substring(2, thumbnail.length - 1)

                    var thumbnailByteArray = Base64.decode(thumbnail, Base64.DEFAULT)
                    var jsonArray = jsonObject.getAsJsonArray("Issues")
                    var document = LeaseDocument(jsonObject.get("Id").asString, jsonObject.get("Title").asString,
                            jsonObject.get("Address").asString, 900, jsonObject.get("Dates").asString,
                            jsonArray.size(), jsonArray.toString(), jsonObject.get("Status").asString, thumbnailByteArray)
                    insertDocument(document)
                }
            }

            override fun onFailure(call: Call<ApiResponse>, t: Throwable) {
                t.printStackTrace()
            }
        })


    }

    fun cancelAnalysis() {
        endActivity.postValue(0)
    }
}