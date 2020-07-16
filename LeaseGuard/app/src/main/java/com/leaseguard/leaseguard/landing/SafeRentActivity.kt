package com.leaseguard.leaseguard.landing

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import androidx.lifecycle.Observer
import android.view.ViewGroup
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

    @Inject
    lateinit var safeRentViewModel : SafeRentActivityViewModel
    private lateinit var viewAdapter: RecyclerView.Adapter<*>
    private lateinit var viewManager: RecyclerView.LayoutManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_saferent)

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
            startActivity(intent)
        })

        val leaseList : ArrayList<LeaseDocument> = ArrayList();
        val leaseDocument : LeaseDocument = LeaseDocument("Luxe Waterloo", "333 King St. N", 600, "April 1, 2017 - August 31, 2017", 0)
        leaseList.add(leaseDocument)
        viewAdapter = DocumentAdapter(leaseList)
        viewManager = LinearLayoutManager(this)
        recyclerDocumentList.setHasFixedSize(true)
        recyclerDocumentList.layoutManager = viewManager
        recyclerDocumentList.adapter = viewAdapter
    }

    class DocumentAdapter(private val myLeaseDocumentList: ArrayList<LeaseDocument>) :
            RecyclerView.Adapter<DocumentAdapter.DocumentViewHolder>() {

        class DocumentViewHolder(val view: View) : RecyclerView.ViewHolder(view) {
            fun updateUi(leaseDocument: LeaseDocument) {
                view.card_title.text = leaseDocument.title
                view.card_address.text = leaseDocument.address
                view.card_rent.text = "$" + leaseDocument.rent.toString() + "/mo"
                view.card_date.text = leaseDocument.dateRange
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
        if (requestCode == LIBRARY_CODE && resultCode == RESULT_OK) {
            val resultFile = data?.data
            safeRentViewModel.onFileSelected(resultFile)
        }
    }
}