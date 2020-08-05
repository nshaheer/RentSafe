package com.leaseguard.leaseguard.views

import android.os.Bundle
import androidx.lifecycle.ViewModel
import dagger.android.support.DaggerAppCompatActivity

/**
 * Base activity for activities that will use dagger injection.
 */
abstract class BaseActivity<T : ViewModel> : DaggerAppCompatActivity() {
    private var viewModel : T? = null
    abstract fun getViewModel() : T

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        this.viewModel = viewModel?:getViewModel()
    }
}