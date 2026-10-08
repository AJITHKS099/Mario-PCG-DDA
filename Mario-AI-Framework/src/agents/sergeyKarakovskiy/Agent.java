package agents.sergeyKarakovskiy;

import engine.core.MarioAgent;
import engine.core.MarioForwardModel;
import engine.core.MarioTimer;
import engine.helper.MarioActions;

/**
 * @author SergeyKarakovskiy
 */
public class Agent implements MarioAgent {
    private boolean[] actions = null;

    // Explanation: Initializes and prepares Agent state and configuration before execution begins.
    @Override
    public void initialize(MarioForwardModel model, MarioTimer timer) {
        actions = new boolean[MarioActions.numberOfActions()];
        actions[MarioActions.RIGHT.getValue()] = true;
        actions[MarioActions.SPEED.getValue()] = true;
    }

    // Explanation: Evaluates current world state and returns boolean button action array for Mario controller.
    @Override
    public boolean[] getActions(MarioForwardModel model, MarioTimer timer) {
        actions[MarioActions.SPEED.getValue()] = actions[MarioActions.JUMP.getValue()] = model.mayMarioJump() || !model.isMarioOnGround();
        return actions;
    }

    // Explanation: Returns the current agent name value.
    @Override
    public String getAgentName() {
        return "SergeyKarakovskiyAgent";
    }
}
