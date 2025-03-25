# Banker's Algorithm Simulator

## Overview
The Banker's Algorithm Simulator is a web-based tool designed to demonstrate the Banker's Algorithm, a resource allocation and deadlock avoidance technique used in operating systems. This project allows users to input resource allocation data and visualize whether a system is in a safe state, an unsafe state, or a deadlock condition.

## Features
- **Safe State Detection:** Determines if the system is in a safe state and provides a safe sequence of processes.
- **Visualization:** Displays the sequence of processes graphically using D3.js.
- **Real-time Feedback:**
  - ✅ **Green** for safe states.
  - ⚠️ **Orange** for unsafe states with a partial sequence.
  - ❌ **Red** for deadlocks.
- **Error Handling:** Alerts users to invalid JSON formats or input errors.
- **Clear Functionality:** Resets input fields and results with a single button.

## Technologies Used

### Frontend
- HTML/CSS for structure and styling.
- JavaScript for client-side logic.
- D3.js for dynamic graph visualization.

### Backend
- Flask (Python) for handling server-side logic and API requests.

