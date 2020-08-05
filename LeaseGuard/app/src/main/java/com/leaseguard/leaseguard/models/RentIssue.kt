package com.leaseguard.leaseguard.models

/**
 * RentIssue Model to represent a given rent issue
 */
data class RentIssue(
        val issue: String,
        val title: String,
        val description: String,
        val isWarning : Boolean
)
