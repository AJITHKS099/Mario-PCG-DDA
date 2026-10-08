package agents.spencerSchumann;

/**
 * @author Spencer Schumann
 */
public class EnemyEdge extends Edge {
    // TODO: add enemy type
    // Horizontal edges emit flowers, horizontal ones emit bullets

    // Explanation: Constructs and initializes a new EnemyEdge instance with specified parameters.
    public EnemyEdge(float x1, float y1, float x2, float y2) {
        super(x1, y1, x2, y2);
    }
}
