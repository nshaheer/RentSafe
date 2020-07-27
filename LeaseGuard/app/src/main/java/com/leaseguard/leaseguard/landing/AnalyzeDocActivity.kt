package com.leaseguard.leaseguard.landing

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.lifecycle.Observer
import com.leaseguard.leaseguard.BaseActivity
import com.leaseguard.leaseguard.R
import com.leaseguard.leaseguard.landing.SafeRentActivity.Companion.DOCUMENT_KEY
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.models.RentIssue
import kotlinx.android.synthetic.main.activity_analyzedoc.*
import javax.inject.Inject

class AnalyzeDocActivity : BaseActivity<AnalyzeDocActivityViewModel>() {
    private val EMAIL_CODE = 1

    @Inject
    lateinit var analyzeDocViewModel: AnalyzeDocActivityViewModel

    var analyzingDialog: AlertDialog? = null

    var switchy = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_analyzedoc)
        analyzeDocActivity.visibility = View.GONE

        supportActionBar?.title = "Analyze Document"
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        val documentKey: String? = intent.getStringExtra(DOCUMENT_KEY)
        documentKey?.let {
            analyzeDocViewModel.useDocument(it)
        }?: run {
            analyzeDocViewModel.doAnalysis()
        }
        analyzeDocViewModel.showErrorDialog.observe(this, Observer {

        })

        //TODO: save state and restore
        analyzeDocViewModel.isLoading.observe(this, Observer { isLoading ->
            if (isLoading) {
                showLoading()
            } else {
                hideLoading()
            }
        })
        analyzeDocViewModel.endActivity.observe(this, Observer {
            showErrorThenExit()
        })

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
            // update the intent to hold the newest document key
            intent.putExtra(DOCUMENT_KEY, leaseDetail.uuid)
        })

        // TODO: remove this, only here for demo
        headerImage.setOnClickListener {
            analyzeDocViewModel.showSafeRent.postValue(switchy)
            switchy = !switchy
        }

        ratingsButton.setOnClickListener {
            val gmmIntentUri = Uri.parse("geo:0,0?q=King Street Towers, 333 King St N, Waterloo, Ontario") // [Property Name, Street Address, City, Province]
            val mapIntent = Intent(Intent.ACTION_VIEW, gmmIntentUri)
            mapIntent.setPackage("com.google.android.apps.maps")
            startActivity(mapIntent)
        }

        signLeaseButton.setOnClickListener {
            val intent = Intent(this, SignLeaseActivity::class.java)
            startActivity(intent)
        }
    }

    private fun populateLeaseDetails(leaseDetail: LeaseDocument) {
        // Lease Details Section
        rentAmountField.text = String.format(getText(R.string.rent_amount_per_month).toString(), leaseDetail.rent.toFloat())
        rentDurationField.text = leaseDetail.dateRange
        keyDepositField.text = "$50" // placeholder
        petsAllowedField.text = if (analyzeDocViewModel.showSafeRent.value!!) "YES" else "NO" // placeholder
        // Property Info Section
        propertyNameField.text = leaseDetail.title
        addressField.text = leaseDetail.address
        landlordField.text = "Sage Corporation"
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

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_analyze_doc, menu)
        return super.onCreateOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        return when (item?.itemId) {
            android.R.id.home -> {
                setResult(RESULT_OK)
                finish()
                return true
            }
            R.id.action_share -> {
                val intent = Intent(Intent.ACTION_SENDTO)
                intent.data = Uri.parse("mailto:") // only email apps should handle this
//                intent.putExtra(Intent.EXTRA_EMAIL, "desmond.lua@luasoftware.com")
//                intent.putExtra(Intent.EXTRA_SUBJECT,"Feedback")

                startActivityForResult(intent, EMAIL_CODE)
//                if (intent.resolveActivity(activity.packageManager) != null) {
//                    startActivity(intent)
//                }
                return true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    private fun showErrorThenExit() {
        AlertDialog.Builder(this)
                .setTitle("Invalid document")
                .setMessage("Something went wrong while reading this document")
                .setPositiveButton("GO BACK") { _, _ ->
                    finish()
                }
                .setCancelable(false)
                .create()
                .show()
    }

    private fun showLoading() {
        analyzingDialog = AlertDialog.Builder(this)
                .setTitle("Analyzing document...")
                .setMessage("We are automatically checking to see if there are any issues with your lease")
                .setPositiveButton("CANCEL") { _, _ ->
                    analyzeDocViewModel.cancelAnalysis()
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