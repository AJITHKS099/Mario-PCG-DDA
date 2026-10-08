import heapq

class MarioPhysicsValidator:
    """
    Discrete 2D Physics A* Pathfinding Solver for Mario Levels.
    Simulates Mario's run, jump, gravity, tile collisions, pit bounds, and hazards.
    """
    # Explanation: Initializes A* reachability solver with level geometry, start position, exit goal, and Mario physics constants.
    def __init__(self, max_nodes=5000):
        self.max_nodes = max_nodes
        self.solid_tiles = set(['X', 'S', 'Q', '?', 'D', 't', 'T', 'B', 'b', '#'])
        self.hazard_tiles = set(['g', 'k', 'r', 'y', 'G', 'K', 'R'])

    # Explanation: Executes A* pathfinding search through level grid to determine if exit flagpole can be reached without dying.
    def is_level_solvable(self, level_source):
        """
        Evaluates whether a level layout is solvable by Mario using A* pathfinding.
        Returns: (is_solvable, metrics_dict)
        """
        if isinstance(level_source, str):
            lines = [line.rstrip('\r\n') for line in level_source.strip().splitlines() if line.strip()]
        else:
            lines = level_source

        if not lines:
            return False, {"is_solvable": False, "reason": "Empty level layout"}

        height = len(lines)
        width = len(lines[0])

        # Find Mario spawn (col 0) and Exit Flagpole F / Castle
        start_x = 0
        start_y = 12
        exit_x = width - 15

        for r in range(height):
            for c in range(width):
                if lines[r][c] == 'M':
                    start_x = c
                    start_y = r
                elif lines[r][c] == 'F':
                    exit_x = c

        # State: (x, y, vy, on_ground)
        start_state = (start_x, start_y, 0, True)

        # Priority Queue: (f_score, g_score, x, y, vy, on_ground, jump_count)
        # f_score = g_score + h(x)
        h_start = max(0, exit_x - start_x)
        pq = [(h_start, 0, start_x, start_y, 0, True, 0)]

        visited = set()
        visited.add(start_state)

        nodes_explored = 0
        solvable = False
        optimal_path_length = 0
        required_jumps = 0
        tight_jumps = 0

        while pq and nodes_explored < self.max_nodes:
            f, g, x, y, vy, on_ground, jumps = heapq.heappop(pq)
            nodes_explored += 1

            if x >= exit_x - 1:
                solvable = True
                optimal_path_length = g
                required_jumps = jumps
                break

            # Possible actions: dx in [-1, 1, 2], do_jump in [True, False]
            possible_actions = []
            for dx in [1, 2, 0, -1]:
                possible_actions.append((dx, False))
                if on_ground:
                    possible_actions.append((dx, True))

            for dx, do_jump in possible_actions:
                nx = x + dx
                if nx < 0 or nx >= width:
                    continue

                nvy = vy
                n_on_ground = on_ground

                if do_jump and on_ground:
                    nvy = -4  # Max jump impulse (up to 4 tiles)
                    n_on_ground = False
                    n_jumps = jumps + 1
                else:
                    n_jumps = jumps

                # Apply gravity
                if not n_on_ground:
                    nvy = min(3, nvy + 1)

                ny = y + nvy

                # Check vertical bounds
                if ny >= height:
                    continue  # Fell into pit gap

                ny = max(0, min(height - 1, ny))

                # Collision check
                tile = lines[ny][nx] if ny < height and nx < width else '-'
                if tile in self.solid_tiles:
                    # If falling onto solid tile, land on top
                    if nvy > 0:
                        ny = ny - 1
                        nvy = 0
                        n_on_ground = True
                    else:
                        continue  # Hit ceiling or solid wall
                else:
                    # Check tile underneath for landing
                    below_y = min(height - 1, ny + 1)
                    below_tile = lines[below_y][nx] if nx < width else '-'
                    if below_tile in self.solid_tiles:
                        n_on_ground = True
                        nvy = 0
                    else:
                        n_on_ground = False

                # Hazard avoidance
                if tile in self.hazard_tiles and not n_on_ground:
                    continue

                next_state = (nx, ny, nvy, n_on_ground)
                if next_state not in visited:
                    visited.add(next_state)
                    ng = g + 1
                    nh = max(0, exit_x - nx)
                    heapq.heappush(pq, (ng + nh, ng, nx, ny, nvy, n_on_ground, n_jumps))

        jump_precision = round(required_jumps / max(1, optimal_path_length), 3) if solvable else 0.0

        metrics = {
            "is_solvable": solvable,
            "path_length": optimal_path_length,
            "required_jumps": required_jumps,
            "jump_precision": jump_precision,
            "branching_complexity": nodes_explored,
            "exit_x": exit_x
        }

        return solvable, metrics

# Global Instance
_validator_instance = MarioPhysicsValidator()

# Explanation: Executes A* pathfinding search through level grid to determine if exit flagpole can be reached without dying.
def is_level_solvable(level_source):
    return _validator_instance.is_level_solvable(level_source)

if __name__ == "__main__":
    from generator import generate_mario_level
    lvl = generate_mario_level(0.5)
    solvable, stats = is_level_solvable(lvl)
    print("A* Playability Solvable:", solvable)
    print("A* Path Metrics:", stats)
