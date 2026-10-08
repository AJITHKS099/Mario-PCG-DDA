import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import engine.core.MarioGame;
import engine.core.MarioResult;
import agents.robinBaumgarten.Agent;

public class PlayLevel {

    // Explanation: Reads and returns the complete text content of a Mario level file from the given file path.
    public static String getLevel(String filepath) {
        try {
            return new String(Files.readAllBytes(Paths.get(filepath)));
        } catch (IOException e) {
            System.err.println("Failed to read file at: " + Paths.get(filepath).toAbsolutePath());
            e.printStackTrace();
            return null;
        }
    }

    // Explanation: Main execution entry point that parses CLI arguments and runs automated AI validation or interactive human play.
    public static void main(String[] args) {
        String levelPath = (args.length > 0) ? args[0] : "levels/level_0.txt";
        String mode = (args.length > 1) ? args[1] : "play";
        
        int levelType = (args.length > 2) ? Integer.parseInt(args[2]) : 0;
        int marioState = (args.length > 3) ? Integer.parseInt(args[3]) : 0; 
        int lives = (args.length > 4) ? Integer.parseInt(args[4]) : 3;
        int coins = (args.length > 5) ? Integer.parseInt(args[5]) : 0;

        String levelContent = getLevel(levelPath);
        if (levelContent == null || levelContent.trim().isEmpty()) {
            System.err.println("Error: Level content is empty or file not found.");
            System.exit(1);
        }

        MarioGame game = new MarioGame();

        if ("validate".equalsIgnoreCase(mode)) {
            // Background validation (Fast)
            MarioResult result = game.runGame(new Agent(), levelContent, 200, levelType, false, marioState);
            boolean won = result.getCompletionPercentage() >= 0.85 || "WIN".equalsIgnoreCase(result.getGameStatus().toString());
            
            if (won) {
                System.out.println("RESULT:WIN:STATE=" + result.getMarioMode() + ":COINS=" + result.getCurrentCoins());
            } else {
                System.out.println("RESULT:LOSE:STATE=0:COINS=" + result.getCurrentCoins());
            }
            System.exit(0);
            
        } else if ("validate_vis".equalsIgnoreCase(mode)) {
            // Visual AI agent playback with larger window (scale 3.5f)
            game.runGame(new Agent(), levelContent, 200, marioState, true, 30, 3.5f, lives, coins);
            System.exit(0);
            
        } else {
            // Interactive human playback with larger game window (scale 3.5f)
            MarioResult result = game.runGame(new agents.human.Agent(), levelContent, 200, marioState, true, 30, 3.5f, lives, coins);
            
            boolean won = "WIN".equalsIgnoreCase(result.getGameStatus().toString()) || result.getCompletionPercentage() >= 0.85;
            int finalState = result.getMarioMode();
            int coinsGained = result.getCurrentCoins();
            int totalCoins = coins + coinsGained;
            
            int newLives = lives;
            if (!won) {
                newLives -= 1;
                finalState = 0;
            }
            if (newLives < 0) {
                newLives = 0;
            }
            
            if (totalCoins >= 100) {
                newLives += (totalCoins / 100);
                totalCoins = totalCoins % 100;
            }

            // Count total enemies present in level content
            int totalEnemies = 0;
            for (char c : levelContent.toCharArray()) {
                if (c == 'g' || c == 'k' || c == 'r' || c == 'T' || c == 'y') {
                    totalEnemies++;
                }
            }
            int kills = result.getKillsTotal();
            int hurts = result.getMarioNumHurts();
            int jumps = result.getNumJumps();

            String updateMsg = String.format(java.util.Locale.US,
                "SESSION_UPDATE:WON=%b:MODE=%d:LIVES=%d:COINS=%d:COMPLETION=%.2f:KILLS=%d:TOTAL_ENEMIES=%d:HURTS=%d:JUMPS=%d",
                won, finalState, newLives, totalCoins, result.getCompletionPercentage(), kills, totalEnemies, hurts, jumps
            );
            System.out.println(updateMsg);
            try {
                java.nio.file.Files.createDirectories(java.nio.file.Paths.get("levels"));
                java.nio.file.Files.write(java.nio.file.Paths.get("levels/last_result.txt"), updateMsg.getBytes());
            } catch (Exception e) {
                e.printStackTrace();
            }
            System.exit(0);
        }
    }
}