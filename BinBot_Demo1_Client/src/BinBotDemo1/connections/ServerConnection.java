package BinBotDemo1.connections;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

/**
 * The ServerConnection class represents the network connection between this client and the BinBot
 * Server. Its methods allow the client to connect to the server while the server is listening for connections, and then
 * to send data back and forth to the server.
 *
 * @author Sean DiGirolamo
 * @version 1.0
 * @since 2019-10-23
 */
public class ServerConnection {
    private Socket sock;

    /**
     * This constructor creates a ServerConnection object which can be used for initiating and communicating with
     * the BinBot Server. It takes the IP Address and port number that the client should connect to as arguments
     *
     * @author Sean DiGirolamo
     * @since 2019-10-23
     */
    public ServerConnection(String ipAddr, int port) throws IOException {
        InetAddress ip = InetAddress.getByName(ipAddr);
        sock = new Socket(ip, port);
    }

    /**
     * This method takes as input a string which will be sent over the socket to the server
     *
     * @author Sean DiGirolamo
     * @since 2019-10-23
     */
    public void send(String s) throws IOException {
        PrintWriter out = new PrintWriter(sock.getOutputStream(), true);
        out.println(s);
    }

    /**
     * This method instructs the client to wait to receive a string from the server. It returns the string received.
     *
     * @author Sean DiGirolamo
     * @since 2019-10-23
     */
    public String receive() throws IOException {
        String retval;
        InputStream is = sock.getInputStream();
        InputStreamReader isr = new InputStreamReader(is);
        BufferedReader br = new BufferedReader(isr);
        while (!br.ready()) {
        }
        retval = br.readLine();
        return retval;
    }
}
