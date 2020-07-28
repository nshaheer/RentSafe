package com.leaseguard.leaseguard.models;

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "lease_table")

class LeaseDocument(

        @PrimaryKey(autoGenerate = true) val id: Int,
        val title: String,
        val address: String,
        val rent: Int,
        val date: String,
        val issues: Int

        )
