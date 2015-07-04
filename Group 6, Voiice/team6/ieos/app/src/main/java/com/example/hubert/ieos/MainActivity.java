package com.example.hubert.ieos;

import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.*;
import android.view.View;

import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends ActionBarActivity {

    private Button btnLogin;
/*
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        setupViewComponent();
    }
*/
    //wait two second
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);

        final Intent localIntent = new Intent(this, LoginActivity.class);
        Timer timer = new Timer();
        TimerTask tast = new TimerTask() {
            @Override
            public void run() {
                startActivity(localIntent);
                MainActivity.this.finish();
            }
        };
        timer.schedule(tast, 1500);
    }

        private Button.OnClickListener btnLoginOnClick = new Button.OnClickListener(){
        public void onClick(View v){
            Intent intent = new Intent();
            intent.setClass(MainActivity.this, LoginActivity.class);
            startActivity(intent);
        }
    };

    private void setupViewComponent(){
        btnLogin = (Button) findViewById(R.id.btnLogin);

        btnLogin.setOnClickListener(btnLoginOnClick);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;

    }

    @Override
    public  boolean  onOptionsItemSelected(MenuItem item) {
        switch  (item.getItemId()) {
            case  R.id.action_compose:
                Toast.makeText( this ,  "Compose" , Toast.LENGTH_SHORT).show();
                return  true ;
            case  R.id.action_settings:
                Toast.makeText( this ,  "Settings" , Toast.LENGTH_SHORT).show();
                return  true ;
            default :
                return  super .onOptionsItemSelected(item);
        }
    }
}
