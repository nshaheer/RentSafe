package com.leaseguard.leaseguard.api

import com.leaseguard.leaseguard.models.ApiResponse
import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part


interface AnalysisService {

    @Multipart
    @POST("leases")
    fun sendPdf(
            @Part file: MultipartBody.Part
    ): Call<ResponseBody>

    @GET("leases/5f2289a36e20e2f22708b9ef")
    fun getLease() : Call<ApiResponse>
}
