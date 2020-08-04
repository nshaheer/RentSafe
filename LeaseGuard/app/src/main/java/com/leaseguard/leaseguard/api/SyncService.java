package com.leaseguard.leaseguard.api;

import android.app.Application;
import android.app.Service;
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
import com.leaseguard.leaseguard.landing.SafeRentActivity;
import com.leaseguard.leaseguard.models.ApiResponse;
import com.leaseguard.leaseguard.models.LeaseDocument;

import java.util.List;

import kotlin.coroutines.Continuation;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

// Polling Service for Analysis Completions
public class SyncService extends LifecycleService {
    // Polling every 20 seconds
    public static final long DEFAULT_SYNC_INTERVAL = 60 * 1000;
    private static final String ANALYZE_COMPLETED = "COMPLETED";
    private Handler handler;
    private LeaseDao leaseDao;
    private Call<ApiResponse> leaseCheck;
    private Runnable getLeaseCompletion = new Runnable() {
        @Override
        public void run() {
            leaseCheck.clone().enqueue(new Callback<ApiResponse>() {

                @Override
                public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                    if (response.isSuccessful()) {
                        Log.d("POLLING", response.body().lease.toString());
                        JsonObject jsonObject = response.body().lease;
                        Log.d("LEASE-RESPONSE", jsonObject.toString());
                        if (ANALYZE_COMPLETED.equals(jsonObject.get("Status").getAsString())) {
                            Log.d("LEASE-RESPONSE", "COMPLETED");
                            String thumbnail = jsonObject.get("Thumbnail").toString();
                            // b' has to be removed from the string prior to the encoding
                            if (thumbnail.length() > 2) {
                                thumbnail = thumbnail.substring(2, thumbnail.length() - 1);
                            }

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
                    System.out.println("Network Error :: " + t.getLocalizedMessage());
                }
            });
        }
    };

    private Runnable runnableService = new Runnable() {
        @Override
        public void run() {
            Log.d("POLLING", "STARTED");
            AnalysisService analysisService = AnalysisServiceBuilder.createService(AnalysisService.class);
            LiveData<List<LeaseDocument>> leases = leaseDao.getLoadingLeases();
            leases.observe(SyncService.this, new Observer<List<LeaseDocument>>() {
                @Override
                public void onChanged(@Nullable List<LeaseDocument> leases) {
                    Log.d("POLLING", "OBSERVABLE");
                    if (leases != null) {
                        for (LeaseDocument lease : leases) {
                            Log.d("POLLING", lease.getId());
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
