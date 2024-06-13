
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

    while current_shapes != goal_shapes:
        made_swap = False
        for i in range(3):
            if current_shapes[i] != goal_shapes[i]:
                for j in range(3):
                    if i != j:
                        for char_i in current_shapes[i]:
                            if char_i not in goal_shapes[i]:
                                for char_j in current_shapes[j]:
                                    if char_j in goal_shapes[i] and char_j not in current_shapes[i]:
                                        # Perform the swap
                                        new_i = current_shapes[i].replace(char_i, char_j, 1)
                                        new_j = current_shapes[j].replace(char_j, char_i, 1)
                                        current_shapes[i], current_shapes[j] = new_i, new_j
                                        steps.append(f"Swap {shape_names[char_i]} from shape {i+1} with {shape_names[char_j]} from shape {j+1}")
                                        made_swap = True
                                        break
                                if made_swap:
                                    break
                        if made_swap:
                            break
                if made_swap:
                    break
        if not made_swap:
            break  # No valid swap found, exit the loop
    return steps, current_shapes

def main():
    st.title('Shape Swapper App')
    st.write("Enter the initial shapes and the target abbreviation to see the steps needed to rearrange the shapes.")

    # Input 1: Abbreviation
    stored_input = st.text_input("Enter the 3-letter abbreviation (e.g., CST):").upper()
    
    # Dropdown options
    shape_options = ["pyramid", "prism", "cone", "cube", "cylinder", "sphere"]
    
    # Input 2: First shape
    shape1 = st.selectbox("Select the first 3D shape:", shape_options).lower()
    
    # Input 3: Second shape
    shape2 = st.selectbox("Select the second 3D shape:", shape_options).lower()
    
    # Input 4: Third shape
    shape3 = st.selectbox("Select the third 3D shape:", shape_options).lower()

    if st.button("Calculate"):
        if stored_input and shape1 and shape2 and shape3:
            try:
                # Map the 3D shape names to their 2D shape abbreviations
                inverse_shape_map = {v: k for k, v in shape_map.items()}
                initial_shapes = [inverse_shape_map[shape1], inverse_shape_map[shape2], inverse_shape_map[shape3]]

                # Generate goal shapes
                goal_shapes = generate_goal_shapes(stored_input)

                # Generate steps to reach the goal
                steps, final_shapes = generate_steps(initial_shapes, goal_shapes)

                # Check if the goal shapes were achieved
                if final_shapes == goal_shapes:
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
                    st.write(f"Stored abbreviation: {stored_input}")
                    st.write(f"Goal shapes: {', '.join(goal_shapes)}")
                    st.write("No possible swaps can achieve the goal state with the given shapes.")
            except KeyError:
                st.error("Invalid shape entered. Please check your inputs.")
        else:
            st.warning("Please fill in all fields.")

if __name__ == "__main__":
    main()
