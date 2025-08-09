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

        // First, we need to parse and validate the input data. Do we just create card objects for this?

        // We then need to parse and validate the deck data, which almost certainly will go into a deck

        // Do a summary of my collection, give me purchase suggestion

        // Do analysis on decks, suggest purchases to flesh out decks.

        // Write all of this to both the screen and to an output file.
        
        // Write out a Python file that can be used by ccg_summary
    }
}