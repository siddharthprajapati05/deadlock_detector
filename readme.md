# Banker's Algorithm Simulator

## Project Overview
   The **Banker's Algorithm Simulator** is a web-based application designed to demonstrate the Banker's Algorithm, a resource allocation and deadlock avoidance technique used in operating systems. Users can input resource allocation data (allocation matrix, maximum matrix, and available resources) to determine whether the system is in a **safe state**, an **unsafe state**, or a **deadlock condition**. The application provides real-time feedback through color-coded messages and visualizes the safe sequence using a dynamic graph created with **D3.js**.

This project serves as an educational tool for understanding deadlock avoidance concepts in operating systems.

---

## Module-Wise Breakdown
T  he project is divided into the following modules:

### **1. Frontend Module**
   - Manages user input through a responsive web interface.
   - Visualizes the safe sequence using **D3.js**.
   - Provides real-time feedback using color-coded messages:
   - ✅ **Green:** Safe state with a complete safe sequence.
   - ⚠️ **Orange:** Unsafe state with a partial sequence.
   - ❌ **Red:** Deadlock state with no safe sequence.
   - Includes a **Clear** button to reset inputs and results.

### **2. Backend Module**
   - Implements the Banker's Algorithm logic using **Python** and **Flask**.
   - Processes input matrices to determine the system's state.
   - Returns a JSON response with the state (safe, unsafe, or deadlock) and the corresponding sequence (if applicable).

### **3. Visualization Module**
   - Utilizes **D3.js** to create an interactive graph representing the safe sequence of processes.
   - Dynamically updates based on the backend results.

---

## Functionalities

The simulator offers the following key features:

   - **Safe State Detection:** Evaluates if the system is in a safe state and returns a safe sequence.
   - **Visualization:** Displays the sequence graphically using D3.js, with interactive nodes.
   - **Real-time Feedback:**
      - ✅ **Green:** Safe state with a full safe sequence.
      - ⚠️ **Orange:** Unsafe state with a partial sequence (e.g., `P0 → P3`).
      - ❌ **Red:** Deadlock with no safe sequence.
   - **Error Handling:** Provides feedback for invalid JSON input or formatting errors.
   - **Clear Functionality:** Resets input fields, results, and the graph with one click.
   - **Enhanced UI:** Modern design with glassmorphism effects, responsive layout, and tooltips.

---

## Technologies Used

### **Programming Languages:**
- **Python:** Backend logic implementation.
- **JavaScript:** Frontend for input management and graph visualization.
- **HTML/CSS:** Structuring and styling the interface.

### **Libraries and Tools:**
- **Flask (2.2.5)**: Python micro-framework for API handling.
- **gunicorn (21.2.0)**: Python WSGI HTTP server for deployment.
- **D3.js (v6)**: Visualization of process sequences.
- **Fetch API:** Communication between frontend and backend.
- **Font Awesome:** Icons for UI elements.
- **Google Fonts:** Typography with 'Poppins' and 'Roboto Mono'.

### **Other Tools:**
- **GitHub:** Version control and project hosting.

---

## Installation

Follow these steps to set up and run the project locally:

### **1. Clone the Repository:**
```bash
   git clone https://github.com/siddharthprajapati05/deadlock_detector.git
   cd bankers-algorithm-simulator
```

### **2. Install Dependencies:**
Ensure you have Python installed, then run:
```bash
   pip install -r requirements.txt
```

#### *requirements.txt includes:*
   ```
   Flask==2.2.5
   gunicorn==21.2.0
```

### **3. Run the Application:**
Start the Flask server using:
```bash
   python app.py
```

### **4. Access the Application:**
Open your browser and navigate to:
```
   http://localhost:5000
```

---

## Usage

1. **Enter Matrices:** Provide input in JSON format:
    - **Allocation Matrix:** e.g., `[[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]`
    - **Maximum Matrix:** e.g., `[[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]`
    - **Available Resources:** e.g., `[3,3,2]`

2. **Check Safe State:** Click on the **Check Safe State** button.

3. **View Results:**
    - **Safe State:** ✅ A green message with the safe sequence is displayed.
    - **Unsafe State:** ⚠️ An orange message with a partial sequence.
    - **Deadlock:** ❌ A red message without a safe sequence.

4. **Visualization:** View the safe sequence graph using **D3.js**.

5. **Clear Inputs:** Click the **Clear** button to reset the form and results.

---

## Test Cases

### **Test Case 1: Safe State**
- **Allocation Matrix:** `[[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]`
- **Maximum Matrix:** `[[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]`
- **Available Resources:** `[3,3,2]`
- **Expected Output:** ✅ Safe State with sequence: `P1 → P3 → P4 → P0 → P2`

### **Test Case 2: Unsafe State**
- **Allocation Matrix:** `[[0,1,0],[2,0,0],[3,0,2],[0,1,1]]`
- **Maximum Matrix:** `[[7,5,3],[3,2,2],[9,0,2],[2,2,2]]`
- **Available Resources:** `[7,4,3]`
- **Expected Output:** ⚠️ Unsafe State with partial sequence: `P0 → P3`

### **Test Case 3: Deadlock**
- **Allocation Matrix:** `[[1,0,0],[1,1,0],[0,0,1]]`
- **Maximum Matrix:** `[[2,1,1],[1,2,1],[1,1,2]]`
- **Available Resources:** `[0,0,0]`
- **Expected Output:** ❌ Deadlock detected. No safe sequence.

---

## Additional Tests
- **Invalid Input:** Provide malformed JSON data to verify error handling.
- **Clear Functionality:** Ensure all inputs and results are cleared when clicking **Clear**.
- **Responsive Design:** Test on different screen sizes for UI responsiveness.

---

## Screenshots
Add screenshots showcasing:
- The input interface.
- Safe, unsafe, and deadlock state results.
- Visualization using D3.js.
- Mobile and desktop responsive views.

---

## Conclusion and Future Scope

The **Banker's Algorithm Simulator** is an effective educational tool for understanding deadlock avoidance. It simplifies the learning experience through interactive visuals and clear feedback.

### **Future Scope:**
- Support dynamic resource requests from processes.
- Implement a feature to save and load previous simulations.
- Provide additional visual simulations on related concepts.
- Enhance the UI with customizable themes and animations.
- Support multi-resource management for complex scenarios.

