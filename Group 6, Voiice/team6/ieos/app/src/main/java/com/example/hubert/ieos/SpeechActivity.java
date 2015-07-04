package com.example.hubert.ieos;

/**
 * Created by hubert on 2015/5/13.
 */

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;
import org.w3c.dom.Text;

public class SpeechActivity extends ActionBarActivity {
    protected static final int RESULT_SPEECH = 1;

    private ImageButton btnSpeak;
    private TextView txtText;
    public String speechResult;
    private Button btnSendData;
    private String httpResponseResult;
    private TextView txtSpeechResult;
    private TextView txtSpeech;
    private String webcamturnon = "turn on the webcam";
    private String webcamturnoff = "turn off the webcam";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_speech);

        txtText = (TextView) findViewById(R.id.txtText);
        btnSpeak = (ImageButton) findViewById(R.id.btnSpeak);
        btnSpeak.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                Intent intent = new Intent(
                        RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, "en-US");

                try {
                    startActivityForResult(intent, RESULT_SPEECH);
                    txtText.setText("");
                    setupViewComponent();
                } catch (ActivityNotFoundException a) {
                    Toast t = Toast.makeText(getApplicationContext(),
                            "Ops! Your device doesn't support Speech to Text",
                            Toast.LENGTH_SHORT);
                    t.show();
                }
            }
        });
    }

    private Button.OnClickListener btnSendDataOnClick = new Button.OnClickListener(){
        public void onClick(View v){
            SendResultTask sendResultTask = new SendResultTask(speechResult);
            sendResultTask.execute();
        }
    };
/*
    private Button.OnClickListener btnSendDataOnClick = new Button.OnClickListener(){
        public void onClick(View v){
            Intent intent = new Intent();
            intent.setClass(SpeechActivity.this, TaaDActivity.class);
            Bundle bundle = new Bundle();
            bundle.putString("speechResult", speechResult);
            intent.putExtras(bundle);
            startActivity(intent);
        }
    };
    */

    private void setupViewComponent(){
        btnSendData = (Button) findViewById(R.id.btnSendData);

        btnSendData.setOnClickListener(btnSendDataOnClick);
        txtSpeech = (TextView) findViewById(R.id.txtSpeech);
        txtSpeechResult = (TextView) findViewById(R.id.txtSpeechResult1);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode) {
            case RESULT_SPEECH: {
                if (resultCode == RESULT_OK && null != data) {
                    ArrayList<String> text = data
                            .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                    txtText.setText(text.get(0));
                    speechResult = text.get(0);
                }
                break;
            }
        }
    }

    private class SendResultTask extends AsyncTask<Object, Integer, Long>
    {
        private String speechresult;
        public SendResultTask(
                String speechresult
        ){
            this.speechresult = speechresult;
        }

        protected Long doInBackground(Object... abc)
        {
            HttpClient httpClient = new DefaultHttpClient();
            // replace with your url
            HttpPost httpPost = new HttpPost("http://140.112.42.149:8080/mobevoice");
            //get sid
            Bundle bundle = getIntent().getExtras();
            String cookie = bundle.getString("cookie");
            Log.d("hicookie", cookie);

            //Post Data
            List<NameValuePair> nameValuePair = new ArrayList<NameValuePair>(1);
            nameValuePair.add(new BasicNameValuePair("speechresult", speechresult));
            Log.d("Http Post Response:", speechresult);
            //Encoding POST data
            try {
                httpPost.setEntity(new UrlEncodedFormEntity(nameValuePair));
                httpPost.setHeader("cookie", cookie);
            } catch (UnsupportedEncodingException e) {
                // log exception
                e.printStackTrace();
            }

            //making POST request.
            try {
                HttpResponse response = httpClient.execute(httpPost);
                HttpEntity entity = response.getEntity();
                String result = EntityUtils.toString(entity);
                // write response to log
                Log.d("speech response:", result);
                //JSON
                httpResponseResult = new JSONObject(result).getString("msg");
            } catch (ClientProtocolException e) {
                // Log exception
                e.printStackTrace();
            } catch (IOException e) {
                // Log exception
                e.printStackTrace();
            }
            catch(org.json.JSONException e){
                e.printStackTrace();
            }
            return null;
        }

        protected void onProgressUpdate(Integer... progress)
        {

        }

        protected void onPostExecute(Long result)
        {
            Log.d("httpResponseResult:", httpResponseResult);
            Log.d("result:", speechresult);
            txtSpeech.setText(speechresult);
            if(speechresult.equals(webcamturnon)){
                Intent intent = new Intent();
                intent.setClass(SpeechActivity.this, StreamingActivity.class);
                txtSpeechResult.setText("Success");
                startActivity(intent);
            }
            else if(speechresult.equals(webcamturnoff)){
                txtSpeechResult.setText("Success");
            }
            else if(httpResponseResult.equals("Success ")){
                Intent intent = new Intent();
                intent.setClass(SpeechActivity.this, TaaDActivity.class);
                Bundle bundle = new Bundle();
                bundle.putString("speechresult", speechresult);
                bundle.putString("serverresult", httpResponseResult); 
                intent.putExtras(bundle);
                txtSpeech.setText(speechresult);
                startActivity(intent);
            }
            else if(httpResponseResult.equals("Unaccept command")){
                txtSpeechResult.setText(httpResponseResult);
            }
            else if(httpResponseResult == null ){
                txtSpeechResult.setText("error");
            }
            else
                txtSpeechResult.setText(httpResponseResult);
        }
    }
}