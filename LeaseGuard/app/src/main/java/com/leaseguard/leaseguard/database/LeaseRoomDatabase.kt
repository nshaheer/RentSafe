package com.leaseguard.leaseguard.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.leaseguard.leaseguard.models.LeaseDocument

/**
 * Annotates class to be a Room Database for SQLite with a table (entity) of the LeaseDocument class
 */
@Database(entities = arrayOf(LeaseDocument::class), version = 3, exportSchema = false)
public abstract class LeaseRoomDatabase : RoomDatabase() {

   abstract fun leaseDao(): LeaseDao

   companion object {
        // Singleton prevents multiple instances of database opening at the
        // same time
        @Volatile
        private var INSTANCE: LeaseRoomDatabase? = null

       /**
        * Provide singleton database instance
        */
       fun getDatabase(context: Context): LeaseRoomDatabase {
            val tempInstance = INSTANCE
            if (tempInstance != null) {
                return tempInstance
            }
            synchronized(this) {
                val instance = Room.databaseBuilder(
                        context.applicationContext,
                        LeaseRoomDatabase::class.java,
                        "lease_database"
                    ).allowMainThreadQueries()
                        .fallbackToDestructiveMigration().build()
                INSTANCE = instance
                return instance
            }
        }
   }
}