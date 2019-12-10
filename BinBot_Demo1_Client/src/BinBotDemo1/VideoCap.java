package BinBotDemo1;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.videoio.VideoCapture;

import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import java.awt.image.WritableRaster;


/**
 * Class to record video feed from a connected device and capture individual frames as BufferedImages
 *
 * @author Sean Reddington
 * @version 1.0
 * @since 2019-10-25
 */
public class VideoCap {

    // Loading the OpenCV core library
    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    VideoCapture capture;
    Mat mat = new Mat();

    /**
     * Instantiates the VideoCapture class and opens the camera instance
     *
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    public VideoCap() {
        capture = new VideoCapture();
        capture.open(0);
    }

    /**
     * Attempts to capture a frame from the VideoCapture feed and converts it to a BufferedImage.
     *
     * @return BufferedImage or null on failure
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    public BufferedImage getOneFrame() {
        if (capture.isOpened()) {
            if (capture.read(this.mat)) { // Capture frame into mat
                //create a BufferedImage from the frame capture
                BufferedImage img = new BufferedImage(mat.width(), mat.height(), BufferedImage.TYPE_3BYTE_BGR);
                WritableRaster raster = img.getRaster();
                DataBufferByte dataBuffer = (DataBufferByte) raster.getDataBuffer();
                byte[] data = dataBuffer.getData();
                mat.get(0, 0, data);
                return img;
            } else {
                System.err.println("Failed to capture frame!");
                return null;
            }
        } else {
            System.err.println("Failed to capture frame -- video capture closed!");
            return null;
        }
    }
}
