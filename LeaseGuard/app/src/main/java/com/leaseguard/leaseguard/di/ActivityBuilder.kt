package com.leaseguard.leaseguard.di

import com.leaseguard.leaseguard.views.AnalyzeDocActivity
import com.leaseguard.leaseguard.views.SafeRentActivity
import com.leaseguard.leaseguard.modules.SafeRentActivityModule
import dagger.Module

import dagger.android.ContributesAndroidInjector


@Module
abstract class ActivityBuilder {
    @ContributesAndroidInjector(modules = [SafeRentActivityModule::class])
    abstract fun contributeSafeRentActivity(): SafeRentActivity

    @ContributesAndroidInjector(modules = [SafeRentActivityModule::class])
    abstract fun contributeAnalyzeDocActivity(): AnalyzeDocActivity
}