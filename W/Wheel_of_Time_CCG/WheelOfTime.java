import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import java.util.ArrayList;

public class WheelOfTime {

    private static List<String> cardSets = List.of("Premier", "Dark Prophecies", "Children of the Dragon", "Cycles", "Promos");
    private static List<String> rarities = List.of("C", "U", "R", "P", "F");
    private static List<String> cardTypes = List.of("Character", "Starting Character", "Event", "Advantage", "Challenge", "Troop");
    private static List<String> factions = List.of("Aiel", "Andor", "Cairhien", "Dark One", "Dragon", "Children of the Light",
        "Aes Sedai", "Mercenary", "Tear", "Illian");
    public static void main (String args[]) {

        int TOTAL_OWN = 0;
        int TOTAL_MAX = 0;

        Path filePath = new File("card_games/W/Wheel_of_Time_CCG/Data/Wheel of Time Data.txt").toPath();
        List<String> input_lines = new ArrayList<>();
        try {
            input_lines = Files.readAllLines(filePath);
        } catch (Exception e) {
            System.out.println("Error occured: "
                               + e.getMessage());
            System.exit(0);
        }

        // First, we need to parse and validate the input data. Do we just create card objects for this?
        for (String line : input_lines) {
            int hashIndex = line.indexOf('#');
            if (hashIndex != -1) { // If '#' is found
                line = line.substring(0, hashIndex); // Return the substring before '#'
            }
            line = line.trim();

            String cardName = line.split(";")[0];

            // See if the set is valid
            String[] parts = line.split(";");
            String thisCardSet = parts[1];
            if (!cardSets.contains(thisCardSet)) {
                System.out.println("Invalid set: " + thisCardSet);
            }

            String thisCardType = parts[2];
            if (!cardTypes.contains(thisCardType)) {
                System.out.println("Invalid type: " + thisCardType);
            }

            String thisFaction = parts[3];
            if (!thisFaction.isEmpty() && !factions.contains(thisFaction)) {
                System.out.println("Invalid faction: " + thisFaction);
            }

            String thisRarity = parts[4];
            if (!rarities.contains(thisRarity)) {
                System.out.println("Invalid rarity: " + thisRarity);
            }

            int card_own = Integer.parseInt(parts[5]);
            TOTAL_OWN += card_own;

            int card_max = 3;
            if (thisCardType.equals("Starting Character")) {
                card_max = 1;
            }
            TOTAL_MAX += card_max;
        }
        System.out.println("Total owned: " + TOTAL_OWN);
        System.out.println("Total max: " + TOTAL_MAX);
        // We then need to parse and validate the deck data, which almost certainly will go into a deck

        // Do a summary of my collection, give me purchase suggestion

        // Do analysis on decks, suggest purchases to flesh out decks.

        // Write all of this to both the screen and to an output file.
        
        // Write out a Python file that can be used by ccg_summary
        String fileName = "card_games/W/Wheel_of_Time_CCG/wheel_of_time.py";
        String pythonCode = "#!/usr/bin/python3\n\n" +
            "\"\"\"\nInventory manager and collection suggestor for the Wheel of Time TCG\n\"\"\"\n" +
            "GAME_NAME = \"Wheel of Time\"\n\n" + 
            "TOTAL_MAX = " + TOTAL_MAX + "\n" +
            "TOTAL_OWN = " + TOTAL_OWN + "\n";

        try (FileWriter writer = new FileWriter(fileName)) {
            writer.write(pythonCode);
            System.out.println("Python module 'wheel_of_time.py' created successfully.");
        } catch (IOException e) {
            System.err.println("Error writing Python module: " + e.getMessage());
        }
    }
}