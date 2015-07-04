package com.example.hubert.ieos;

/**
 * Created by hubert on 2015/5/23.
 */
import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.Window;
import android.view.WindowManager;
import com.example.hubert.ieos.MjpegInputStream;
import com.example.hubert.ieos.MjpegView;

public class StreamingActivity extends Activity {
	String URL = "http://140.112.42.154:2016/";
    private MjpegView mv;
    private static final int MENU_QUIT = 1;

    /* Creates the menu items */
    public boolean onCreateOptionsMenu(Menu menu) {
        menu.add(0, MENU_QUIT, 0, "Quit");
        return true;
    }

    /* Handles item selections */
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case MENU_QUIT:
                finish();
                return true;
        }
        return false;
    }

    public void onCreate(Bundle icicle) {
        super.onCreate(icicle);
        //sample public cam
		 requestWindowFeature(Window.FEATURE_NO_TITLE);
         getWindow().setFlags(WindowManager.LayoutParams.FLAG_FORCE_NOT_FULLSCREEN, WindowManager.LayoutParams.FLAG_FORCE_NOT_FULLSCREEN);
         mv = new MjpegView(this);
         setContentView(mv);
        MjpegSampleTask mjpegsample = new  MjpegSampleTask();
        mjpegsample.execute();
    }

    public void onPause() {
        super.onPause();
        mv.stopPlayback();
    }

    private class MjpegSampleTask extends AsyncTask<Object, Integer, Long> {
        protected Long doInBackground(Object... abc) {         
            mv.setSource(MjpegInputStream.read(URL));
            mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
            mv.showFps(false);
            return null;
        }
    }
}
