package com.leaseguard.leaseguard.views

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.MenuItem
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.net.toUri
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.leaseguard.leaseguard.R
import com.leaseguard.leaseguard.api.SyncService
import com.leaseguard.leaseguard.models.LeaseDocument
import com.leaseguard.leaseguard.viewmodels.SafeRentActivityViewModel
import kotlinx.android.synthetic.main.activity_saferent.*
import kotlinx.android.synthetic.main.card_document.view.*
import java.io.File
import javax.inject.Inject

/**
 * Activity that displays list of lease documents and lets the user upload a new document.
 */
class SafeRentActivity : BaseActivity<SafeRentActivityViewModel>() {
    companion object {
        val DOCUMENT_KEY = "documentKey"
        val ANALYZE_COMPLETED = "COMPLETED"
    }

    private val PHOTO_CODE = 1
    private val PHOTO_LIBRARY_CODE = 2
    private val PDF_CODE = 3
    private val GOOGLE_DRIVE_CODE = 4
    private val ANALYZE_DOC_CODE = 5

    private val REQUEST_EXTERNAL_STORAGE = 1
    private val PERMISSIONS_STORAGE = arrayOf(
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
    )

    @Inject
    lateinit var safeRentViewModel : SafeRentActivityViewModel

    private lateinit var viewAdapter: RecyclerView.Adapter<*>
    private lateinit var viewManager: RecyclerView.LayoutManager

