package com.leaseguard.leaseguard.modules

import com.leaseguard.leaseguard.viewmodels.AnalyzeDocActivityViewModel
import com.leaseguard.leaseguard.viewmodels.SafeRentActivityViewModel
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