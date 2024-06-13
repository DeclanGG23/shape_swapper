
import streamlit as st

# Function to normalize shapes
import streamlit as st
from functools import lru_cache

def normalize_shape(shape):
    return ''.join(sorted(shape))

def matches_goal(current_shapes, goal_shapes):
    return all(normalize_shape(current_shapes[i]) == normalize_shape(goal_shapes[i]) for i in range(len(current_shapes)))

@lru_cache(maxsize=None)
def calculate_mismatches(current_shapes, goal_shapes):
    mismatches = sum(1 for i in range(len(current_shapes)) if normalize_shape(current_shapes[i]) != normalize_shape(goal_shapes[i]))
    return mismatches

def generate_possible_swaps(current_shapes):
    swaps = []
    for i in range(len(current_shapes)):
        for j in range(i + 1, len(current_shapes)):
            swaps.append((i, j))
    return swaps

def perform_swap(current_shapes, swap):
    i, j = swap
    new_shapes = list(current_shapes)
    new_shapes[i], new_shapes[j] = new_shapes[j], new_shapes[i]
    return tuple(new_shapes)

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
                continue  # Avoid revisiting the same state
            mismatches = calculate_mismatches(new_shapes, tuple(goal_shapes))

            if mismatches < lowest_mismatches:
                lowest_mismatches = mismatches
                best_swap = swap, new_shapes

        if best_swap:
            swap, current_shapes = best_swap
            visited.add(current_shapes)
            steps.append(f"Swap {swap[0] + 1} with {swap[1] + 1}")
        else:
            break  # No beneficial swaps found

    return steps, list(current_shapes)

# Streamlit app part remains the same

