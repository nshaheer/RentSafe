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
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import org.json.JSONArray
import org.json.JSONObject
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.File
import javax.inject.Inject

class AnalyzeDocActivityViewModel @Inject constructor(private val documentRepository: DocumentRepository) : ViewModel() {
    var analysisIsReady = MutableLiveData<Boolean>()
    var surveyIsComplete = MutableLiveData<Int>()

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

    fun useDocument(key: String) {
        val document = documentRepository.getDocuments().value?.find { it.id == key }
        document?.let {
            isUploading.postValue(false)
            analysisIsReady.postValue(true)
            leaseDetails.postValue(it)
            updateRentIssuesWithJsonString(it.issueDetails)
        }?: run {
            showErrorDialog.postValue(0)
        }
    }

    fun surveyFinished(surveyResult: MutableList<Boolean?>) {
        val jsonResult = generateSurveyResultJson(surveyResult)
        postSurveyResult(jsonResult)
    }

    private fun generateSurveyResultJson(surveyResult: MutableList<Boolean?>): String {
        val stringBuilder = StringBuilder()
        stringBuilder.append("{")
        for (i in 0 until surveyResult.size) {
            val str = "\"question$i\" : \"${surveyResult.get(i)}\""
            stringBuilder.append(str)
            if (i < surveyResult.size - 1) {
                stringBuilder.append(",")
            }
        }
        stringBuilder.append("}")
        return stringBuilder.toString()
    }

    private fun postSurveyResult(result: String) {
        val analysisService = AnalysisServiceBuilder.createService(AnalysisService::class.java)
        analysisService.sendSurveyResult(result).enqueue(object : Callback<String> {
            override fun onFailure(call: Call<String>, t: Throwable) {
                // TODO: handle failure
            }

            override fun onResponse(call: Call<String>, response: Response<String>) {
                surveyIsComplete.postValue(0)
            }
        })
    }

    /**
     * Launching a new coroutine to insert the data in a non-blocking way
     */
    fun insertDocument(leaseDocument: LeaseDocument) = viewModelScope.launch(Dispatchers.IO) {
        documentRepository.deleteAll()
        documentRepository.addDocument(leaseDocument)
    }

    /**
     * Takes a JSON string representing an Array of RentIssues and converts it into a list of RentIssues
     * and updates the view with our new data
     */
    fun updateRentIssuesWithJsonString(str : String) {
        var newRentIssues : ArrayList<RentIssue> = ArrayList()
        var jsonArray : JSONArray = JSONArray(str)
        for (i in 0 until jsonArray.length()) {
            var jsonObj : JSONObject = jsonArray.getJSONObject(i)
            newRentIssues.add(RentIssue(jsonObj.getString("Issue"), jsonObj.getString("Title"), jsonObj.getString("Description"), jsonObj.getBoolean("IsWarning")))
        }
        rentIssues.postValue(newRentIssues)
    }

    /**
     * Upload the lease for analysis.
     */
    @ExperimentalStdlibApi
    fun uploadLease() {
        isUploading.postValue(true)
        // TODO: Make an API call for uploading lease
        val thread = Thread(Runnable {
            Thread.sleep(5000)
            isUploading.postValue(false)
            analysisIsReady.postValue(false)    // analysis is not ready immediately
        })
        thread.start()
        val analysisService = AnalysisServiceBuilder.createService(AnalysisService::class.java)
        //val leaseDocs = analysisService.sendPdf()
        var path = documentRepository.getPdfUri()?.path?.split(":")
        Log.d("URI", documentRepository.getPdfUri()?.path)
        var pathStr = path?.get(path.size - 1)
        var file = File(pathStr)
        var pdf : RequestBody? = RequestBody.create("*/*".toMediaTypeOrNull(), file)
        val fileToUpload = pdf?.let { MultipartBody.Part.createFormData("file", file.name, it) }
        if (fileToUpload != null) {
            Log.d("PDF", file.name + " :: " + fileToUpload.toString())
            analysisService.sendPdf(fileToUpload).enqueue(object: Callback<ApiResponse> {
                override fun onResponse(call: Call<ApiResponse>, response: Response<ApiResponse>) {
                    if (response.isSuccessful) {
                        // When data is available, populate LiveData
                        var jsonObject : JsonObject = response.body()?.lease ?: JsonObject()
                        Log.d("LEASE-RESPONSE", jsonObject.toString())
                        Log.d("LEASE", response.toString())
                        var thumbnail = jsonObject.get("Thumbnail").asString
                        if (thumbnail.length > 2) {
                            // b' has to be removed from the string prior to the encoding
                            thumbnail = thumbnail.substring(2, thumbnail.length - 1)
                        }
                        var thumbnailByteArray = Base64.decode(thumbnail, Base64.DEFAULT)
                        var jsonArray = jsonObject.getAsJsonArray("Issues")
                        var document = LeaseDocument(jsonObject.get("Id").asString, jsonObject.get("Title").asString,
                                jsonObject.get("Address").asString, jsonObject.get("Rent").asInt, jsonObject.get("Dates").asString,
                                jsonArray.size(), jsonArray.toString(), jsonObject.get("Status").asString, thumbnailByteArray, jsonObject.get("DocumentName").asString)
                        updateRentIssuesWithJsonString(jsonArray.toString())
                        insertDocument(document)
                        leaseDetails.postValue(document)
                    }
                }

                override fun onFailure(call: Call<ApiResponse>, t: Throwable) {
                    t.printStackTrace()
                }
            })
        }


    }

    fun cancelAnalysis() {
        endActivity.postValue(0)
    }
}