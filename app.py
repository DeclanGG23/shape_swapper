
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

def find_best_swap(current_shapes, goal_shapes):
    best_swap = None
    min_mismatches = float('inf')
    
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
                            
                            # Check if this swap reduces mismatches
                            if mismatches < min_mismatches:
                                min_mismatches = mismatches
                                best_swap = (i, j, char_i, char_j)
                                print(f"Considered swap: {char_i} from shape {i+1} with {char_j} from shape {j+1}")
                                print(f"Resulting shapes: {new_shapes}")
                                print(f"Mismatches: {mismatches}")
    
    return best_swap

def generate_steps(initial_shapes, goal_shapes):
    steps = []
    current_shapes = [normalize(shape) for shape in initial_shapes]
    goal_shapes = [normalize(shape) for shape in goal_shapes]

    print(f"Initial shapes: {current_shapes}")  # Debug statement
    print(f"Goal shapes: {goal_shapes}")  # Debug statement

    while current_shapes != goal_shapes:
        swap = find_best_swap(current_shapes, goal_shapes)
        if not swap:
            break
        i, j, char_i, char_j = swap
        current_shapes[i] = current_shapes[i].replace(char_i, char_j, 1)
        current_shapes[j] = current_shapes[j].replace(char_j, char_i, 1)
        steps.append(f"Swap {char_i} from shape {i+1} with {char_j} from shape {j+1}")
        print(f"After swap: {current_shapes}")  # Debug statement

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
                inverse_shape_map = {
                    "pyramid": "TT", "prism": "TS", "cone": "TC",
                    "cube": "SS", "cylinder": "SC", "sphere": "CC"
                }
                initial_shapes = [
                    inverse_shape_map[shape1], 
                    inverse_shape_map[shape2], 
                    inverse_shape_map[shape3]
                ]

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
