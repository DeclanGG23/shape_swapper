
import streamlit as st

# Function to normalize shapes
def normalize_shape(shape):
    return ''.join(sorted(shape))

# Function to check if the state matches the goal
def matches_goal(current_shapes, goal_shapes):
    return all(normalize_shape(current_shapes[i]) == normalize_shape(goal_shapes[i]) for i in range(len(current_shapes)))

# Function to calculate mismatches between current and goal shapes
def calculate_mismatches(current_shapes, goal_shapes):
    mismatches = 0
    for i in range(len(current_shapes)):
        if normalize_shape(current_shapes[i]) != normalize_shape(goal_shapes[i]):
            mismatches += 1
    return mismatches

# Function to generate possible swaps
def generate_possible_swaps(current_shapes):
    swaps = []
    for i in range(len(current_shapes)):
        for j in range(i + 1, len(current_shapes)):
            swaps.append((i, j))
    return swaps

# Function to perform a swap
def perform_swap(current_shapes, swap):
    i, j = swap
    new_shapes = current_shapes[:]
    new_shapes[i], new_shapes[j] = new_shapes[j], new_shapes[i]
    return new_shapes

# Function to generate the goal shapes based on the input abbreviation
def generate_goal_shapes(stored_input):
    shapes = ['C', 'S', 'T']
    goal_shapes = []
    for letter in stored_input:
        remaining_shapes = ''.join(sorted([s for s in shapes if s != letter]))
        goal_shapes.append(remaining_shapes)
    return goal_shapes

# Function to solve the shapes
def solve_shapes(initial_shapes, goal_shapes):
    current_shapes = initial_shapes[:]
    steps = []
    performed_swaps = set()

    st.write(f"Initial shapes: {current_shapes}")
    st.write(f"Goal shapes: {goal_shapes}")

    while not matches_goal(current_shapes, goal_shapes):
        swaps = generate_possible_swaps(current_shapes)
        st.write(f"Available swaps: {swaps}")

        best_swap = None
        min_mismatches = calculate_mismatches(current_shapes, goal_shapes)
        
        for swap in swaps:
            if swap in performed_swaps or (swap[1], swap[0]) in performed_swaps:
                continue  # Skip redundant swaps
            new_shapes = perform_swap(current_shapes, swap)
            mismatches = calculate_mismatches(new_shapes, goal_shapes)
            st.write(f"Trying swap: {swap} -> {new_shapes}, Mismatches: {mismatches}")

            if mismatches < min_mismatches:
                min_mismatches = mismatches
                best_swap = swap
                st.write(f"Best swap so far: {swap} -> {new_shapes}, Mismatches: {mismatches}")

        if best_swap:
            performed_swaps.add(best_swap)
            current_shapes = perform_swap(current_shapes, best_swap)
            steps.append(f"Swap {best_swap[0] + 1} with {best_swap[1] + 1}")
            st.write(f"Performed best swap: {best_swap}, Current shapes: {current_shapes}")
        else:
            st.write("No valid swaps found. Ending process.")
            break

    st.write(f"Final shapes: {current_shapes}")
    return steps, current_shapes

# Streamlit app
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
                steps, final_shapes = solve_shapes(initial_shapes, goal_shapes)

                # Check if the goal shapes were achieved
                if matches_goal(final_shapes, goal_shapes):
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
