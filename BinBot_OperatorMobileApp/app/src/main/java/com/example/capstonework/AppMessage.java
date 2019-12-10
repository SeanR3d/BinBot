package com.example.capstonework;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.InputStream;


/**
 * This class is used to communicate between the BinBot mobile application and the server. It is used for both alerting
 * the Server to stop operation and for sending images to display to the app. It is sent as a json string in the format
 * {
 *     "poweredState":<Boolean>,
 *     "img":<String>,
 *      "height":<int>,
 *     "width":<width>
 * }
 * where poweredState is true when the system should continue operation and the img is a BufferedImage converted into
 * a string which will be displayed in the mobile application.
 *
 * @author Sean DiGirolamo
 * @since 2019-10-29
 */

public class AppMessage {

    private Boolean poweredState;
    private Bitmap img = null;
    private int height = -1;
    private int width = -1;

    /**
     * This constructor takes as input a json string. It assumes that the json is properly formatted in the proper
     * configuration and results in an AppMessage object based on the json string provided.
     *
     * @author Sean DiGirolamo
     * @since 2019-10-29
     */
    public AppMessage(String json) {
        JSONObject jsonObject;
        try {
            jsonObject = new JSONObject(json);
            this.poweredState = jsonObject.getBoolean("poweredState");
            this.height = jsonObject.getInt("height");
            this.width = jsonObject.getInt("width");
            this.img = this.stringToBitmap(jsonObject.getString("img"));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    /**
     * This method creates a new immutable AppMessage object based on the arguments provided.
     *
     * @author Sean DiGirolamo
     * @since 2019-10-29
     */
    public AppMessage(Boolean poweredState, Bitmap img, int height, int width) {
        this.poweredState = poweredState;
        this.img = img;
        if(img != null){
            this.height = img.getHeight();
            this.width = img.getWidth();
        }
        this.height = -1;
        this.width = -1;
    }

    /**
     * This method returns the AppMessage class a a json string which can be sent to the BinBot Mobile Application.
     *
     * @author Sean DiGirolamo
     * @since 2019-10-29
     */
    public String json() {
        StringBuilder retval = new StringBuilder("{\"poweredState\":")
                .append(this.poweredState.toString()).append(",")
                .append("\"img\":" + "\"");

        if (this.img != null) {
            retval.append(img);
        }

        retval.append("\",")
                .append("\"height\":").append(this.height).append(",")
                .append("\"width\":").append(this.width).append("}");

        return retval.toString();
    }

    /**
     * This method returns the value of the poweredState boolean contained within the AppMessage
     *
     * @author Sean DiGirolamo
     * @since 2019-10-29
     */
    public Boolean poweredState() {
        return this.poweredState;
    }

    /**
     * This method returns the Buffered img contained within the AppMessage
     *
     * @author Sean DiGirolamo
     * @since 2019-10-21
     */
    public Bitmap img() {
        return this.img;
    }

    private Bitmap stringToBitmap(String image){
        try{
            byte [] encodeByte= Base64.decode(image,Base64.DEFAULT);

            InputStream inputStream  = new ByteArrayInputStream(encodeByte);
            Bitmap bitmap  = BitmapFactory.decodeStream(inputStream);
            return bitmap;
        }catch(Exception e){
            e.getMessage();
            return null;
        }
    }


}
