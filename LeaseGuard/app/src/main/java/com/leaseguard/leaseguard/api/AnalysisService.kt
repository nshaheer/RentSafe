package com.leaseguard.leaseguard.api

import com.leaseguard.leaseguard.models.ApiResponse
import com.leaseguard.leaseguard.models.LeaseDocument
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.Response
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.*


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
}
