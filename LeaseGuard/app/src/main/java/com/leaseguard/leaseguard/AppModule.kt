package com.leaseguard.leaseguard

import android.content.Context
import com.leaseguard.leaseguard.repositories.DocumentRepository
import com.leaseguard.leaseguard.database.LeaseRoomDatabase
import dagger.Module
import dagger.Provides
import javax.inject.Singleton

@Module
class AppModule {
    @Singleton
    @Provides
    fun provideContext(application: LeaseGuardApplication): Context {
        return application
    }

    @Provides
    @Singleton
    fun provideDocumentRepository(application: LeaseGuardApplication): DocumentRepository {
        val leaseDao = LeaseRoomDatabase.getDatabase(application).leaseDao()
        return DocumentRepository(leaseDao)
    }
}