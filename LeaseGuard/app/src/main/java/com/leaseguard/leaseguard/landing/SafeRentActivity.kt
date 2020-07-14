package com.leaseguard.leaseguard.landing

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
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

    @Inject
    lateinit var safeRentViewModel : SafeRentActivityViewModel
    private lateinit var viewAdapter: RecyclerView.Adapter<*>
    private lateinit var viewManager: RecyclerView.LayoutManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_saferent)
        floatingActionMenu.addItem("Google Drive", R.drawable.ic_folder,
                View.OnClickListener {
                    // TODO: open drive
                })
        floatingActionMenu.addItem("PDF", R.drawable.ic_pdf,
                View.OnClickListener {
                    // TODO: open pdf
                })
        floatingActionMenu.addItem("Library", R.drawable.ic_lib,
                View.OnClickListener {
                    // TODO: open library
                })
        floatingActionMenu.addItem("Photo", R.drawable.ic_camera,
                View.OnClickListener {
                    // TODO: open camera
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
}