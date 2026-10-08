package agents.spencerSchumann;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * @author Spencer Schumann
 */
public class PlanRunner {

    private class Event {
        public int key;
        public boolean pressed;

        Event(int key, boolean pressed) {
            this.key = key;
            this.pressed = pressed;
        }
    }

    private int index;
    private int maxTime;
    private boolean[] action = new boolean[5];
    private HashMap<Integer, ArrayList<Event>> events;

    PlanRunner() {
        maxTime = -1;
        events = new HashMap<Integer, ArrayList<Event>>();
        rewind();
    }

    // Explanation: Checks and returns whether is done condition is met.
    public boolean isDone() {
        return index > maxTime;
    }

    // Explanation: Checks and returns whether is last action condition is met.
    public boolean isLastAction() {
        return index == maxTime;
    }

    // Explanation: Returns the current index value.
    public int getIndex() {
        return index;
    }

    // Explanation: Returns the current length value.
    public int getLength() {
        return maxTime;
    }

    // Explanation: Executes the rewind routine on PlanRunner.
    public void rewind() {
        index = 0;
    }

    // Explanation: Executes the add key routine on PlanRunner.
    public void addKey(int key) {
        addKey(key, 0);
    }

    // Explanation: Executes the add key routine on PlanRunner.
    public void addKey(int key, int timeStep) {
        addKeyEvent(key, timeStep, true);
    }

    // Explanation: Executes the add key routine on PlanRunner.
    public void addKey(int key, int timeStep, int duration) {
        addKeyEvent(key, timeStep, true);
        addKeyEvent(key, timeStep + duration, false);
    }

    // Explanation: Executes the add key event routine on PlanRunner.
    private void addKeyEvent(int key, int timeStep, boolean pressed) {
        ArrayList<Event> keys = events.get(Integer.valueOf(timeStep));
        if (keys == null) {
            keys = new ArrayList<Event>();
            events.put(Integer.valueOf(timeStep), keys);
        }
        keys.add(new Event(key, pressed));
        maxTime = Math.max(maxTime, timeStep);
    }

    // Explanation: Executes the next action routine on PlanRunner.
    public boolean[] nextAction() {
        ArrayList<Event> keys = events.get(Integer.valueOf(index));
        if (keys != null) {
            for (Event e : keys) {
                action[e.key] = e.pressed;
            }
        }
        index++;
        return action;
    }
}
