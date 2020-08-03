package com.leaseguard.leaseguard.api;

import android.app.Service;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.Nullable;

import com.leaseguard.leaseguard.database.LeaseDao;
import com.leaseguard.leaseguard.database.LeaseRoomDatabase;
import com.leaseguard.leaseguard.models.ApiResponse;
import com.leaseguard.leaseguard.models.LeaseDocument;

import java.util.List;

import kotlin.coroutines.Continuation;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

// Polling Service for Analysis Completions
public class SyncService extends Service {
    private Handler handler;

    public static final long DEFAULT_SYNC_INTERVAL = 10 * 1000;

    private Runnable runnableService = new Runnable() {
        @Override
        public void run() {
            Log.d("POLLING", "STARTED");
            AnalysisService analysisService = AnalysisServiceBuilder.createService(AnalysisService.class);
            Call<ApiResponse> leaseDocs = analysisService.getLease();
            leaseDocs.enqueue(new Callback<ApiResponse>()
            {
                @Override
                public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response)
                {
                    if (response.isSuccessful())
                    {
                        ApiResponse apiResponse = response.body();
                        LeaseDao leaseDao = LeaseRoomDatabase.Companion.getDatabase(getApplicationContext()).leaseDao();
                        leaseDao.deleteLoadingLease();
                        //leaseDao.insert(apiResponse);
                        Log.d("POLLING", response.body().lease.toString());
                        //API response
                        System.out.println(apiResponse.toString());
                    }
                    else
                    {
                        Log.d("POLLING", "FAILED");
                        System.out.println("Request Error :: " + response.errorBody());
                    }
                }

                @Override
                public void onFailure(Call<ApiResponse> call, Throwable t)
                {
                    System.out.println("Network Error :: " + t.getLocalizedMessage());
                }
            });
            handler.postDelayed(runnableService, DEFAULT_SYNC_INTERVAL);
        }
    };

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        handler = new Handler();
        handler.post(runnableService);
        return START_STICKY;
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        handler.removeCallbacks(runnableService);
        stopSelf();
        super.onDestroy();
    }

}
