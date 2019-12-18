package com.example.assassins;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends AppCompatActivity {
    public static final String LOGIN_NAME = "login_name";
    String rootURL = "http://35.231.34.135:5000/";
    String loginURL = "http://35.231.34.135:5000/api/user/login/";

    EditText loginField;
    TextView loginInfo;
    RequestQueue queue;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Intent intent = getIntent();
        loginField = findViewById(R.id.usernameField);
        loginInfo = findViewById(R.id.loginInfoText);
        queue = Volley.newRequestQueue(this);
    }

    private void launch_main() {
        String name = loginField.getText().toString();
        Intent loginIntent = new Intent(this, MainActivity.class);
        loginIntent.putExtra(LOGIN_NAME, name);
        setResult(RESULT_OK, loginIntent);
        startActivity(loginIntent);
    }

    public void login(View view) {
//        String name = loginField.getText().toString();
//        Intent loginIntent = new Intent(this, MainActivity.class);
//        loginIntent.putExtra(LOGIN_NAME, name);
//        setResult(RESULT_OK, loginIntent);
//        startActivity(loginIntent);
        hideKeyboard(this);
        loginInfo.setText("logging in");
        loginRequest();
//        loginInfo.setText(loginInfo.getText() + " done!");
    }

    private void loginRequest() {
//        VolleyLog.DEBUG = true;
        Map<String, String> params = new HashMap<String, String>();
        params.put("name", loginField.getText().toString());
        JSONObject body = new JSONObject(params);

        JsonObjectRequest loginRequest = new JsonObjectRequest
                (Request.Method.POST, loginURL, body, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.d("LoginActivity", "login request response good");
                        try {
                            boolean valid = response.getBoolean("success");
                            if (valid) {
                                Log.d("LoginActivity", "login successful");
                                launch_main();
                            }
                            else {
                                Log.d("LoginActivity", "login unsuccessful");
                                loginInfo.setText("Username not found");
                            }
                        } catch (JSONException e) {
                            Log.d("LoginActivity", "Error accessing key from login request.");
                            Log.d("LoginActivity", e.getStackTrace().toString());
                            loginInfo.setText("The request did not return the expected key.");
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("LoginActivity", "login request failed");
                        Log.d("LoginActivity", error.getMessage());
                        loginInfo.setText("There was an issue reaching the server");
                    }
                });
        queue.add(loginRequest);
    }

    public static void hideKeyboard(Activity activity) {
        InputMethodManager imm = (InputMethodManager) activity.getSystemService(Activity.INPUT_METHOD_SERVICE);
        View view = activity.getCurrentFocus();
        if (view == null) {
            view = new View(activity);
        }
        imm.hideSoftInputFromWindow(view.getWindowToken(), 0);
    }

    public void createUser(View view) {
    }
}
