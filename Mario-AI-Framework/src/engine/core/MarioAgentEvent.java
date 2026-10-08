package engine.core;

public class MarioAgentEvent {
    private boolean[] actions;
    private float marioX;
    private float marioY;
    private int marioState;
    private boolean marioOnGround;
    private int time;

    // Explanation: Constructs and initializes a new MarioAgentEvent instance with specified parameters.
    public MarioAgentEvent(boolean[] actions, float marioX, float marioY, int marioState, boolean marioOnGround, int time) {
        this.actions = actions;
        this.marioX = marioX;
        this.marioY = marioY;
        this.marioState = marioState;
        this.marioOnGround = marioOnGround;
        this.time = time;
    }

    // Explanation: Evaluates current world state and returns boolean button action array for Mario controller.
    public boolean[] getActions() {
        return this.actions;
    }

    // Explanation: Returns the current mario x value.
    public float getMarioX() {
        return this.marioX;
    }

    // Explanation: Returns the current mario y value.
    public float getMarioY() {
        return this.marioY;
    }

    // Explanation: Returns the current mario state value.
    public int getMarioState() {
        return this.marioState;
    }

    // Explanation: Returns the current mario on ground value.
    public boolean getMarioOnGround() {
        return this.marioOnGround;
    }

    // Explanation: Returns the current time value.
    public int getTime() {
        return this.time;
    }
}