    private val leaseList : ArrayList<LeaseDocument> = ArrayList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_saferent)

        // Set the action bar
        supportActionBar?.title = "RentSafe"
        supportActionBar?.setHomeAsUpIndicator(R.drawable.ic_menu)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        addDocumentFAB.inflate(R.menu.menu_add_document)

        addDocumentFAB.setOnActionSelectedListener { actionItem ->
            when (actionItem.id) {
                R.id.fab_action_googleDrive -> {
                    val intent = Intent()
                            .setType("*/*")
                            .setAction(Intent.ACTION_GET_CONTENT)
                    startActivityForResult(Intent.createChooser(intent, "Select a file"), GOOGLE_DRIVE_CODE)
                    addDocumentFAB.close()
                }
                R.id.fab_action_pdf -> {
                    val intent = Intent()
                            .setType("*/*")
                            .setAction(Intent.ACTION_GET_CONTENT)
                    startActivityForResult(Intent.createChooser(intent, "Select a file"), PDF_CODE)
                    addDocumentFAB.close()
                }
                R.id.fab_action_photoLibrary -> {
                    val pickPhoto = Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
                    startActivityForResult(pickPhoto, PHOTO_LIBRARY_CODE)
                    addDocumentFAB.close()
                }
                R.id.fab_action_photo -> {
                    Intent(MediaStore.ACTION_IMAGE_CAPTURE).also { takePictureIntent ->
                        takePictureIntent.resolveActivity(packageManager)?.also {
                            startActivityForResult(takePictureIntent, PHOTO_CODE)
                        }
                    }
                    addDocumentFAB.close()
                }
            }
            true
        }

        safeRentViewModel.startAnalyzeDocActivity.observe(this, Observer {
            val intent = Intent(this, AnalyzeDocActivity::class.java)
            startActivityForResult(intent, ANALYZE_DOC_CODE)
        })

        safeRentViewModel.documentUpdated.observe(this, Observer { documents ->
            leaseList.clear()
            leaseList.addAll(documents)
            viewAdapter.notifyDataSetChanged()
            if (leaseList.isNotEmpty()) {
                noDocumentContainer.visibility = View.GONE
            } else {
                noDocumentContainer.visibility = View.VISIBLE
            }
        })

        if (leaseList.isNotEmpty()) {
            noDocumentContainer.visibility = View.GONE
        } else {
            noDocumentContainer.visibility = View.VISIBLE
        }
        viewAdapter = DocumentAdapter(leaseList)
        viewManager = LinearLayoutManager(this)
        recyclerDocumentList.setHasFixedSize(true)
        recyclerDocumentList.layoutManager = viewManager
        recyclerDocumentList.adapter = viewAdapter

        verifyStoragePermissions(this)
        startService(Intent(applicationContext, SyncService::class.java))
    }

    /**
     * Verify if we have the required permissions and request it if we don't
     */
    private fun verifyStoragePermissions(activity: Activity?) {
        // Check if we have write permission
        val permission = ActivityCompat.checkSelfPermission(activity!!, Manifest.permission.READ_EXTERNAL_STORAGE)
        if (permission != PackageManager.PERMISSION_GRANTED) {
            // We don't have permission so prompt the user
            ActivityCompat.requestPermissions(
                    activity,
                    PERMISSIONS_STORAGE,
                    REQUEST_EXTERNAL_STORAGE
            )
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        stopService(Intent(applicationContext, SyncService::class.java))
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        return when (item?.itemId) {
            android.R.id.home -> {
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    /**
     * Adapter for the RecyclerView that contains lease cards
     */
    class DocumentAdapter(private val myLeaseDocumentList: ArrayList<LeaseDocument>) :
            RecyclerView.Adapter<DocumentAdapter.DocumentViewHolder>() {

        class DocumentViewHolder(val view: View) : RecyclerView.ViewHolder(view) {
            fun updateUi(leaseDocument: LeaseDocument) {
                view.setOnClickListener {
                    if (leaseDocument.status.equals(ANALYZE_COMPLETED)) {
                        val intent = Intent(it.context, AnalyzeDocActivity::class.java)
                        intent.putExtra(DOCUMENT_KEY, leaseDocument.id)
                        view.context.startActivity(intent)
                    }
                }

                view.card_title.text = leaseDocument.title
                view.card_address.text = leaseDocument.address

                if (leaseDocument.status.equals(ANALYZE_COMPLETED)) {
                    if (leaseDocument.rent == 0) {
                        view.card_rent.text = view.context.getString(R.string.not_available)
                    } else {
                        view.card_rent.text = "$" + leaseDocument.rent.toString() + "/mo"
                    }
                    view.card_date.text = leaseDocument.date
                    val thumbnail = BitmapFactory.decodeByteArray(leaseDocument.thumbnail, 0, leaseDocument.thumbnail.size)
                    view.card_image.setImageBitmap(thumbnail)
                    view.card_image.scaleType = ImageView.ScaleType.FIT_XY
                    view.card_issues.visibility = View.VISIBLE
                    view.card_date.visibility = View.VISIBLE
                    view.card_title.visibility = View.VISIBLE
                } else {
                    view.card_rent.text = view.context.getString(R.string.processing_document)
                    view.card_address.text = leaseDocument.documentName
                    view.card_issues.visibility = View.INVISIBLE
                    view.card_date.visibility = View.INVISIBLE
                    view.card_title.visibility = View.INVISIBLE
                }

                val issueString : String = view.context.getString(R.string.issue_found)
                val issuesString : String = view.context.getString(R.string.issues_found)
                val numIssues : Int = leaseDocument.numIssues
                if (numIssues == 0) {
                    view.card_issues.text = "No " + issuesString
                    view.card_issues.backgroundTintList = ContextCompat.getColorStateList(view.context, R.color.darkgreen)
                } else {
                    view.card_issues.text = if (numIssues == 1) numIssues.toString() + " " + issueString else numIssues.toString() + " " + issuesString
                    view.card_issues.backgroundTintList = ContextCompat.getColorStateList(view.context, R.color.watchoutred)
                }
            }
        }

        fun addLeaseDocument(document : LeaseDocument) {
            myLeaseDocumentList.add(document)
            notifyDataSetChanged()
        }

        // Create new views (invoked by the layout manager)
        override fun onCreateViewHolder(parent: ViewGroup,
                                        viewType: Int): DocumentViewHolder {
            // create a new view
            val view = LayoutInflater.from(parent.context)
                    .inflate(R.layout.card_document, parent, false) as View
            return DocumentViewHolder(view)
        }

        // Replace the contents of a view (invoked by the layout manager)
        override fun onBindViewHolder(holder: DocumentViewHolder, position: Int) {

            // - get element from your dataset at this position
            // - replace the contents of the view with that element
            holder.updateUi(myLeaseDocumentList.get(position))
        }

        // Return the size of your dataset (invoked by the layout manager)
        override fun getItemCount() = myLeaseDocumentList.size
    }

    override fun getViewModel(): SafeRentActivityViewModel {
        return safeRentViewModel
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == RESULT_OK) {
            if (requestCode == PHOTO_CODE) {
                Toast.makeText(this, "Photo Taken", Toast.LENGTH_SHORT).show()
            } else if (requestCode == PDF_CODE) {
                val uri: Uri? = data?.data
                val file = File(uri?.path) //create path from uri
                safeRentViewModel.onFileSelected(file.toUri())
            }
        }
    }
}