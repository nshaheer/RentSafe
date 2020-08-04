package com.leaseguard.leaseguard.models

data class RentIssue(
        val issue: String,
        val title: String,
        val description: String,
        val isWarning : Boolean
)
