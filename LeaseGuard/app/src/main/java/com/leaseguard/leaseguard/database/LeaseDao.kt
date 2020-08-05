package com.leaseguard.leaseguard.database

import androidx.lifecycle.LiveData
import androidx.room.*
import com.leaseguard.leaseguard.models.LeaseDocument

/**
 * Data Access Object for lease_table queries
 */
@Dao
interface LeaseDao {
    @Query("SELECT * from lease_table ORDER BY id ASC")
    fun getLeases(): LiveData<List<LeaseDocument>>

    @Query("SELECT * from lease_table WHERE status!='COMPLETED' ORDER BY id ASC")
    fun getLoadingLeases(): LiveData<List<LeaseDocument>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(leaseDocument: LeaseDocument)

    @Delete
    suspend fun delete(leaseDocument: LeaseDocument)

    @Update(onConflict = OnConflictStrategy.REPLACE)
   fun update(leaseDocument: LeaseDocument)

    @Query("DELETE from lease_table WHERE status!='COMPLETED'")
    fun deleteLoadingLease()

    @Query("DELETE FROM lease_table")
    suspend fun deleteAll()
}