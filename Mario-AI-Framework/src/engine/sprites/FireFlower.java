package engine.sprites;

import java.awt.Graphics;

import engine.core.MarioSprite;
import engine.graphics.MarioImage;
import engine.helper.Assets;
import engine.helper.EventType;
import engine.helper.SpriteType;

public class FireFlower extends MarioSprite {
    private MarioImage graphics;
    private int life;

    // Explanation: Constructs and initializes a new FireFlower instance with specified parameters.
    public FireFlower(boolean visuals, float x, float y) {
        super(x, y, SpriteType.FIRE_FLOWER);
        this.width = 4;
        this.height = 12;
        this.facing = 1;
        this.life = 0;
        if (visuals) {
            this.graphics = new MarioImage(Assets.items, 1);
            this.graphics.originX = 8;
            this.graphics.originY = 15;
            this.graphics.width = 16;
            this.graphics.height = 16;
        }
    }

    // Explanation: Creates and returns an independent duplicate of this FireFlower for forward simulation.
    @Override
    public MarioSprite clone() {
        FireFlower f = new FireFlower(false, x, y);
        f.xa = this.xa;
        f.ya = this.ya;
        f.initialCode = this.initialCode;
        f.width = this.width;
        f.height = this.height;
        f.facing = this.facing;
        f.life = this.life;
        return f;
    }

    // Explanation: Checks and resolves collision interactions between this entity and other active sprites.
    @Override
    public void collideCheck() {
        if (!this.alive) {
            return;
        }

        float xMarioD = world.mario.x - x;
        float yMarioD = world.mario.y - y;
        if (xMarioD > -16 && xMarioD < 16) {
            if (yMarioD > -height && yMarioD < world.mario.height) {
                world.addEvent(EventType.COLLECT, this.type.getValue());
                world.mario.getFlower();
                world.removeSprite(this);
            }
        }
    }

    // Explanation: Updates physics, animation, and state transitions for this FireFlower on each game tick.
    @Override
    public void update() {
        if (!this.alive) {
            return;
        }

        super.update();
        life++;
        if (life < 9) {
            this.y--;
            return;
        }
        if (this.graphics != null) {
            this.graphics.index = 1 + (this.life / 2) % 2;
        }
    }

    // Explanation: Renders the visual graphics for this FireFlower onto the target display canvas.
    @Override
    public void render(Graphics og) {
        super.render(og);
        this.graphics.render(og, (int) (this.x - this.world.cameraX), (int) (this.y - this.world.cameraY));
    }
}