package com.leaseguard.leaseguard.repositories

import com.leaseguard.leaseguard.models.LeaseDocument
import javax.inject.Inject

class DocumentRepository @Inject constructor() {
    private var documents: List<LeaseDocument>? = null

    fun getDocuments(): List<LeaseDocument> {
        return documents?: listOf()
    }

    fun addDocument(doc: LeaseDocument) {
        documents = listOf(doc)
    }
}