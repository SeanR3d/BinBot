package com.example.capstonework;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    static boolean key;
    Button start;
    Button stop;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        start = findViewById(R.id.start_button);
        stop = findViewById(R.id.stop_button);

        start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                boolean key = true;
                //executionWork();
                startThread(key);

            }
        });

        stop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //boolean key = false;
                stopThread(false);
            }
        });


    }

    private void stopThread(boolean b) {
        boolean stopKey = b;
        final String IP = "192.168.43.68";
        final int PORT = 7002;

        new Thread(new Runnable() {
            @Override
            public void run() {
                //create an instance of serverConnection and transmit to server
                ServerConnection serverConnection = null;
                try {
                    serverConnection = new ServerConnection(IP, PORT);
                    AppMessage appMessage = new AppMessage(false,null,-1,-1);
                    serverConnection.send(appMessage.json());
                    serverConnection.close();

                } catch (IOException e) {
                    e.printStackTrace();
                }


            }
        }).start();


    }


    static public void startThread(boolean key){
        final boolean newkey = key;
        final String IP = "192.168.43.68";
        final int PORT = 7002;
        new Thread(new Runnable() {
            @Override

            public void run() {
                    ServerConnection serverConnection;
                    AppMessage appMessage;
                    try {
                        serverConnection = new ServerConnection(IP, PORT);
                        appMessage = new AppMessage(newkey,null,-1,-1);
                        serverConnection.send(appMessage.json());
                        serverConnection.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
            }//end of run
        //end of new startThread
        }).start();




    }

    /*private void executionWork() {

        BackgroundWork backgroundWork= new BackgroundWork();
        backgroundWork.execute();
    }

    class BackgroundWork extends AsyncTask<Void, Void, Void>{

        @Override
        protected Void doInBackground(Void... voids) {
            final String IP = "192.168.56.1";
            final int PORT = 6000;


            Socket socket;
            PrintWriter printWriter;
            String str = "Start is Is Android 12";
            ServerConnection connection;
            try {
                connection = new ServerConnection(IP, PORT);
                connection.send(str);

            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }*/
}//end of MainActivity
