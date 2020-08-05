package com.leaseguard.leaseguard.api;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.IBinder;
import android.util.Base64;
import android.util.Log;

import androidx.annotation.Nullable;
import androidx.lifecycle.LifecycleService;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.Observer;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.leaseguard.leaseguard.database.LeaseDao;
import com.leaseguard.leaseguard.database.LeaseRoomDatabase;
import com.leaseguard.leaseguard.models.ApiResponse;
import com.leaseguard.leaseguard.models.LeaseDocument;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

/**
 * Polling Service for Analysis Completions, it will update the DocumentList LiveData and
 * SQLite database upon successful completion from the Analysis returned from Analysis Service
 */
public class SyncService extends LifecycleService {
    // Polling every 60 seconds
    public static final long DEFAULT_SYNC_INTERVAL = 60 * 1000;
    private static final String ANALYZE_COMPLETED = "COMPLETED";
    private Handler handler;
    private LeaseDao leaseDao;
    private Call<ApiResponse> leaseCheck;
    // Create a new runnable in charge of the actual API call to the Analysis Service asynchronously
    private Runnable getLeaseCompletion = new Runnable() {
        @Override
        public void run() {
            leaseCheck.clone().enqueue(new Callback<ApiResponse>() {
                // If response is successful parse the json result and store the result in SQLite
                @Override
                public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                    if (response.isSuccessful()) {
                        JsonObject jsonObject = response.body().lease;
                        if (ANALYZE_COMPLETED.equals(jsonObject.get("Status").getAsString())) {
                            Log.d("LEASE-RESPONSE", "COMPLETED");
                            String thumbnail = jsonObject.get("Thumbnail").toString();
                            // b' has to be removed from the string prior to the encoding
                            if (thumbnail.length() > 2) {
                                thumbnail = thumbnail.substring(2, thumbnail.length() - 1);
                            }
                            // Decode encoded thumbnail and store byte array in database
                            byte[] thumbnailByteArray = Base64.decode(thumbnail, Base64.DEFAULT);
                            JsonArray jsonArray = jsonObject.getAsJsonArray("Issues");
                            LeaseDocument document = new LeaseDocument(jsonObject.get("Id").getAsString(), jsonObject.get("Title").getAsString(),
                                    jsonObject.get("Address").getAsString(), jsonObject.get("Rent").getAsInt(), jsonObject.get("Dates").getAsString(),
                                    jsonArray.size(), jsonArray.toString(), jsonObject.get("Status").getAsString(), thumbnailByteArray, jsonObject.get("DocumentName").getAsString());
                            leaseDao.update(document);
                        }
                    } else {
                        Log.d("POLLING", "FAILED " + response.errorBody());
                    }
                }

                @Override
                public void onFailure(Call<ApiResponse> call, Throwable t) {
                    Log.d("POLLING", "FAILED" + t.getLocalizedMessage());
                }
            });
        }
    };

    // Runnable that will be started on a new thread to query for updates of incomplete analysis
    private Runnable runnableService = new Runnable() {
        @Override
        public void run() {
            AnalysisService analysisService = AnalysisServiceBuilder.createService(AnalysisService.class);
            // Because retrieving Loading Leases from the LeaseDao is asynchronous as it queries SQLite,
            // we utilize the observer to identify when the retrieval is complete
            LiveData<List<LeaseDocument>> leases = leaseDao.getLoadingLeases();
            leases.observe(SyncService.this, new Observer<List<LeaseDocument>>() {
                @Override
                public void onChanged(@Nullable List<LeaseDocument> leases) {
                    // If leases were able to be retrieved
                    if (leases != null) {
                        // For each loading lease, send a query to check for completion
                        for (LeaseDocument lease : leases) {
                            // Call analysis service to obtain anaylsis status of the lease
                            leaseCheck = analysisService.getLease(lease.getId());
                            AsyncTask.execute(getLeaseCompletion);
                        }
                    }
                }
            });
            handler.postDelayed(runnableService, DEFAULT_SYNC_INTERVAL);
        }
    };

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        leaseDao = LeaseRoomDatabase.Companion.getDatabase(getApplication()).leaseDao();
        super.onStartCommand(intent, flags, startId);
        handler = new Handler();
        handler.post(runnableService);
        return START_STICKY;
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        super.onBind(intent);
        return null;
    }

    @Override
    public void onDestroy() {
        stopSelf();
        super.onDestroy();
    }

}
