package com.leaseguard.leaseguard.models;

import com.google.gson.JsonObject;
import com.google.gson.annotations.SerializedName;

/**
 * API response wrapper class to facilitate JSON parsing
 */
public class ApiResponse {
    @SerializedName("Lease")
    public JsonObject lease;
}
