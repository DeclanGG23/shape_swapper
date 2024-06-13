
import streamlit as st

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

def normalize(shape):
    return ''.join(sorted(shape))

def solve_slot(current_shapes, slot_index, goal_shape, steps, shape_names):
    goal_shape = normalize(goal_shape)
    for i in range(len(current_shapes)):
        if i != slot_index:
            needed_chars = [c for c in goal_shape if c not in current_shapes[slot_index]]
            for char in needed_chars:
                if char in current_shapes[i]:
                    # Swap the first incorrect char from the slot with the needed char
                    incorrect_chars = [c for c in current_shapes[slot_index] if c not in goal_shape]
                    if incorrect_chars:
                        incorrect_char = incorrect_chars[0]
                        current_shapes[slot_index] = current_shapes[slot_index].replace(incorrect_char, char, 1)
                        current_shapes[i] = current_shapes[i].replace(char, incorrect_char, 1)
                        steps.append(f"Swap {shape_names[incorrect_char]} from shape {slot_index+1} with {shape_names[char]} from shape {i+1}")
                        print(f"After swap: {current_shapes}")  # Debug statement
                        return  # Perform only one swap at a time

def generate_steps(initial_shapes, goal_shapes):
    steps = []
    current_shapes = [normalize(shape) for shape in initial_shapes]
    goal_shapes = [normalize(shape) for shape in goal_shapes]
    shape_names = {'C': 'circle', 'S': 'square', 'T': 'triangle'}

    print(f"Initial shapes: {current_shapes}")  # Debug statement
    print(f"Goal shapes: {goal_shapes}")  # Debug statement

    # Solve the first slot completely
    solve_slot(current_shapes, 0, goal_shapes[0], steps, shape_names)
    print(f"After solving first slot: {current_shapes}")  # Debug statement
    
    # Now, handle slots 2 and 3 if they are not already correct
    if current_shapes[1] != goal_shapes[1] or current_shapes[2] != goal_shapes[2]:
        solve_slot(current_shapes, 1, goal_shapes[1], steps, shape_names)
        print(f"After solving second slot: {current_shapes}")  # Debug statement
        if current_shapes[2] != goal_shapes[2]:
            solve_slot(current_shapes, 2, goal_shapes[2], steps, shape_names)
            print(f"After solving third slot: {current_shapes}")  # Debug statement

    return steps, current_shapes

def shapes_match(final_shapes, goal_shapes):
    normalized_final_shapes = [normalize(shape) for shape in final_shapes]
    normalized_goal_shapes = [normalize(shape) for shape in goal_shapes]
    return normalized_final_shapes == normalized_goal_shapes

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
                if shapes_match(final_shapes, goal_shapes):
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
                    st.write(f"Final shapes: {final_shapes}")  # Debug statement
            except KeyError:
                st.error("Invalid shape entered. Please check your inputs.")
        else:
            st.warning("Please fill in all fields.")

if __name__ == "__main__":
    main()
