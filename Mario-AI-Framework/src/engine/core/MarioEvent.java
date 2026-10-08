package engine.core;

import engine.helper.EventType;

public class MarioEvent {
    private EventType eventType;
    private int eventParam;
    private float marioX;
    private float marioY;
    private int marioState;
    private int time;

    // Explanation: Constructs and initializes a new MarioEvent instance with specified parameters.
    public MarioEvent(EventType eventType) {
        this.eventType = eventType;
        this.eventParam = 0;
        this.marioX = 0;
        this.marioY = 0;
        this.marioState = 0;
        this.time = 0;
    }

    // Explanation: Constructs and initializes a new MarioEvent instance with specified parameters.
    public MarioEvent(EventType eventType, int eventParam) {
        this.eventType = eventType;
        this.eventParam = eventParam;
        this.marioX = 0;
        this.marioY = 0;
        this.marioState = 0;
        this.time = 0;
    }

    // Explanation: Constructs and initializes a new MarioEvent instance with specified parameters.
    public MarioEvent(EventType eventType, float x, float y, int state, int time) {
        this.eventType = eventType;
        this.eventParam = 0;
        this.marioX = x;
        this.marioY = y;
        this.marioState = state;
        this.time = time;
    }

    // Explanation: Constructs and initializes a new MarioEvent instance with specified parameters.
    public MarioEvent(EventType eventType, int eventParam, float x, float y, int state, int time) {
        this.eventType = eventType;
        this.eventParam = eventParam;
        this.marioX = x;
        this.marioY = y;
        this.marioState = state;
        this.time = time;
    }

    // Explanation: Returns the current event type value.
    public int getEventType() {
        return this.eventType.getValue();
    }

    // Explanation: Returns the current event param value.
    public int getEventParam() {
        return this.eventParam;
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

    // Explanation: Returns the current time value.
    public int getTime() {
        return this.time;
    }

    // Explanation: Executes the equals routine on MarioEvent.
    @Override
    public boolean equals(Object obj) {
        MarioEvent otherEvent = (MarioEvent) obj;
        return this.eventType == otherEvent.eventType &&
                (this.eventParam == 0 || this.eventParam == otherEvent.eventParam);
    }
}
