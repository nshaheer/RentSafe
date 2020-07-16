package com.leaseguard.leaseguard.repositories

import com.leaseguard.leaseguard.models.LeaseDocument
import javax.inject.Inject

class DocumentRepository @Inject constructor() {
    private var documents: ArrayList<LeaseDocument>? = ArrayList()

    fun getDocuments(): List<LeaseDocument> {
        return documents?: listOf()
    }

    fun addDocument(doc: LeaseDocument) {
        documents?.add(doc)
    }
}