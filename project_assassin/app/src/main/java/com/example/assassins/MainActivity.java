package com.example.assassins;

import android.Manifest;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.media.ExifInterface;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.VideoView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;
import androidx.core.graphics.drawable.RoundedBitmapDrawable;
import androidx.core.graphics.drawable.RoundedBitmapDrawableFactory;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    ImageView photoViewer;
    VideoView videoViewer;
    TextView usernameDisplay;

    String photoPath;
    String username;

    public static final int PHOTO_REQUEST_CODE=0;
    public static final int VIDEO_REQUEST_CODE=1;

    String submitPhotoURL = "http://35.231.34.135:5000/api/submit/photo/";

    RequestQueue mainQueue;
    Bitmap currentPhoto;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Intent loginIntent = getIntent();
        username = loginIntent.getStringExtra(LoginActivity.LOGIN_NAME);

        usernameDisplay = findViewById(R.id.usernameDisplay);
        usernameDisplay.setText(username);

        mainQueue = Volley.newRequestQueue(this);

        photoViewer = findViewById(R.id.photo_viewer);
        videoViewer = findViewById(R.id.video_viewer);

        photoViewer.setVisibility(View.INVISIBLE);
        videoViewer.setVisibility(View.INVISIBLE);
        videoViewer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
            @Override
            public void onCompletion(MediaPlayer mediaPlayer) {
                videoViewer.start();
            }
        });

        if (Build.VERSION.SDK_INT >= 23) {
            requestPermissions(new String[]{Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE}, 2);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && requestCode == PHOTO_REQUEST_CODE) {
            Bitmap b = BitmapFactory.decodeFile(photoPath);
            currentPhoto = b;
            b = fixOrientation(b);
            RoundedBitmapDrawable rb = RoundedBitmapDrawableFactory.create(getResources(), b);
            rb.setCornerRadius(300.0f);
            rb.setAntiAlias(true);


            photoViewer.setImageDrawable(rb);
            videoViewer.stopPlayback();
            videoViewer.setVisibility(View.INVISIBLE);
            photoViewer.setVisibility(View.VISIBLE);
//            photoViewer.setImageBitmap(b);
        }
        else if (resultCode == RESULT_OK && requestCode == VIDEO_REQUEST_CODE) {
            Uri videoUri = data.getData();
            videoViewer.setVideoURI(videoUri);
            photoViewer.setVisibility(View.INVISIBLE);
            videoViewer.setVisibility(View.VISIBLE);
            videoViewer.start();
        }
    }

    public void openCamera(View view) {
        Intent takePhoto = new Intent("android.media.action.IMAGE_CAPTURE");
        if (takePhoto.resolveActivity(getPackageManager()) != null) { // just checks if there is an app to handle the intent, good practice
            File photoFile = null;
            photoFile = createPhotoPath();
            if (photoFile != null) {
                Uri photoURI = FileProvider.getUriForFile(MainActivity.this, "com.example.assassins.fileprovider", photoFile);
                takePhoto.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePhoto, PHOTO_REQUEST_CODE);
            }
        }
    }

    public void openVideo(View view) {
        Intent takeVideo = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
        if (takeVideo.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takeVideo, VIDEO_REQUEST_CODE);
        }
    }

    private File createPhotoPath() {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        File storageDir = this.getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = null;
        try {
            image = File.createTempFile(timeStamp, ".jpg", storageDir);
        } catch (IOException e) {
            e.printStackTrace();
        }
        photoPath = image.getAbsolutePath();
        return image;
    }

    private Bitmap fixOrientation(Bitmap b) {
        ExifInterface ei = null;
        try {
            ei = new ExifInterface(photoPath);
        }
        catch(IOException e) {
            e.printStackTrace();
        }

        int orientation = ei.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_UNDEFINED);
        switch(orientation)
        {
            case ExifInterface.ORIENTATION_ROTATE_90:
                return rotateImage(b, 90);

            case ExifInterface.ORIENTATION_ROTATE_180:
                return rotateImage(b, 180);

            case ExifInterface.ORIENTATION_ROTATE_270:
                return rotateImage(b, 270);

            case ExifInterface.ORIENTATION_NORMAL:
            default:
                return b;
        }
    }

    public static Bitmap rotateImage(Bitmap source, float angle) {
        Matrix matrix = new Matrix();
        matrix.postRotate(angle);
        return Bitmap.createBitmap(source, 0, 0, source.getWidth(), source.getHeight(),
                matrix, true);
    }

    public String getStringImage(Bitmap bmp) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] imageBytes = baos.toByteArray();
        String encodedImg = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImg;
    }

    public void submitPressed(View view) {
        Log.d("MainActivity", "submit pressed");
        sendSubmitPhotoRequest();
    }

    private void sendSubmitPhotoRequest() {
//        VolleyLog.DEBUG = true;
        Log.d("MainActivity", "beginning request");
        String imgString = getStringImage(currentPhoto);
        Log.d("MainActivity", "imgString");

        Map<String, String> params = new HashMap<String, String>();
        params.put("photo", imgString);
        JSONObject body = new JSONObject(params);

        JsonObjectRequest submitPhotoRequest = new JsonObjectRequest
                (Request.Method.POST, submitPhotoURL, body, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.d("MainActivity", "submit photo request response good");
                        try {
                            boolean valid = response.getBoolean("success");
                            if (valid) {
                                Log.d("MainActivity", response.toString());
                                Log.d("MainActivity", "submit photo successful");
                            }
                            else {
                                Log.d("MainActivity", "submit photo unsuccessful");
                            }
                        } catch (JSONException e) {
                            Log.d("MainActivity", "Error accessing key from submit photo request.");
                            Log.d("MainActivity", e.getStackTrace().toString());
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("MainActivity", "submit photo request failed");
                        Log.d("MainActivity", error.getMessage());
                    }
                });
        mainQueue.add(submitPhotoRequest);
    }

}
