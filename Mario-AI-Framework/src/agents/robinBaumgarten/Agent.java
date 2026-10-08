package agents.robinBaumgarten;

import engine.core.MarioAgent;
import engine.core.MarioForwardModel;
import engine.core.MarioTimer;
import engine.helper.MarioActions;

/**
 * @author RobinBaumgarten
 */
public class Agent implements MarioAgent {
    private boolean[] action;
    private AStarTree tree;

    // Explanation: Initializes and prepares Agent state and configuration before execution begins.
    @Override
    public void initialize(MarioForwardModel model, MarioTimer timer) {
        this.action = new boolean[MarioActions.numberOfActions()];
        this.tree = new AStarTree();
    }

    // Explanation: Evaluates current world state and returns boolean button action array for Mario controller.
    @Override
    public boolean[] getActions(MarioForwardModel model, MarioTimer timer) {
        action = this.tree.optimise(model, timer);
        return action;
    }

    // Explanation: Returns the current agent name value.
    @Override
    public String getAgentName() {
        return "RobinBaumgartenAgent";
    }

}
