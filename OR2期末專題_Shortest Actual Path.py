import itertools

# names of places to visit
places = ['風華', '中X', '新X', '廣X', '來X福', '一流台南店']

# distances in a full matrix
dists = [[0, 155, 15.3, 10.1, 27.1, 297],
         [156, 0, 167, 163, 132, 166],
         [14.4, 167, 0, 4.3, 39.9, 306],
         [11.9, 164, 5.4, 0, 36.1, 306],
         [28.9, 134, 39.5, 40.6, 0, 275],
         [298, 167, 306, 303, 275, 0]]

# Function to calculate the total distance of a path
def calculate_total_distance(path):
    total_distance = 0
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        total_distance += dists[start][end]
    # Add the distance from the last place back to the start place
    total_distance += dists[path[-1]][path[0]]
    return total_distance

# Function to find the optimal path and total distance using dynamic programming
def find_optimal_path():
    n = len(places)
    # Initialize the memoization table with infinite distances
    memo = [[float('inf')] * n for _ in range(1 << n)]
    # Start from the initial state where only the starting place is visited
    memo[1][0] = 0

    # Iterate over all possible subsets of places
    for mask in range(1, 1 << n):
        for last in range(n):
            # Check if the last place is included in the subset
            if mask & (1 << last):
                # Compute the minimum distance to reach the current state
                for prev in range(n):
                    # Check if the previous place is included in the subset
                    if prev != last and mask & (1 << prev):
                        memo[mask][last] = min(
                            memo[mask][last],
                            memo[mask ^ (1 << last)][prev] + dists[prev][last]
                        )

    # Find the optimal path and total distance
    shortest_distance = float('inf')
    optimal_path = None

    # Iterate over all possible ending places
    for last in range(1, n):
        distance = memo[(1 << n) - 1][last] + dists[last][0]
        if distance < shortest_distance:
            shortest_distance = distance
            optimal_path = construct_path(memo, last)

    return optimal_path, shortest_distance

# Function to construct the optimal path given the memoization table and the last place
def construct_path(memo, last):
    n = len(places)
    path = [0]  # Start from the initial place
    mask = (1 << n) - 1
    while mask != 0:
        prev = None
        for i in range(n):
            if i != last and mask & (1 << i):
                if prev is None or (
                    memo[mask][last] == memo[mask ^ (1 << last)][prev] + dists[prev][last]
                ):
                    prev = i
        path.append(prev)
        mask ^= 1 << prev
        last = prev
    path.append(0)  # Return to the initial place
    path.reverse()
    return path

# Find the optimal path and total distance
optimal_path, total_distance = find_optimal_path()

# Convert the indexes of optimal_path to corresponding place names
optimal_places = [places[i] for i in optimal_path]

# Create the formatted output with arrow separators
formatted_output = ' -> '.join(optimal_places)

# Print the optimal path and total distance
print("Optimal Path:")
print(formatted_output)
print("Total Distance:", total_distance)
