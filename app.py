
import streamlit as st

# Function to normalize shapes
def normalize_shape(shape):
    return ''.join(sorted(shape))

def matches_goal(current_shapes, goal_shapes):
    return all(normalize_shape(current_shapes[i]) == normalize_shape(goal_shapes[i]) for i in range(len(current_shapes)))

def generate_possible_swaps(current_shapes, goal_shapes):
    swaps = []
    for i in range(len(current_shapes)):
        for j in range(i + 1, len(current_shapes)):
            if current_shapes[i] != goal_shapes[i] or current_shapes[j] != goal_shapes[j]:
                swaps.append((i, j))
    return swaps

def perform_swap(current_shapes, swap):
    i, j = swap
    new_shapes = current_shapes[:]
    new_shapes[i], new_shapes[j] = new_shapes[j], new_shapes[i]
    return new_shapes

def generate_goal_shapes(stored_input):
    shapes = ['C', 'S', 'T']
    goal_shapes = []
    for letter in stored_input:
        remaining_shapes = ''.join(sorted([s for s in shapes if s != letter]))
        goal_shapes.append(remaining_shapes)
    return goal_shapes

def solve_shapes(initial_shapes, goal_shapes):
    current_shapes = initial_shapes[:]
    steps = []

    while not matches_goal(current_shapes, goal_shapes):
        swaps = generate_possible_swaps(current_shapes, goal_shapes)
        best_swap = None
        lowest_mismatches = float('inf')

        for swap in swaps:
            new_shapes = perform_swap(current_shapes, swap)
            mismatches = sum(normalize_shape(new_shapes[i]) != normalize_shape(goal_shapes[i]) for i in range(len(new_shapes)))

            if mismatches < lowest_mismatches:
                lowest_mismatches = mismatches
                best_swap = swap

        if best_swap:
            current_shapes = perform_swap(current_shapes, best_swap)
            steps.append(f"Swap {best_swap[0] + 1} with {best_swap[1] + 1}")
        else:
            break  # No beneficial swaps found

    return steps, current_shapes

def main():
    st.title('Shape Swapper App')
    stored_input = st.text_input("Enter the 3-letter abbreviation (e.g., CST):").upper()
    shape_options = ["pyramid", "prism", "cone", "cube", "cylinder", "sphere"]
    shape1 = st.selectbox("Select the first 3D shape:", shape_options).lower()
    shape2 = st.selectbox("Select the second 3D shape:", shape_options).lower()
    shape3 = st.selectbox("Select the third 3D shape:", shape_options).lower()

    if st.button("Calculate"):
        inverse_shape_map = {"pyramid": "TT", "prism": "TS", "cone": "TC", "cube": "SS", "cylinder": "SC", "sphere": "CC"}
        initial_shapes = [inverse_shape_map[shape1], inverse_shape_map[shape2], inverse_shape_map[shape3]]
        goal_shapes = generate_goal_shapes(stored_input)
        steps, final_shapes = solve_shapes(initial_shapes, goal_shapes)
        st.write("Steps to achieve the goal:")
        for step in steps:
            st.write(step)
        st.write(f"Final shapes: {final_shapes}")

if __name__ == "__main__":
    main()
