
import streamlit as st

# Mapping from shape pairs to 3D shapes
shape_map = {
    "TT": "pyramid", "TS": "prism", "TC": "cone",
    "SS": "cube", "SC": "cylinder", "CC": "sphere",
    "ST": "prism", "CT": "cone", "CS": "cylinder"
}

# Function to generate the goal shapes based on the input abbreviation
def generate_goal_shapes(stored_input):
    shapes = ['C', 'S', 'T']
    goal_shapes = []
    for letter in stored_input:
        remaining_shapes = ''.join(sorted([s for s in shapes if s != letter]))
        goal_shapes.append(remaining_shapes)
    return goal_shapes

# Function to determine the steps required to rearrange the shapes to meet the goal
def generate_steps(initial_shapes, goal_shapes):
    steps = []
    current_shapes = initial_shapes[:]
    shape_names = {'C': 'circle', 'S': 'square', 'T': 'triangle'}

    for i in range(3):
        target_shape = goal_shapes[i]
        while current_shapes[i] != target_shape:
            found = False
            for j in range(3):
                if i != j:
                    for char_i in current_shapes[i]:
                        if char_i not in target_shape:
                            for char_j in current_shapes[j]:
                                if char_j in target_shape and char_j not in current_shapes[i]:
                                    # Perform the swap
                                    new_i = current_shapes[i].replace(char_i, char_j, 1)
                                    new_j = current_shapes[j].replace(char_j, char_i, 1)
                                    current_shapes[i], current_shapes[j] = new_i, new_j
                                    steps.append(f"Swap {shape_names[char_i]} from statue {i+1} with {shape_names[char_j]} from statue {j+1}")
                                    found = True
                                    break
                            if found:
                                break
                if found:
                    break
            if not found:
                # If no valid swaps found, break to avoid infinite loop
                break
    return steps

st.title('Shape Swapper App')

stored_input = st.text_input("Enter the 3-letter abbreviation (e.g., CST):").upper()
shape1 = st.text_input("Enter the first 3D shape (e.g., pyramid, prism, cone, cube, cylinder, sphere):").lower()
shape2 = st.text_input("Enter the second 3D shape (e.g., pyramid, prism, cone, cube, cylinder, sphere):").lower()
shape3 = st.text_input("Enter the third 3D shape (e.g., pyramid, prism, cone, cube, cylinder, sphere):").lower()

if st.button("Calculate"):
    if stored_input and shape1 and shape2 and shape3:
        # Map the 3D shape names to their 2D shape abbreviations
        inverse_shape_map = {v: k for k, v in shape_map.items()}
        initial_shapes = [inverse_shape_map[shape1], inverse_shape_map[shape2], inverse_shape_map[shape3]]

        # Generate goal shapes
        goal_shapes = generate_goal_shapes(stored_input)

        # Generate steps to reach the goal
        steps = generate_steps(initial_shapes, goal_shapes)

        # Display results
        st.write(f"Stored abbreviation: {stored_input}")
        st.write(f"Goal shapes: {', '.join(goal_shapes)}")
        st.write("Steps to achieve the goal:")
        if steps:
            for i, step in enumerate(steps):
                st.write(f"Step {i+1}: {step}")
        else:
            st.write("No swaps needed, already in goal state.")
    else:
        st.write("Please fill in all fields.")
