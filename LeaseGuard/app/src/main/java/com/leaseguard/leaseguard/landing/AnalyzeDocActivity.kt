package com.leaseguard.leaseguard.landing

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.*
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.core.content.ContextCompat
import androidx.core.content.edit
import androidx.core.view.setMargins
import androidx.core.view.updateLayoutParams
import androidx.lifecycle.Observer
import com.leaseguard.leaseguard.BaseActivity
import com.leaseguard.leaseguard.R
import com.leaseguard.leaseguard.landing.SafeRentActivity.Companion.DOCUMENT_KEY
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.models.RentIssue
import kotlinx.android.synthetic.main.activity_analyzedoc.*
import kotlinx.android.synthetic.main.activity_analyzedoc.headerImage
import kotlinx.android.synthetic.main.activity_analyzedoc.headerText
import kotlinx.android.synthetic.main.activity_analyzedoc_survey.*
import kotlinx.android.synthetic.main.activity_analyzedoc_survey_permission.accept_button
import kotlinx.android.synthetic.main.activity_analyzedoc_survey_permission.reject_button
import javax.inject.Inject

class AnalyzeDocActivity : BaseActivity<AnalyzeDocActivityViewModel>() {
    private val EMAIL_CODE = 1
    private val SURVEY_DONE_KEY = "SURVEY_DONE"

    @Inject
    lateinit var analyzeDocViewModel: AnalyzeDocActivityViewModel

    var analyzingDialog: AlertDialog? = null

    @ExperimentalStdlibApi
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportActionBar?.title = "Analyze Document"
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        val documentKey: String? = intent.getStringExtra(DOCUMENT_KEY)
        if (documentKey != null) {
            analyzeDocViewModel.useDocument(documentKey)
        } else {
            initUploadingDialogListeners()
            analyzeDocViewModel.uploadLease()
        }

