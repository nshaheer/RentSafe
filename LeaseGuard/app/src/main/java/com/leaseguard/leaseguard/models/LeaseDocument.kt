package com.leaseguard.leaseguard.models;

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * LeaseDocument model class used to represent an entity that will be stored in
 * our SQLite database within the table 'lease_table'
 */
@Entity(tableName = "lease_table")
class LeaseDocument(

        @PrimaryKey
        val id: String,
        val title: String, // Landlord / Property Management name
        val address: String,
        val rent: Int, // Rent amount
        val date: String, // Date range of lease
        val numIssues: Int,
        val issueDetails : String, // Rent Issue details stored as JSON text
        val status: String, // Completion status
        val thumbnail : ByteArray, // Thumbnail image
        val documentName : String

        )
