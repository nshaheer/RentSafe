package com.leaseguard.leaseguard.di

import com.leaseguard.leaseguard.landing.SafeRentActivity
import com.leaseguard.leaseguard.landing.SafeRentActivityModule
import dagger.Module

import dagger.android.ContributesAndroidInjector


@Module
abstract class ActivityBuilder {
    @ContributesAndroidInjector(modules = [SafeRentActivityModule::class])
    abstract fun contributeSafeRentActivity(): SafeRentActivity
}