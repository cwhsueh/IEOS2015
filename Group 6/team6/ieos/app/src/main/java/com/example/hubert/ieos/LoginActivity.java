package com.example.hubert.ieos;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.*;
import android.view.View;

import org.apache.http.Header;
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

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.cookie.Cookie;


public class LoginActivity extends  ActionBarActivity {

    private Button btnLoginServer;
    private EditText edtUsername, edtPassword;
    private TextView txtResult;

    public String httpResponseResult;
    public String temp1;
    public String[] cookie;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        setupViewComponent();
    }

    private Button.OnClickListener btnLoginServerOnClick = new Button.OnClickListener(){
        public void onClick(View v){
            String strUsername = edtUsername.getText().toString();
            String strPassword = edtPassword.getText().toString();

            SendResultTask sendResultTask = new SendResultTask(strUsername, strPassword);
            sendResultTask.execute();
        }
    };

    private void setupViewComponent(){
        btnLoginServer = (Button) findViewById(R.id.btnLoginServer);
        edtUsername = (EditText) findViewById(R.id.edtUsername);
        edtPassword = (EditText) findViewById(R.id.edtPassword);
        txtResult = (TextView) findViewById((R.id.txtResult));

        btnLoginServer.setOnClickListener(btnLoginServerOnClick);
    }

    private class SendResultTask extends AsyncTask<Object, Integer, Long>
    {
        private String username;
        private String password;
        public SendResultTask(
                String username,
                String password
        ){
            this.username = username;
            this.password = password;
        }

        protected Long doInBackground(Object... abc)
        {
            HttpClient httpClient = new DefaultHttpClient();
            // replace with your url
            HttpPost httpPost = new HttpPost("http://140.112.42.149:8080/mobelogin");

            //Post Data
            List<NameValuePair> nameValuePair = new ArrayList<NameValuePair>(2);
            nameValuePair.add(new BasicNameValuePair("name", username));
            nameValuePair.add(new BasicNameValuePair("password", password));
            Log.d("Http Post Response:", username);
            Log.d("Http Post Response:", password);
            //Encoding POST data
            try {
                httpPost.setEntity(new UrlEncodedFormEntity(nameValuePair));
            } catch (UnsupportedEncodingException e) {
                // log exception
                e.printStackTrace();
            }

            //making POST request.
            try {
                HttpResponse response = httpClient.execute(httpPost);
                HttpEntity entity = response.getEntity();
                //get hheader
                Header[] temp = response.getHeaders("set-cookie");

                for(Header header : temp){
                    Log.d("Http response header:", header.getValue());
                    temp1 = header.getValue();
                }
                cookie = temp1.split(";");
                Log.d("split cookie:", cookie[0]);
                String result = EntityUtils.toString(entity);
                // write response to log
                Log.d("Http Post Response:", result);
                //JSON
                httpResponseResult = new JSONObject(result).getString("msg");
            } catch (ClientProtocolException e) {
                // Log exception
                e.printStackTrace();
            } catch (IOException e) {
                // Log exception
                e.printStackTrace();
            } catch (org.json.JSONException e){

            }
            return null;
        }

        protected void onProgressUpdate(Integer... progress)
        {

        }

        protected void onPostExecute(Long result)
        {
            Bundle bundle = new Bundle();
            bundle.putString("cookie", temp1);

            Log.d("httpResponseResult:", httpResponseResult);
            if(httpResponseResult.equals("login successful")){
                Intent intent = new Intent();
                intent.setClass(LoginActivity.this, SpeechActivity.class);
                intent.putExtras(bundle);
                startActivity(intent);
            }
            else if(httpResponseResult.equals("login unsuccessful")){
                txtResult.setText("The email and password you entered don't match.");
            }
            else if(httpResponseResult == null ){
                Intent intent = new Intent();
                intent.setClass(LoginActivity.this, SpeechActivity.class);
                intent.putExtras(bundle);
                startActivity(intent);
            }
            else
                //txtResult.setText("error");
                txtResult.setText(httpResponseResult);
        }
    }
}
