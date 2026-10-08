package engine.effects;

import java.awt.Graphics;

import engine.core.MarioEffect;

public class DustEffect extends MarioEffect {
    // Explanation: Constructs and initializes a new DustEffect instance with specified parameters.
    public DustEffect(float x, float y) {
        super(x, y, (float) (Math.random() * 2 - 1), (float) Math.random() * -1, 0, 0, 8 + (int) (Math.random() * 2), 10 + (int) (Math.random() * 5));
    }

    // Explanation: Renders the visual graphics for this DustEffect onto the target display canvas.
    @Override
    public void render(Graphics og, float cameraX, float cameraY) {
        if (this.life > 10) {
            this.graphics.index = 7;
        } else {
            this.graphics.index = this.startingIndex + (10 - life) * 4 / 10;
        }
        super.render(og, cameraX, cameraY);
    }
}