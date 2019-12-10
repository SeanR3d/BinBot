package BinBotDemo1.instructions;

import org.json.JSONObject;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.*;


/**
 * The Instruction class represents a set of instructions that BinBot should follow in order to retrieve trash. It is
 * also capable of converting json string to this object and providing a json version of itself in the format of
 * {
 * "status":<"PATROL"|"NAVIGATION"|"RETRIEVAL">,
 * "img":<image as object>,
 * "treads:[
 * {
 * "angle":<Double>,
 * "distance":<Double>
 * }
 * ]
 * "arms":[
 * {
 * "angle":<Double>
 * }
 * ]
 * }
 * where status is BinBot's operating status, img holds a picture captured by BinBot's camera, treads is an array
 * containing pairs of angles it should turn and distances it should travel forward after turning,
 * and arms is an array of angles each joint should turn.
 *
 * @author Sean DiGirolamo
 * @since 2019-10-18
 */
public class Instruction {
    private Status status;
    private BufferedImage img;
    //	private List<Pair<Double, Double>> treads;
    private List<Map.Entry<Double, Double>> treads;
    private List<Double> arms;

    /**
     * This constructor takes as input a json string. It assumes that the json is properly formatted in the proper
     * configuration and results in an Instruction object based on the json string provided.
     *
     * @author Sean DiGirolamo
     * @since 2019-10-18
     */
    public Instruction(String json) {
        JSONObject jsonObject = new JSONObject(json);

        this.status = Status.valueOf(jsonObject.getString("status"));

        this.treads = new ArrayList<>();

        this.img = this.stringToBufferedImage(jsonObject.getString("img"));

        for (Object o : jsonObject.getJSONArray("treads")) {
            JSONObject jo = (JSONObject) o;
//			treads.add(new Pair<>(jo.getDouble("angle"), jo.getDouble("distance")));
            treads.add(new AbstractMap.SimpleEntry<>(jo.getDouble("angle"), jo.getDouble("distance")));
        }

        this.arms = new ArrayList<>();
        for (Object o : jsonObject.getJSONArray("arms")) {
            arms.add(((JSONObject) o).getDouble("angle"));
        }
    }

    /**
     * This constructor takes as input an object array generated by OpenCV. Contained in this array is data about where
     * waste has been located and if waste is in the image. Based on this data, instructions will be calculated for
     * Binbot to execute and placed inside the resulting Instruction object.
     *
     * @author Sean DiGirolamo
     * @since 2019-10-18
     */
    public Instruction(Object[][] o) {
        this.status = Status.PATROL;
        this.img = null;
        this.treads = new ArrayList<>();
//		this.treads.add(new Pair<>(0.0, 00.0));
        this.treads.add(new AbstractMap.SimpleEntry<>(0.0, 00.0));
        this.arms = new ArrayList<>();
        this.arms = new ArrayList<>();
        this.arms.add(0.0);
    }

    /**
     * This method returns the Instruction class a a json string which can be sent to the BinBot robot and interpreted
     * as a set of commands to follow in the format described above.
     *
     * @author Sean DiGirolamo
     * @since 2019-10-20
     */
    public String json() {
        String retval = "{\"status\":\"" + this.status.toString() + "\",";

        retval += "\"img\":" + "\"" + bufferedImageToString(img) + "\",";

        retval += "\"treads\":[";
        if (this.treads != null) {
            for (Map.Entry<Double, Double> pair : this.treads) {
                retval += "{\"angle\":" + pair.getKey() + ",";
                retval += "\"distance\":" + pair.getValue() + "}";
                if (pair != this.treads.get(this.treads.size() - 1)) {
                    retval += ",";
                }
            }
        }
        retval += "],";

        retval += "\"arms\":[";
        if (this.arms != null) {
            for (Double d : this.arms) {
                retval += "{\"angle\":" + d + "}";
                if (d != this.arms.get(this.arms.size() - 1)) {
                    retval += ",";
                }
            }
        }
        retval += "]}";

        return retval;
    }

    /**
     * This method creates a new Instruction object based on the arguments provided. This shouldn't really ever be used
     * outside of testing purposes, but it is here just in case.
     *
     * @author Sean DiGirolamo
     * @since 2019-10-23
     */
    public Instruction(Status status, BufferedImage img, List<Map.Entry<Double, Double>> treads, List<Double> arms) {
        this.status = status;
        this.img = img;
        this.treads = treads;
        this.arms = arms;
    }

    /**
     * This method returns the Buffered img contained within the Instruction
     *
     * @author Sean DiGirolamo
     * @since 2019-10-21
     */
    public BufferedImage img() {
        return this.img;
    }

    private BufferedImage stringToBufferedImage(String s) {
        BufferedImage retval = null;
        byte[] bytes = Base64.getDecoder().decode(s);
        try {
            retval = ImageIO.read(new ByteArrayInputStream(bytes));
        } catch (Exception e) {
            e.printStackTrace();
        }

        return retval;
    }

    private String bufferedImageToString(BufferedImage bi) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        try {
            ImageIO.write(bi, "jpg", out);
        } catch (Exception e) {
            e.printStackTrace();
        }
        byte[] byteArray = out.toByteArray();
        String retval = Base64.getEncoder().encodeToString(byteArray);
        return retval;

    }
}