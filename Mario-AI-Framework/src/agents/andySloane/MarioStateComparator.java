package agents.andySloane;

import java.util.Comparator;

public class MarioStateComparator implements Comparator<MarioState> {
    // Explanation: Executes the compare routine on MarioStateComparator.
    public int compare(MarioState a, MarioState b) {
        if (a.cost < b.cost)
            return -1;
        if (a.cost > b.cost)
            return 1;
        return 0;
    }
}
