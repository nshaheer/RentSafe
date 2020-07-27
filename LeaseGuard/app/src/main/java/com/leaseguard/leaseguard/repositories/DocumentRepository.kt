package com.leaseguard.leaseguard.repositories

import com.leaseguard.leaseguard.models.LeaseDocument
import javax.inject.Inject

class DocumentRepository @Inject constructor() {
    private var documents: HashMap<String, LeaseDocument>? = HashMap()

    fun getDocuments(): List<LeaseDocument> {
        return documents?.values?.toList()?: listOf()
    }

    fun addDocument(doc: LeaseDocument) {
        documents?.put(doc.uuid, doc)
    }

    fun getDocument(key: String): LeaseDocument? {
        return documents?.get(key)
    }
}