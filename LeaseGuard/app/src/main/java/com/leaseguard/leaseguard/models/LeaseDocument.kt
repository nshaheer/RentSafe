package com.leaseguard.leaseguard.models;

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "lease_table")

class LeaseDocument(

        @PrimaryKey
        val id: String,
        val title: String, // Landlord / Property Management name
        val address: String,
        val rent: Int,
        val date: String,
        val numIssues: Int,
        val issueDetails : String,
        val status: String,
        val thumbnail : ByteArray,
        val documentName : String

        )