        // When analysis is ready, show analysis details view
        analyzeDocViewModel.analysisIsReady.observe(this, Observer {
            if (it) {
                showAnalysisCompleteView()
            } else {
                showAnalyzingView()
            }
        })
    }

    private fun initUploadingDialogListeners() {
        analyzeDocViewModel.showErrorDialog.observe(this, Observer {
            // TODO: show error dialog if something goes wrong when uploading
        })

        //TODO: save state and restore
        analyzeDocViewModel.isUploading.observe(this, Observer { isLoading ->
            if (isLoading) {
                showUploadingDialog()
            } else {
                hideUploadingDialog()
            }
        })
        analyzeDocViewModel.endActivity.observe(this, Observer {
            showErrorThenExit()
        })
    }

    private fun showAnalyzingView() {
        analyzeDocViewModel.surveyIsComplete.observe(this, Observer {
            this.getPreferences(MODE_PRIVATE).edit {
                this.putBoolean(SURVEY_DONE_KEY, true)
            }
        })
        if (this.getPreferences(MODE_PRIVATE).getBoolean(SURVEY_DONE_KEY, false)) {
            finish()
        } else {
            setContentView(R.layout.activity_analyzedoc_survey_permission)
            accept_button.setOnClickListener {
                showSurveyView()
            }
            reject_button.setOnClickListener {
                finish()
            }
        }
    }

    private val surveyQuestions = listOf(
            R.string.survey_question1,
            R.string.survey_question2,
            R.string.survey_question3,
            R.string.survey_question4
    )

    // Assuming restarting survey when destroyed
    private fun showSurveyView() {
        var questionCounter = 0
        val answers = MutableList<Boolean?>(surveyQuestions.size) { null }
        setContentView(R.layout.activity_analyzedoc_survey)
        findViewById<Button>(R.id.accept_button).setOnClickListener {
            answers[questionCounter] = true
            questionCounter++
            if (questionCounter >= surveyQuestions.size) {
                analyzeDocViewModel.surveyFinished(answers)
                showSurveyFinishedView()
                return@setOnClickListener
            }
            bodyText.text = getText(surveyQuestions[questionCounter])
        }
        findViewById<Button>(R.id.reject_button).setOnClickListener {
            answers[questionCounter] = false
            questionCounter++
            if (questionCounter >= surveyQuestions.size) {
                analyzeDocViewModel.surveyFinished(answers)
                showSurveyFinishedView()
                return@setOnClickListener
            }
            bodyText.text = getText(surveyQuestions[questionCounter])
        }
    }

    private fun showSurveyFinishedView() {
        setContentView(R.layout.activity_analyzedoc_survey_permission)
        findViewById<ImageView>(R.id.headerImage).setImageDrawable(getDrawable(R.drawable.ic_empty_thank_you))
        findViewById<TextView>(R.id.headerText).text = getText(R.string.thank_you)
        findViewById<TextView>(R.id.bodyText1).text = getText(R.string.survey_end_body1)
        findViewById<TextView>(R.id.bodyText2).text = getText(R.string.survey_end_body2)
        findViewById<Button>(R.id.accept_button).setText(R.string.go_back_home)
        findViewById<Button>(R.id.accept_button).setOnClickListener {
            finish()
        }
        findViewById<TextView>(R.id.reject_button).visibility = View.GONE
    }

    private fun showAnalysisCompleteView() {
        setContentView(R.layout.activity_analyzedoc)

        analyzeDocViewModel.rentIssues.observe(this, Observer { rentIssues ->
            if (rentIssues.size == 0) {
                headerImage.setImageResource(R.drawable.ic_empty_success)
                headerText.text = getText(R.string.looksgood)
                headerText.setTextColor(getColor(R.color.successgreen))
                issueText.text = getText(R.string.no_issues_body)
                warningsContainer.visibility = View.GONE
            } else {
                val numIssues = rentIssues.size
                headerImage.setImageResource(R.drawable.ic_empty_warning)
                headerText.text = getText(R.string.watchout)
                headerText.setTextColor(getColor(R.color.watchoutred))
                issueText.text = if (numIssues == 1) getString(R.string.issue_body) else getString(R.string.issues_body, numIssues)
                warningsContainer.visibility = View.VISIBLE
            }
        })
        analyzeDocViewModel.rentIssues.observe(this, Observer { rentIssues ->
            populateRentIssues(rentIssues)
        })
        analyzeDocViewModel.leaseDetails.observe(this, Observer { leaseDetail ->
            populateLeaseDetails(leaseDetail)
            // update the intent to hold the newest document key
            intent.putExtra(DOCUMENT_KEY, leaseDetail.id)
        })

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
        if (leaseDetail.rent == 0) {
            rentAmountField.text = getText(R.string.not_available)
        } else {
            rentAmountField.text = String.format(getText(R.string.rent_amount_per_month).toString(), leaseDetail.rent.toFloat())
        }

        rentDurationField.text = leaseDetail.date
        keyDepositField.text = "$50" // placeholder TODO: update ML analyzer to get actual key deposit value
        petsAllowedField.text = "NO" // placeholder TODO: Update to use dynamic API value
        // Property Info Section
        propertyNameField.text = "King Street Towers" // placeholder TODO: update ML analyzer to get actual property name
        addressField.text = leaseDetail.address
        landlordField.text = leaseDetail.title
    }

    private fun populateRentIssues(rentIssues: List<RentIssue>) {
        warningsContainer.removeAllViews()
        for (rentIssue in rentIssues) {
            val warning = layoutInflater.inflate(R.layout.view_warning, warningsContainer, false) as TextView
            warning.text = rentIssue.issue
            if (rentIssue.isWarning) {
                warning.compoundDrawableTintList = ContextCompat.getColorStateList(applicationContext, R.color.warningyellow)
            } else {
                warning.compoundDrawableTintList = ContextCompat.getColorStateList(applicationContext, R.color.watchoutred)
            }
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
                val view = layoutInflater.inflate(R.layout.dialog_share_document, null) as EditText
                val dialog = AlertDialog.Builder(this)
                        .setTitle("Email Document")
                        .setView(view)
                        .setPositiveButton("SEND") { _, _ ->
                            // TODO: Make API call to send lease_id, email_address
                        }
                        .setNeutralButton("CANCEL", null)
                        .show()

                view.requestFocus()
                view.updateLayoutParams<ViewGroup.MarginLayoutParams> { setMargins(32) }
                dialog.window?.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE)

                view.setOnEditorActionListener { _, actionId, _ ->
                    if (actionId == EditorInfo.IME_ACTION_DONE) {
                        // TODO: Make API call to send lease_id, email_address
                        dialog.dismiss()
                        return@setOnEditorActionListener true
                    }
                    false
                }

                return true
            }
            R.id.action_delete -> {
                // TODO: Implement delete individual lease documents
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

    private fun showUploadingDialog() {
        analyzingDialog = AlertDialog.Builder(this)
                .setTitle("Uploading document...")
                .setMessage("We are uploading your lease documents so we can carefully analyze them")
                .setPositiveButton("CANCEL") { _, _ ->
                    analyzeDocViewModel.cancelAnalysis()
                }
                .setCancelable(false)
                .create()
        analyzingDialog?.show()
    }

    private fun hideUploadingDialog() {
        analyzingDialog?.dismiss()
    }

    override fun getViewModel(): AnalyzeDocActivityViewModel {
        return analyzeDocViewModel
    }
}