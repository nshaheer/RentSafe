package com.leaseguard.leaseguard.api

import com.leaseguard.leaseguard.models.ApiResponse
import okhttp3.MultipartBody
import retrofit2.Call
import retrofit2.http.*

/**
 * Interface utilized by Retrofit Http Client Library to call endpoints of the AnalysisService backend
 */
interface AnalysisService {
    @Multipart
    @POST("leases")
    fun sendPdf(
            @Part file: MultipartBody.Part
    ): Call<ApiResponse>

    @GET("leases/5f2289a36e20e2f22708b9ef")
    fun getLease() : Call<ApiResponse>

    @GET("leases/{id}")
    fun getLease(@Path("id") id : String) : Call<ApiResponse>

    @Headers("Content-type: application/json")
    @POST("questionnaires")
    fun sendSurveyResult(@Body body: String) : Call<String>

    @POST("leases/{documentId}/email")
    fun sendEmail(@Path(value = "documentId") documentId: String, @Query("email") email: String) : Call<Any>
}
