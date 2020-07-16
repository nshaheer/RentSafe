package com.leaseguard.leaseguard

import android.content.Context
import com.leaseguard.leaseguard.repositories.DocumentRepository
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
    fun provideDocumentRepository(): DocumentRepository {
        return DocumentRepository()
    }
}