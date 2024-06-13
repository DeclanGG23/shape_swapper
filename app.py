
import streamlit as st
from functools import lru_cache
# Function to normalize shapes
def normalize_shape(shape):
    return tuple(sorted(shape))

# Check if the current state matches the goal state
def matches_goal(current_shapes, goal_shapes):
    return all(normalize_shape(current_shapes[i]) == goal_shapes[i] for i in range(len(current_shapes)))

# Use lru_cache to store results of mismatch calculations
@lru_cache(maxsize=None)
def calculate_mismatches(current_shapes, goal_shapes):
    return sum(1 for i in range(len(current_shapes)) if current_shapes[i] != goal_shapes[i])

# Generate possible swaps between shapes
def generate_possible_swaps(current_shapes):
    swaps = []
    for i in range(len(current_shapes)):
        for j in range(i + 1, len(current_shapes)):
            swaps.append((i, j))
    return swaps

# Perform a swap and return a new tuple of shapes
def perform_swap(current_shapes, swap):
    i, j = swap
    new_shapes = list(current_shapes)
    new_shapes[i], new_shapes[j] = new_shapes[j], new_shapes[i]
    return tuple(new_shapes)

# Main solving function using the above utility functions
def solve_shapes(initial_shapes, goal_shapes):
    current_shapes = tuple(initial_shapes)
    steps = []
    visited = set()

    while not matches_goal(current_shapes, goal_shapes):
        swaps = generate_possible_swaps(current_shapes)
        best_swap = None
        lowest_mismatches = float('inf')

        for swap in swaps:
            new_shapes = perform_swap(current_shapes, swap)
            if new_shapes in visited:
                continue
            mismatches = calculate_mismatches(new_shapes, goal_shapes)

            if mismatches < lowest_mismatches:
                lowest_mismatches = mismatches
                best_swap = swap, new_shapes

        if best_swap:
            swap, current_shapes = best_swap
            visited.add(current_shapes)
            steps.append(f"Swap {swap[0] + 1} with {swap[1] + 1}")
        else:
            break

    return steps, list(current_shapes)

# Define Streamlit UI elements and interaction
def main():
    st.title('Shape Swapper Game')
    st.write("Enter the 3-letter abbreviation and select the initial 3D shapes.")

    stored_input = st.text_input("Enter the 3-letter abbreviation (e.g., CST):").upper()
    shape_options = ["pyramid", "prism", "cone", "cube", "cylinder", "sphere"]
    shape1 = st.selectbox("Select the first 3D shape:", shape_options).lower()
    shape2 = st.selectbox("Select the second 3D shape:", shape_options).lower()
    shape3 = st.selectbox("Select the third 3D shape:", shape_options).lower()

    if st.button("Calculate"):
        initial_shapes = [normalize_shape(shape) for shape in [shape1, shape2, shape3]]
        goal_shapes = generate_goal_shapes(stored_input)
        steps, final_shapes = solve_shapes(tuple(initial_shapes), tuple(goal_shapes))
        st.write("Steps to achieve the goal:")
        for step in steps:
            st.write(step)
        st.write("Final shapes:")
        st.write(final_shapes)

if __name__ == "__main__":
    main()

