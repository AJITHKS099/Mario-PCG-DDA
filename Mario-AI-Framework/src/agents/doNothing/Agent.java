package agents.doNothing;

import engine.core.MarioAgent;
import engine.core.MarioForwardModel;
import engine.core.MarioTimer;
import engine.helper.MarioActions;

public class Agent implements MarioAgent {
    // Explanation: Initializes and prepares Agent state and configuration before execution begins.
    @Override
    public void initialize(MarioForwardModel model, MarioTimer timer) {

    }

    // Explanation: Evaluates current world state and returns boolean button action array for Mario controller.
    @Override
    public boolean[] getActions(MarioForwardModel model, MarioTimer timer) {
        return new boolean[MarioActions.numberOfActions()];
    }

    // Explanation: Returns the current agent name value.
    @Override
    public String getAgentName() {
        return "DoNothingAgent";
    }
}
