package com.leaseguard.leaseguard.di

import com.leaseguard.leaseguard.AppModule
import com.leaseguard.leaseguard.LeaseGuardApplication
import com.leaseguard.leaseguard.landing.SafeRentActivityModule
import dagger.Component
import dagger.android.AndroidInjector
import dagger.android.support.AndroidSupportInjectionModule
import javax.inject.Singleton

@Singleton
@Component(
        modules = [
            AndroidSupportInjectionModule::class,
            AppModule::class,
            SafeRentActivityModule::class,
            ActivityBuilder::class
        ]
)
interface AppComponent : AndroidInjector<LeaseGuardApplication> {
    @Component.Builder
    abstract class Builder : AndroidInjector.Builder<LeaseGuardApplication>()
}