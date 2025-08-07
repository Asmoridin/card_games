import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import java.util.ArrayList;

public class WheelOfTime {
    public static void main (String args[]) {
        Path filePath = new File("card_games/W/Wheel_of_Time_CCG/Data/Wheel of Time Data.txt").toPath();
        List<String> input_lines = new ArrayList<>();
        try {
            input_lines = Files.readAllLines(filePath);
        } catch (Exception e) {
            System.out.println("Error occured: "
                               + e.getMessage());
            System.exit(0);
        }
        System.out.println(input_lines.get(0));
    }
}