package com.leaseguard.leaseguard.landing

import android.app.AlertDialog
import android.os.Bundle
import android.view.View
import android.widget.TextView
import androidx.lifecycle.Observer
import com.leaseguard.leaseguard.BaseActivity
import com.leaseguard.leaseguard.R
import kotlinx.android.synthetic.main.activity_analyzedoc.*
import javax.inject.Inject

class AnalyzeDocActivity : BaseActivity<AnalyzeDocActivityViewModel>() {

    @Inject
    lateinit var analyzeDocViewModel: AnalyzeDocActivityViewModel

    var analyzingDialog: AlertDialog? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_analyzedoc)
        analyzeDocActivity.visibility = View.GONE
        analyzeDocViewModel.isLoading.observe(this, Observer { isLoading ->
            if (isLoading) {
                showLoading()
            } else {
                hideLoading()
            }
        })
        analyzeDocViewModel.endActivity.observe(this, Observer {
            finish()
        })
        analyzeDocViewModel.warningText.observe(this, Observer { warningTexts ->
            populateWarningText(warningTexts)
        })
    }

    private fun populateWarningText(warningTexts: List<String>) {
        warningsContainer.removeAllViews()
        for (text in warningTexts) {
            val warning = layoutInflater.inflate(R.layout.view_warning, warningsContainer, false) as TextView
            warning.text = text
            warningsContainer.addView(warning)
        }
    }

    override fun onResume() {
        super.onResume()
        analyzeDocViewModel.doAnalysis()
    }

    private fun showLoading() {
        analyzingDialog = AlertDialog.Builder(this)
                .setTitle("Analyzing document...")
                .setMessage("We are automatically checking to see if there are any issues with your lease")
                .setPositiveButton("CANCEL") { dialogInterface, _ ->
                    analyzeDocViewModel.cancelAnalysis(dialogInterface)
                }
                .setCancelable(false)
                .create()
        analyzingDialog?.show()
    }

    private fun hideLoading() {
        analyzeDocActivity.visibility = View.VISIBLE
        analyzingDialog?.dismiss()
    }

    override fun getViewModel(): AnalyzeDocActivityViewModel {
        return analyzeDocViewModel
    }
}