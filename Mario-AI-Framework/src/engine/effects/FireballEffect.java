package engine.effects;

import java.awt.Graphics;

import engine.core.MarioEffect;

public class FireballEffect extends MarioEffect {
    // Explanation: Constructs and initializes a new FireballEffect instance with specified parameters.
    public FireballEffect(float x, float y) {
        super(x, y, 0, 0, 0, 0, 32, 8);
    }

    // Explanation: Renders the visual graphics for this FireballEffect onto the target display canvas.
    @Override
    public void render(Graphics og, float cameraX, float cameraY) {
        this.graphics.index = this.startingIndex + (8 - this.life);
        super.render(og, cameraX, cameraY);
    }
}
