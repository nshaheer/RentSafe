package com.leaseguard.leaseguard

import com.leaseguard.leaseguard.di.DaggerAppComponent.builder
import dagger.android.AndroidInjector
import dagger.android.DaggerApplication

class LeaseGuardApplication : DaggerApplication() {
    private val instance: LeaseGuardApplication? = null

    @Synchronized
    fun getInstance(): LeaseGuardApplication? {
        return instance
    }

    override fun applicationInjector(): AndroidInjector<out DaggerApplication?>? {
        return builder().create(this)
    }
}