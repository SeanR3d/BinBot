package BinBotDemo1;

import BinBotDemo1.connections.ServerConnection;
import BinBotDemo1.instructions.Instruction;
import BinBotDemo1.instructions.Status;

import javax.imageio.ImageIO;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

/**
 * Class to test exchanging .jgp files between the client and server.
 *
 * @author Sean DiGirolamo
 * @version 1.0
 * @since 2019-10-25
 */
public class FileExchangeTest {

    static final String IP = "127.0.0.1";
    static final int PORT = 7001;

    static ServerConnection connection;

    public static void main(String[] args) throws IOException {
        serverTest();
    }

    public static void serverTest() throws IOException {
        String path = "C:/Users/Sean/Desktop/Client/";
        String receiveFilename = "received.jpg";
        System.out.println("Connecting to " + IP + " " + PORT + "...");
        connection = new ServerConnection(IP, PORT);
        System.out.println("Connection established!");

        System.out.println("Attempting to receive");
        String jsonReceive = connection.receive();
        System.out.println("received: " + jsonReceive);
        Instruction instrReceive = new Instruction(jsonReceive);
        System.out.println("Saving image at " + path + receiveFilename);
        ImageIO.write(instrReceive.img(), "jpg", new File(path + receiveFilename));
        System.out.println("saved!");

        BufferedImage img = ImageIO.read(new File(path + receiveFilename));
        Instruction instrSend = new Instruction(Status.NAVIGATE, img, null, null);
        System.out.print("Sending: " + instrSend.json());
        connection.send(instrSend.json());
        System.out.println("Sent");
    }
}