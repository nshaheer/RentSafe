package com.leaseguard.leaseguard.landing

import android.content.Intent
import android.content.res.Resources
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.MenuItem
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.leaseguard.leaseguard.BaseActivity
import com.leaseguard.leaseguard.R
import com.leaseguard.leaseguard.models.LeaseDocument
import kotlinx.android.synthetic.main.activity_saferent.*
import kotlinx.android.synthetic.main.card_document.view.*
import javax.inject.Inject


class SafeRentActivity : BaseActivity<SafeRentActivityViewModel>() {
    private val LIBRARY_CODE = 1
    private val ANALYZE_DOC_CODE = 2

    @Inject
    lateinit var safeRentViewModel : SafeRentActivityViewModel

    private lateinit var viewAdapter: RecyclerView.Adapter<*>
    private lateinit var viewManager: RecyclerView.LayoutManager

    private val leaseList : ArrayList<LeaseDocument> = ArrayList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_saferent)

        supportActionBar?.title = "RentSafe"
        supportActionBar?.setHomeAsUpIndicator(R.drawable.ic_menu)
        supportActionBar?.setDisplayShowHomeEnabled(true)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        floatingActionMenu.addItem("Library", R.drawable.ic_lib,
                View.OnClickListener {
                    val intent = Intent()
                            .setType("*/*")
                            .setAction(Intent.ACTION_GET_CONTENT)
                    startActivityForResult(Intent.createChooser(intent, "Select a file"), LIBRARY_CODE)
                })
        floatingActionMenu.addItem("Photo", R.drawable.ic_camera,
                View.OnClickListener {
                    // TODO: open camera
                })

        safeRentViewModel.startAnalyzeDocActivity.observe(this, Observer {
            val intent = Intent(this, AnalyzeDocActivity::class.java)
            startActivityForResult(intent, ANALYZE_DOC_CODE)
        })

        safeRentViewModel.documentUpdated.observe(this, Observer { documents ->
            leaseList.clear()
            leaseList.addAll(documents)
            Log.d("testdoc", documents.size.toString())
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
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        return when (item?.itemId) {
            android.R.id.home -> {
                // TODO: handle the menu button press
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    class DocumentAdapter(private val myLeaseDocumentList: ArrayList<LeaseDocument>) :
            RecyclerView.Adapter<DocumentAdapter.DocumentViewHolder>() {

        class DocumentViewHolder(val view: View) : RecyclerView.ViewHolder(view) {
            fun updateUi(leaseDocument: LeaseDocument) {
                view.card_title.text = leaseDocument.title
                view.card_address.text = leaseDocument.address
                view.card_rent.text = "$" + leaseDocument.rent.toString() + "/mo"
                view.card_date.text = leaseDocument.dateRange
                val issueString : String = view.context.getString(R.string.issues_found)
                if (leaseDocument.numIssues == 0) {
                    view.card_issues.text = "no " + issueString
                    view.card_issues.backgroundTintList = ContextCompat.getColorStateList(view.context, R.color.darkgreen)
                } else {
                    view.card_issues.text =  leaseDocument.numIssues.toString() + " " + issueString
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
                                        viewType: Int): DocumentAdapter.DocumentViewHolder {
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
            if (requestCode == LIBRARY_CODE) {
                val resultFile = data?.data
                safeRentViewModel.onFileSelected(resultFile)
            } else if (requestCode == ANALYZE_DOC_CODE) {
                safeRentViewModel.onReturned()
            }
        }
    }
}