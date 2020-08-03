package com.leaseguard.leaseguard.repositories

import androidx.lifecycle.LiveData
import com.leaseguard.leaseguard.database.LeaseDao
import com.leaseguard.leaseguard.models.LeaseDocument
import javax.inject.Inject

class DocumentRepository @Inject constructor(private val leaseDao: LeaseDao) {
    private var documents: LiveData<List<LeaseDocument>> = leaseDao.getLeases()

    fun getDocuments(): LiveData<List<LeaseDocument>> {
        return documents
    }

    suspend fun addDocument(leaseDocument: LeaseDocument) {
        leaseDao.insert(leaseDocument)
    }

    suspend fun deleteDocument(leaseDocument: LeaseDocument) {
        leaseDao.delete(leaseDocument)
    }

    suspend fun deleteAll() {
        leaseDao.deleteAll()
    }
}