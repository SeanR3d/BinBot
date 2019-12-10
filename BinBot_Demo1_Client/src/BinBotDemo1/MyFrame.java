package BinBotDemo1;

import BinBotDemo1.connections.ServerConnection;
import BinBotDemo1.instructions.Instruction;
import BinBotDemo1.instructions.Status;
import org.opencv.core.Core;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.IOException;

/**
 * JFrame class to display video feed including the bounding boxes of the object detector results. Using the
 * VideoCap class, the instance's thread captures a BufferedImage which is sent to the processing server. The server
 * will return the BufferedImage with the resulting bounding boxes.
 *
 * @author Sean Reddington
 * @version 1.0
 * @since 2019-10-25
 */
public class MyFrame extends JFrame {

    // Loading the OpenCV core library
    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    private JPanel contentPane;
    private VideoCap videoCap = new VideoCap();

    static final String IP = "127.0.0.1";
    static final int PORT = 7001;

    static ServerConnection connection;

    /**
     * Main class to run the client portion of team BinBot's first demo. Establishes a connection to the BinBot server,
     * then begins the live feed object detection within a JFrame.
     *
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    public static void main(String[] args) throws IOException {
        setup();
        EventQueue.invokeLater(() -> {

            try {
                MyFrame frame = new MyFrame();
                frame.setVisible(true);
            } catch (Exception e) {
                e.printStackTrace();
            }

        });

    }

    /**
     * Configures JPanel for video feed display and starts thread.
     *
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    public MyFrame() {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setBounds(0, 0, 1280, 720);
        contentPane = new JPanel();
        contentPane.setBorder(new EmptyBorder(0, 0, 0, 0));
        setContentPane(contentPane);
        contentPane.setLayout(null);

        new MyThread().start();

    }

    /**
     * Configures connection to the BinBot processing server via the ServerConnection class.
     *
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    public static void setup() throws IOException {
        System.out.println("Connecting to " + IP + " " + PORT + "...");
        connection = new ServerConnection(IP, PORT);
        System.out.println("Connection established!");
    }

    /**
     * Sends the passed BufferedImage to the BinBot processing server via the ServerConnection instance.
     *
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    public static void sendCapture(BufferedImage image) {
        Instruction imgSend = new Instruction(Status.NAVIGATE, image, null, null);
//        System.out.print("Sending: " + imgSend.json());
        System.out.print("Sending image to server..");
        try {
            connection.send(imgSend.json());
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("Sent");
    }

    /**
     * Receives a BufferedImage from the BinBot processing server via the ServerConnection instance.
     *
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    public static BufferedImage receiveCapture() {
        System.out.println("Attempting to receive");
        String jsonReceive = null;
        try {
            jsonReceive = connection.receive();
        } catch (IOException e) {
            e.printStackTrace();
        }
//        System.out.println("received: " + jsonReceive);
        System.out.println("received image from server");
        Instruction imgReceive = new Instruction(jsonReceive);
        return imgReceive.img();
    }

    /**
     * Captures a BufferedImage from the video feed and sends it to the BinBot processing server. The server will send
     * a modified BufferedImage containing bounding boxes of any object detected from the machine learning model.
     *
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    @Override
    public void paint(Graphics g) {
        g = contentPane.getGraphics();
        BufferedImage image = videoCap.getOneFrame(); // Capture a frame to send to server
        sendCapture(image); // Send the BufferedImage to the server
        image = receiveCapture(); // Receive the modified BufferedImage back from the server
        g.drawImage(image, 0, 0, this); // Draw the new image to the JFrame
    }

    /**
     * Thread class to handle the JFrame
     *
     * @author Sean Reddington
     * @version 1.0
     * @since 2019-10-25
     */
    class MyThread extends Thread {
        @Override
        public void run() {
            for (; ; ) {
                repaint();
                try {
                    Thread.sleep(30);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
