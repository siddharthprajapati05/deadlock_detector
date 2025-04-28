Automated Deadlock Detection Tool (Banker's Algorithm)

Overview
This Streamlit-based application implements the Banker's Algorithm to detect potential deadlocks and determine safe states in a system by analyzing resource allocation, maximum resource needs, and available resources.
It supports both single-instance and multi-instance resources, providing a user-friendly interface for input, analysis, visualization, and resolution of deadlocks.

The tool also includes:

A Resource Allocation Graph to visualize process-resource relationships.

A System Performance Monitor for simulated metrics.

Features
Input Methods
Demo Data: Predefined dataset for quick testing.

Manual Input: Customizable process and resource configurations with allocation and maximum matrices.

CSV Upload: Import allocation and maximum matrices from CSV files.

Deadlock Analysis
Implements the Banker's Algorithm to check for safe states.

Displays Allocation, Maximum, Need, and Available Resource matrices.

Outputs safe execution sequences or warns of unsafe states.

Visualization
Generates a Resource Allocation Graph using NetworkX and Matplotlib.

Highlights processes (safe/unsafe), resources, allocation edges, and need edges.

Resolution Strategies
Suggests strategies such as:

Process termination

Resource preemption

Allocation policies

Allows simulated implementation of strategies with updated matrices.

System Monitor
Simulates CPU, memory, disk, and network usage metrics.

Displays resource usage history and process information.

Supports simulated real-time monitoring with alerts for potential issues.

User Interface
Streamlit-based interface organized into tabs:

Analysis

Visualization

Resolution Strategies

System Monitor

Sidebar for configuration, including a Reset Application button.

Interactive elements like sliders, buttons, and toggles.

Prerequisites
To run the application, ensure you have the following installed:

Python 3.8 or higher

Required Python packages (listed in requirements.txt):

streamlit

pandas

numpy

networkx

matplotlib

You can install the dependencies using:

bash
Copy
Edit
pip install -r requirements.txt
Installation
Clone or download the repository:

bash
Copy
Edit
git clone <https://github.com/siddharthprajapati05/deadlock_detector.git>
Install the required dependencies:

pip install -r requirements.txt

Ensure the main script (e.g., app.py) is in the project directory.

Usage
Run the Streamlit application:


streamlit run app.py
Access the application in your web browser (typically at http://localhost:8501).

Configure the tool via the sidebar:

Choose an Input Method (Demo Data, Manual Input, or CSV Upload).

For Manual Input: specify the number of processes, resources, and their respective matrices.

For CSV Upload: provide allocation and maximum matrix CSV files.

Navigate through the tabs:

Analysis: Run the Banker's Algorithm to check for safe states and view matrices.

Visualization: Generate and interpret the resource allocation graph.

Resolution Strategies: Explore and implement deadlock resolution options (if applicable).

System Monitor: Monitor simulated performance metrics and toggle real-time monitoring.

Use the Reset Application button in the sidebar to clear the session state and start over.

File Structure

app.py               # The main Streamlit application script
requirements.txt     # Lists the required Python packages
README.md            # Documentation file (this file)

Select Demo Data in the sidebar to load a predefined safe state scenario.

Go to the Analysis tab and click Run Deadlock Analysis to view the safe sequence and matrices.

Switch to the Visualization tab and click Generate Visualization to see the resource allocation graph.

If the system is in an unsafe state, visit the Resolution Strategies tab to explore and implement options.

Check the System Monitor tab for simulated performance metrics and toggle real-time monitoring.

Notes
The application supports multi-instance resources, making it suitable for complex systems.

The resource allocation graph uses NetworkX for graph creation and Matplotlib for rendering.

Resolution strategies are simulated and update matrices dynamically.

The system monitor provides randomized metrics for demonstration purposes.

For CSV uploads, ensure the allocation and maximum matrices have matching resource columns and process indices.

