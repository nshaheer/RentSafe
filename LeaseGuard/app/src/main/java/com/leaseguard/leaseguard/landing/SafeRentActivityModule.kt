package com.leaseguard.leaseguard.landing

import com.leaseguard.leaseguard.repositories.DocumentRepository
import dagger.Module
import dagger.Provides

@Module
class SafeRentActivityModule {
    @Provides
    fun provideSafeRentActivityViewModel(documentRepository: DocumentRepository) : SafeRentActivityViewModel {
        return SafeRentActivityViewModel(documentRepository)
    }

    @Provides
    fun provideAnalyzeDocActivityViewModel(documentRepository: DocumentRepository): AnalyzeDocActivityViewModel {
        return AnalyzeDocActivityViewModel(documentRepository)
    }
}