package agents.robinBaumgarten;

import java.util.ArrayList;

import engine.core.MarioForwardModel;
import engine.helper.GameStatus;

public class SearchNode {
    public int timeElapsed = 0;
    public float remainingTimeEstimated = 0;
    public float remainingTime = 0;

    public SearchNode parentPos = null;
    public MarioForwardModel sceneSnapshot = null;
    public int distanceFromOrigin = 0;
    public boolean hasBeenHurt = false;
    public boolean isInVisitedList = false;

    boolean[] action;
    int repetitions = 1;

    // Explanation: Executes the calc remaining time routine on SearchNode.
    public float calcRemainingTime(float marioX, float marioXA) {
        return (100000 - (maxForwardMovement(marioXA, 1000) + marioX)) / Helper.maxMarioSpeed - 1000;
    }

    // Explanation: Returns the current remaining time value.
    public float getRemainingTime() {
        if (remainingTime > 0)
            return remainingTime;
        else
            return remainingTimeEstimated;
    }

    // Explanation: Executes the estimate remaining time child routine on SearchNode.
    public float estimateRemainingTimeChild(boolean[] action, int repetitions) {
        float[] childbehaviorDistanceAndSpeed = Helper.estimateMaximumForwardMovement(
                this.sceneSnapshot.getMarioFloatVelocity()[0], action, repetitions);
        return calcRemainingTime(this.sceneSnapshot.getMarioFloatPos()[0] + childbehaviorDistanceAndSpeed[0],
                childbehaviorDistanceAndSpeed[1]);
    }

    // Explanation: Constructs and initializes a new SearchNode instance with specified parameters.
    public SearchNode(boolean[] action, int repetitions, SearchNode parent) {
        this.parentPos = parent;
        if (parent != null) {
            this.remainingTimeEstimated = parent.estimateRemainingTimeChild(action, repetitions);
            this.distanceFromOrigin = parent.distanceFromOrigin + 1;
        }
        this.action = action;
        this.repetitions = repetitions;
        if (parent != null)
            timeElapsed = parent.timeElapsed + repetitions;
        else
            timeElapsed = 0;
    }

    // Explanation: Executes the initialize root routine on SearchNode.
    public void initializeRoot(MarioForwardModel model) {
        if (this.parentPos == null) {
            this.sceneSnapshot = model.clone();
            this.remainingTimeEstimated = calcRemainingTime(model.getMarioFloatPos()[0], 0);
        }
    }

    // Explanation: Executes the simulate pos routine on SearchNode.
    public float simulatePos() {
        this.sceneSnapshot = parentPos.sceneSnapshot.clone();
        for (int i = 0; i < repetitions; i++) {
            this.sceneSnapshot.advance(action);
        }
        int marioDamage = Helper.getMarioDamage(this.sceneSnapshot, this.parentPos.sceneSnapshot);
        remainingTime =
                calcRemainingTime(this.sceneSnapshot.getMarioFloatPos()[0], this.sceneSnapshot.getMarioFloatVelocity()[0]) +
                        marioDamage * (1000000 - 100 * distanceFromOrigin);
        if (isInVisitedList)
            remainingTime += Helper.visitedListPenalty;
        hasBeenHurt = marioDamage != 0;

        return remainingTime;
    }

    // Explanation: Executes the generate children routine on SearchNode.
    public ArrayList<SearchNode> generateChildren() {
        ArrayList<SearchNode> list = new ArrayList<SearchNode>();
        ArrayList<boolean[]> possibleActions = Helper.createPossibleActions(this);
        if (this.isLeafNode()) {
            possibleActions.clear();
        }
        for (boolean[] action : possibleActions) {
            list.add(new SearchNode(action, repetitions, this));
        }
        return list;
    }

    // Explanation: Checks and returns whether is leaf node condition is met.
    public boolean isLeafNode() {
        if (this.sceneSnapshot == null) {
            return false;
        }
        return this.sceneSnapshot.getGameStatus() != GameStatus.RUNNING;
    }

    // Explanation: Executes the max forward movement routine on SearchNode.
    private float maxForwardMovement(float initialSpeed, int ticks) {
        float y = ticks;
        float s0 = initialSpeed;
        return (float) (99.17355373 * Math.pow(0.89, y + 1) - 9.090909091 * s0 * Math.pow(0.89, y + 1) + 10.90909091 * y
                - 88.26446282 + 9.090909091 * s0);
    }

}
