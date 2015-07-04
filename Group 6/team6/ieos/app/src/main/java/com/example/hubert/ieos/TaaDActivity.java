package com.example.hubert.ieos;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.os.AsyncTask;

public class TaaDActivity extends ActionBarActivity {
    private TextView txtSpeechResult;
    private TextView txtServerResult;
    private String speechResult;
    private Button btnStreaming;
    private Button btnSpeechRecognition;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_taad);

        setupViewComponent();
        showResult();
    }

    private Button.OnClickListener btnStreamingOnClick = new Button.OnClickListener(){
        public void onClick(View v){
            Intent intent = new Intent();
            intent.setClass(TaaDActivity.this, StreamingActivity.class);
            startActivity(intent);
        }
    };

    private Button.OnClickListener btnSpeechRecognitionOnClick = new Button.OnClickListener(){
        public void onClick(View v){
            Intent intent = new Intent();
            intent.setClass(TaaDActivity.this, SpeechActivity.class);
            startActivity(intent);
        }
    };

    private void setupViewComponent() {
        txtSpeechResult = (TextView) findViewById(R.id.txtSpeechResult);
        txtServerResult = (TextView) findViewById(R.id.txtServerResult);
        btnStreaming = (Button) findViewById(R.id.btnStreaming);
        btnSpeechRecognition = (Button) findViewById(R.id.btnSpeechRecognition);

        btnStreaming.setOnClickListener(btnStreamingOnClick);
        btnSpeechRecognition.setOnClickListener(btnSpeechRecognitionOnClick);
    }

    private void showResult() {
        Bundle bundle = getIntent().getExtras();
        String speechresult = bundle.getString("speechresult");
        String serverresult = bundle.getString("serverresult");
        txtSpeechResult.setText(speechresult);
        txtServerResult.setText(serverresult);
    }
    }


