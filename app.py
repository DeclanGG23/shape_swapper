
import streamlit as st

shape_map = { "TT": "pyramid", "TS": "prism", "TC": "cone", "SS": "cube", "SC": "cylinder", "CC": "sphere", "ST": "prism", "CT": "cone", "CS": "cylinder" }


def generate_goal_shapes(stored_input):
    shapes = ['C', 'S', 'T']
    goal_shapes = []
    for letter in stored_input:
        remaining_shapes = ''.join(sorted([s for s in shapes if s != letter]))
        goal_shapes.append(remaining_shapes)
    return goal_shapes


def normalize(shape):
    return ''.join(sorted(shape))


def find_best_swap(current_shapes, goal_shapes, shape_names, best_mismatches=float('inf'), best_swap=None):
    if current_shapes == goal_shapes:
        return best_swap, best_mismatches

    for i in range(len(current_shapes)):
        for j in range(i + 1, len(current_shapes)):
            for char_i in current_shapes[i]:
                if char_i not in goal_shapes[i]:
                    for char_j in current_shapes[j]:
                        if char_j not in goal_shapes[j]:
                            # Perform the swap
                            new_shapes = current_shapes[:]
                            new_shapes[i] = new_shapes[i].replace(char_i, char_j, 1)
                            new_shapes[j] = new_shapes[j].replace(char_j, char_i, 1)

                            # Count mismatches
                            mismatches = sum(1 for k in range(len(new_shapes)) if normalize(new_shapes[k]) != normalize(goal_shapes[k]))

                            # Recursive call to explore this path
                            recursive_swap, recursive_mismatches = find_best_swap(new_shapes, goal_shapes, shape_names, best_mismatches, best_swap)

                            # Update best solution if found a better path
                            if recursive_mismatches < best_mismatches:
                                best_mismatches = recursive_mismatches
                                best_swap = (i, j, char_i, char_j)

    return best_swap, best_mismatches


def generate_steps(initial_shapes, goal_shapes):
    steps = []
    current_shapes = [normalize(shape) for shape in initial_shapes]
    goal_shapes = [normalize(shape) for shape in goal_shapes]
    shape_names = {'C': 'circle', 'S': 'square', 'T': 'triangle'}

    # Find the best swap sequence using backtracking
    best_swap, best_mismatches = find_best_swap(current_shapes, goal_shapes, shape_names)

    if best_mismatches == float('inf'):
        return steps, current_shapes

    # Generate steps based on the best swap sequence
    while best_swap:
        i, j, char_i, char_j = best_swap
        steps.append(f"Swap {shape_names[char_i]} from shape {i+1} with {shape_names[char_j]} from shape {j+1}")
        current_shapes[i] = current_shapes[i].replace(char_i, char_j, 1)
        current_shapes[j] = current_shapes[j].replace(char_j, char_i, 1)
        best_swap, _ = find_best_swap(current_shapes, goal_shapes, shape_names)

    return steps, current_shapes


def shapes_match(final_shapes, goal_shapes):
    normalized_final_shapes = [normalize(shape) for shape in final_shapes]
    normalized_goal_shapes = [normalize(shape) for shape in goal_shapes]
    return normalized_final_shapes == normalized_goal_shapes


def get_user_input():
  st.title("Shape Swapper App")
  st.write("Enter the initial shapes (C, S, T) and the target abbreviation to see the steps needed to rearrange the shapes.")
  initial_shape1 = st.text_input("Shape 1", "")
  initial_shape2 = st.text_input("Shape 2


