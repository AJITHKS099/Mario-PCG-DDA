package engine.helper;

public enum MarioActions {
    LEFT(0, "Left"),
    RIGHT(1, "Right"),
    DOWN(2, "Down"),
    SPEED(3, "Speed"),
    JUMP(4, "Jump");

    private int value;
    private String name;

    MarioActions(int newValue, String newName) {
        value = newValue;
        name = newName;
    }

    // Explanation: Returns the current value value.
    public int getValue() {
        return value;
    }

    // Explanation: Returns the current string value.
    public String getString() {
        return name;
    }

    // Explanation: Executes the number of actions routine on MarioActions.
    public static int numberOfActions() {
        return MarioActions.values().length;
    }

    // Explanation: Returns the current action value.
    public static MarioActions getAction(int value) {
        return MarioActions.values()[value];
    }
}
