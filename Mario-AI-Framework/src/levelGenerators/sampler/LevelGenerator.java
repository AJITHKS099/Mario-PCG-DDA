package levelGenerators.sampler;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;
import java.util.Random;

import engine.core.MarioLevelGenerator;
import engine.core.MarioLevelModel;
import engine.core.MarioTimer;

public class LevelGenerator implements MarioLevelGenerator {
    private int sampleWidth = 10;
    private String folderName = "levels/original/";

    private Random rnd;

    // Explanation: Constructs and initializes a default instance of LevelGenerator.
    public LevelGenerator() {
        this("levels/original/", 10);
    }

    // Explanation: Constructs and initializes a new LevelGenerator instance with specified parameters.
    public LevelGenerator(String sampleFolder) {
        this(sampleFolder, 10);
    }

    // Explanation: Constructs and initializes a new LevelGenerator instance with specified parameters.
    public LevelGenerator(String sampleFolder, int sampleWidth) {
        this.sampleWidth = sampleWidth;
        this.folderName = sampleFolder;
    }

    // Explanation: Returns the current random level value.
    private String getRandomLevel() throws IOException {
        File[] listOfFiles = new File(folderName).listFiles();
        List<String> lines = Files.readAllLines(listOfFiles[rnd.nextInt(listOfFiles.length)].toPath());
        String result = "";
        for (int i = 0; i < lines.size(); i++) {
            result += lines.get(i) + "\n";
        }
        return result;
    }

    // Explanation: Returns the current generated level value.
    @Override
    public String getGeneratedLevel(MarioLevelModel model, MarioTimer timer) {
        rnd = new Random();
        model.clearMap();
        for (int i = 0; i < model.getWidth() / sampleWidth; i++) {
            try {
                model.copyFromString(i * sampleWidth, 0, i * sampleWidth, 0, sampleWidth, model.getHeight(), this.getRandomLevel());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return model.getMap();
    }

    // Explanation: Returns the current generator name value.
    @Override
    public String getGeneratorName() {
        return "SamplerLevelGenerator";
    }
}
