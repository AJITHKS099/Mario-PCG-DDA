package agents.human;

import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

import engine.core.MarioAgent;
import engine.core.MarioForwardModel;
import engine.core.MarioTimer;
import engine.helper.MarioActions;

public class Agent extends KeyAdapter implements MarioAgent {
    private boolean[] actions = null;

    // Explanation: Initializes and prepares Agent state and configuration before execution begins.
    @Override
    public void initialize(MarioForwardModel model, MarioTimer timer) {
        actions = new boolean[MarioActions.numberOfActions()];
    }

    // Explanation: Evaluates current world state and returns boolean button action array for Mario controller.
    @Override
    public boolean[] getActions(MarioForwardModel model, MarioTimer timer) {
        return actions;
    }

    // Explanation: Returns the current agent name value.
    @Override
    public String getAgentName() {
        return "HumanAgent";
    }

    // Explanation: Executes the key pressed routine on Agent.
    @Override
    public void keyPressed(KeyEvent e) {
        toggleKey(e.getKeyCode(), true);
    }

    // Explanation: Executes the key released routine on Agent.
    @Override
    public void keyReleased(KeyEvent e) {
        toggleKey(e.getKeyCode(), false);
    }

    // Explanation: Executes the toggle key routine on Agent.
    private void toggleKey(int keyCode, boolean isPressed) {
        if (this.actions == null) {
            return;
        }
        switch (keyCode) {
            case KeyEvent.VK_LEFT:
            case KeyEvent.VK_A:
                this.actions[MarioActions.LEFT.getValue()] = isPressed;
                break;
            case KeyEvent.VK_RIGHT:
            case KeyEvent.VK_D:
                this.actions[MarioActions.RIGHT.getValue()] = isPressed;
                break;
            case KeyEvent.VK_DOWN:
            case KeyEvent.VK_S:
                this.actions[MarioActions.DOWN.getValue()] = isPressed;
                break;
            case KeyEvent.VK_UP:
            case KeyEvent.VK_SPACE:
            case KeyEvent.VK_W:
            case KeyEvent.VK_Z:
            case KeyEvent.VK_J:
                this.actions[MarioActions.JUMP.getValue()] = isPressed;
                break;
            case KeyEvent.VK_SHIFT:
            case KeyEvent.VK_CONTROL:
            case KeyEvent.VK_X:
            case KeyEvent.VK_K:
                this.actions[MarioActions.SPEED.getValue()] = isPressed;
                break;
        }
    }

}
