package com.leaseguard.leaseguard.api

import com.leaseguard.leaseguard.models.ApiResponse
import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.*


interface AnalysisService {

    @Multipart
    @POST("leases")
    fun sendPdf(
            @Part file: MultipartBody.Part
    ): Call<ResponseBody>

    @GET("leases/5f2289a36e20e2f22708b9ef")
    fun getLease() : Call<ApiResponse>

    @Headers("Content-type: application/json")
    @POST("questionnaires")
    fun sendSurveyResult(@Body body: String) : Call<String>
}
