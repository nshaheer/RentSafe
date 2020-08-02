package com.leaseguard.leaseguard.models;

import com.google.gson.JsonObject;
import com.google.gson.annotations.SerializedName;

public class ApiResponse {
    @SerializedName("Lease")
    public JsonObject lease;
}
