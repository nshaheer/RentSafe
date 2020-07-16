package com.leaseguard.leaseguard.landing

import dagger.Module
import dagger.Provides

@Module
class SafeRentActivityModule {
    @Provides
    fun provideSafeRentActivityViewModel() : SafeRentActivityViewModel {
        return SafeRentActivityViewModel()
    }

    @Provides
    fun provideAnalyzeDocActivityViewModel(): AnalyzeDocActivityViewModel {
        return AnalyzeDocActivityViewModel()
    }
}