package com.leaseguard.leaseguard.landing

import android.app.AlertDialog
import android.os.Bundle
import android.view.MenuItem
import android.view.View
import android.widget.TextView
import androidx.lifecycle.Observer
import com.leaseguard.leaseguard.BaseActivity
import com.leaseguard.leaseguard.R
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.models.RentIssue
import kotlinx.android.synthetic.main.activity_analyzedoc.*
import javax.inject.Inject

class AnalyzeDocActivity : BaseActivity<AnalyzeDocActivityViewModel>() {

    @Inject
    lateinit var analyzeDocViewModel: AnalyzeDocActivityViewModel

    var analyzingDialog: AlertDialog? = null

    var switchy = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_analyzedoc)
        analyzeDocActivity.visibility = View.GONE

        supportActionBar?.title = "Analyze Document"
        supportActionBar?.setDisplayShowHomeEnabled(true)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        //TODO: save state and restore
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

        // TODO: remove this, only here for demo
        headerImage.setOnClickListener {
            analyzeDocViewModel.showSafeRent.postValue(switchy)
            switchy = !switchy
        }

        analyzeDocViewModel.showSafeRent.observe(this, Observer { showSafeRentPage ->
            if (showSafeRentPage) {
                headerImage.setImageResource(R.drawable.ic_empty_success)
                headerText.text = getText(R.string.looksgood)
                headerText.setTextColor(getColor(R.color.successgreen))
                issueText.text = getText(R.string.no_issues_body)
                warningsContainer.visibility = View.GONE
            } else {
                headerImage.setImageResource(R.drawable.ic_empty_warning)
                headerText.text = getText(R.string.watchout)
                headerText.setTextColor(getColor(R.color.watchoutred))
                issueText.text = getText(R.string.issues_body)
                warningsContainer.visibility = View.VISIBLE
            }
        })
        analyzeDocViewModel.rentIssues.observe(this, Observer { rentIssues ->
            populateRentIssues(rentIssues)
        })
        analyzeDocViewModel.leaseDetails.observe(this, Observer { leaseDetail ->
            populateLeaseDetails(leaseDetail)
        })
    }

    private fun populateLeaseDetails(leaseDetail: LeaseDocument) {
        propertyField.text = leaseDetail.title
        addressField.text = leaseDetail.address
        rentAmountField.text = String.format(getText(R.string.rent_amount_per_month).toString(), leaseDetail.rent.toFloat())
        rentalDurationField.text = leaseDetail.dateRange
    }

    private fun populateRentIssues(rentIssues: List<RentIssue>) {
        warningsContainer.removeAllViews()
        for (rentIssue in rentIssues) {
            val warning = layoutInflater.inflate(R.layout.view_warning, warningsContainer, false) as TextView
            warning.text = rentIssue.issue
            warning.setOnClickListener {
                val dialog = AlertDialog.Builder(this)
                        .setTitle(rentIssue.title)
                        .setMessage(rentIssue.description)
                        .setPositiveButton("OKAY") { dialogInterface, _ ->
                            dialogInterface.dismiss()
                        }
                        .setCancelable(false)
                        .create()
                dialog?.show()
            }
            warningsContainer.addView(warning)
        }
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        return when (item?.itemId) {
            android.R.id.home -> {
                finish()
                return true
            }
            else -> super.onOptionsItemSelected(item)
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