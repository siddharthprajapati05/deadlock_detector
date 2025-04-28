import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
from datetime import datetime
import random

# Set page configuration
st.set_page_config(
    page_title="Automated Deadlock Detection Tool (Banker's Algorithm)",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("Automated Deadlock Detection Tool (Banker's Algorithm)")
st.markdown("""
This tool uses the Banker's Algorithm to detect potential deadlocks and determine safe states in system processes 
by analyzing resource allocation, maximum needs, and available resources. It supports both single and multi-instance resources.
The resource allocation graph visualizes process-resource relationships.
""")

# Sidebar
st.sidebar.header("Configuration")

# Reset button
if st.sidebar.button("Reset Application", key="reset_btn"):
    with st.spinner("Resetting application..."):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Provide feedback
        st.sidebar.success("Application reset to initial state!")
        
        # Rerun to refresh UI
        st.rerun()

# Data input method selection
input_method = st.sidebar.radio(
    "Input Method:",
    ["Demo Data", "Manual Input", "CSV Upload"]
)

# Function to check safe state using Banker's Algorithm
def check_safe_state(processes, resources, allocation_matrix, max_matrix, available_resources):
    num_processes = len(processes)
    num_resources = len(resources)
    
    # Initialize work (available resources) and finish vector
    work = available_resources.copy()
    finish = [False] * num_processes
    safe_sequence = []
    
    # Compute need matrix (Max - Allocation)
    need_matrix = max_matrix - allocation_matrix
    
    # Safety algorithm
    while len(safe_sequence) < num_processes:
        found = False
        for i in range(num_processes):
            if not finish[i]:
                # Check if resources can be allocated
                can_allocate = True
                for j in range(num_resources):
                    if need_matrix[i][j] > work[j]:
                        can_allocate = False
                        break
                if can_allocate:
                    # Simulate resource allocation
                    for j in range(num_resources):
                        work[j] += allocation_matrix[i][j]
                    finish[i] = True
                    safe_sequence.append(processes[i])
                    found = True
        if not found:
            # No safe sequence exists
            return None, need_matrix
    return safe_sequence, need_matrix

# Function to suggest resolution strategies
def suggest_resolution_strategies(processes, resources, allocation_matrix, max_matrix, need_matrix):
    strategies = []
    
    # Strategy 1: Process Termination
    for i, p in enumerate(processes):
        allocated_resources = [resources[j] for j in range(len(resources)) if allocation_matrix[i][j] > 0]
        needed_resources = [resources[j] for j in range(len(resources)) if need_matrix[i][j] > 0]
        
        impact_score = sum(allocation_matrix[i]) / sum(max_matrix[i]) if sum(max_matrix[i]) > 0 else 0
        
        strategies.append({
            "strategy_type": "Process Termination",
            "description": f"Terminate process {p}",
            "impact": f"Impact score: {impact_score:.2f}",
            "details": f"Process {p} holds {sum(allocation_matrix[i])} units of resources and needs {sum(need_matrix[i])} more.",
            "score": impact_score
        })
    
    # Strategy 2: Resource Preemption
    for i, p in enumerate(processes):
        for j, r in enumerate(resources):
            if allocation_matrix[i][j] > 0:
                impact_score = allocation_matrix[i][j] / sum(allocation_matrix[i]) if sum(allocation_matrix[i]) > 0 else 0
                
                waiting_processes = [proc for k, proc in enumerate(processes) if need_matrix[k][j] > 0]
                
                strategies.append({
                    "strategy_type": "Resource Preemption",
                    "description": f"Preempt {int(allocation_matrix[i][j])} units of resource {r} from process {p}",
                    "impact": f"Impact score: {impact_score:.2f}",
                    "details": f"This would allow waiting processes ({', '.join(waiting_processes)}) to proceed.",
                    "score": impact_score
                })
    
    # Strategy 3: Resource Allocation Policy
    strategies.append({
        "strategy_type": "Resource Allocation Policy",
        "description": "Implement hierarchical resource allocation",
        "impact": "Impact score: N/A (System-wide change)",
        "details": "Assign a unique number to each resource and require processes to request resources in ascending order.",
        "score": 0.5
    })
    
    # Sort strategies by impact score (lower is better)
    strategies.sort(key=lambda x: x["score"])
    
    return strategies

# Function to visualize resource allocation graph
def visualize_graph(processes, resources, allocation_matrix, need_matrix, safe_sequence):
    plt.figure(figsize=(10, 8))
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes
    for p in processes:
        G.add_node(p, type="process")
    for r in resources:
        G.add_node(r, type="resource")
    
    # Add allocation edges (resource to process)
    for i, p in enumerate(processes):
        for j, r in enumerate(resources):
            if allocation_matrix[i][j] > 0:
                G.add_edge(r, p, weight=int(allocation_matrix[i][j]), type="allocation")
    
    # Add need edges (process to resource)
    for i, p in enumerate(processes):
        for j, r in enumerate(resources):
            if need_matrix[i][j] > 0:
                G.add_edge(p, r, weight=int(need_matrix[i][j]), type="need")
    
    # Create position dictionary
    pos = nx.spring_layout(G, seed=42)
    
    # Draw process nodes
    process_nodes = [node for node in G.nodes() if node in processes]
    nx.draw_networkx_nodes(G, pos, nodelist=process_nodes, node_color='skyblue', node_size=500, label='Processes')
    
    # Draw resource nodes
    resource_nodes = [node for node in G.nodes() if node in resources]
    nx.draw_networkx_nodes(G, pos, nodelist=resource_nodes, node_color='lightgreen', node_size=500, label='Resources')
    
    # Highlight nodes if unsafe state
    if not safe_sequence:
        nx.draw_networkx_nodes(G, pos, nodelist=process_nodes, node_color='red', node_size=500)
    
    # Draw edges
    allocation_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'allocation']
    need_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'need']
    
    nx.draw_networkx_edges(G, pos, edgelist=allocation_edges, edge_color='green', arrows=True, width=1.5, label='Allocation')
    nx.draw_networkx_edges(G, pos, edgelist=need_edges, edge_color='red', arrows=True, width=1.5, label='Need')
    
    # Draw edge labels for weights
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos)
    
    plt.title("Resource Allocation Graph", size=15)
    plt.legend()
    plt.axis('off')
    
    return plt

# Function to generate demo data (supports multi-instance)
def generate_demo_data():
    processes = [f"P{i}" for i in range(1, 5)]  # P1, P2, P3, P4
    resources = [f"R{i}" for i in range(1, 4)]  # R1, R2, R3
    
    # Total resources (multi-instance)
    total_resources = np.array([3, 3, 2])  # R1: 3 units, R2: 3 units, R3: 2 units
    
    # Available resources (manually set for demo)
    available_resources = np.array([1, 2, 0])  # R1: 1, R2: 2, R3: 0
    
    # Allocation matrix
    allocation_matrix = np.array([
        [0, 1, 0],  # P1
        [2, 0, 0],  # P2
        [3, 0, 1],  # P3
        [0, 1, 1]   # P4
    ])
    
    # Maximum matrix
    max_matrix = np.array([
        [7, 5, 3],  # P1
        [3, 2, 2],  # P2
        [9, 0, 2],  # P3
        [2, 2, 2]   # P4
    ])
    
    return processes, resources, allocation_matrix, max_matrix, total_resources, available_resources

# Function to simulate system load and performance metrics
def generate_system_metrics():
    cpu_usage = random.uniform(20, 95)
    memory_usage = random.uniform(30, 90)
    disk_io = random.uniform(5, 60)
    network_io = random.uniform(10, 70)
    
    return {
        "CPU Usage (%)": cpu_usage,
        "Memory Usage (%)": memory_usage,
        "Disk I/O (MB/s)": disk_io,
        "Network I/O (MB/s)": network_io
    }

# Main application logic
if input_method == "Demo Data":
    st.sidebar.info("Using demo data with a safe state scenario (multi-instance resources)")
    processes, resources, allocation_matrix, max_matrix, total_resources, available_resources = generate_demo_data()

elif input_method == "Manual Input":
    st.sidebar.subheader("Define Processes and Resources")
    
    num_processes = st.sidebar.slider("Number of Processes", 2, 10, 4, key="num_processes")
    num_resources = st.sidebar.slider("Number of Resources", 2, 10, 3, key="num_resources")
    
    processes = [f"P{i+1}" for i in range(num_processes)]
    resources = [f"R{i+1}" for i in range(num_resources)]
    
    st.sidebar.subheader("Resource Configuration")
    st.sidebar.markdown("Specify the total and available instances of each resource")
    
    total_resources = np.zeros(num_resources)
    available_resources = np.zeros(num_resources)
    
    for j, r in enumerate(resources):
        total_resources[j] = st.sidebar.number_input(
            f"Total units of {r}", min_value=1, value=3, step=1, key=f"total_{j}"
        )
        available_resources[j] = st.sidebar.number_input(
            f"Available units of {r}", min_value=0, value=1, step=1, key=f"avail_{j}"
        )
    
    # Initialize matrices
    allocation_matrix = np.zeros((num_processes, num_resources))
    max_matrix = np.zeros((num_processes, num_resources))
    
    # Create tabs for allocation and max matrices
    tab1, tab2 = st.tabs(["Resource Allocation", "Maximum Resources"])
    
    with tab1:
        st.subheader("Resource Allocation Matrix")
        st.markdown("Specify the number of resource units allocated to each process:")
        for i, p in enumerate(processes):
            cols = st.columns(num_resources)
            for j, r in enumerate(resources):
                with cols[j]:
                    allocation_matrix[i][j] = st.number_input(
                        f"{p} has {r}", min_value=0, value=0, step=1, key=f"alloc_{i}_{j}"
                    )
    
    with tab2:
        st.subheader("Maximum Resource Matrix")
        st.markdown("Specify the maximum number of resource units each process may need:")
        for i, p in enumerate(processes):
            cols = st.columns(num_resources)
            for j, r in enumerate(resources):
                with cols[j]:
                    max_matrix[i][j] = st.number_input(
                        f"{p} max {r}", 
                        min_value=int(allocation_matrix[i][j]), 
                        value=max(1, int(allocation_matrix[i][j])), 
                        step=1, 
                        key=f"max_{i}_{j}"
                    )
    
    # Validate inputs
    allocated = np.sum(allocation_matrix, axis=0)
    for j, r in enumerate(resources):
        if allocated[j] + available_resources[j] > total_resources[j]:
            st.sidebar.warning(
                f"Warning: Allocated ({allocated[j]}) + Available ({available_resources[j]}) "
                f"exceeds Total ({total_resources[j]}) for {r}"
            )

elif input_method == "CSV Upload":
    st.sidebar.subheader("Upload CSV Files")
    st.sidebar.markdown("Upload CSV files for allocation and maximum matrices, and specify resources")
    
    allocation_file = st.sidebar.file_uploader("Upload Allocation Matrix CSV", type="csv", key="alloc_file")
    max_file = st.sidebar.file_uploader("Upload Maximum Matrix CSV", type="csv", key="max_file")
    
    st.sidebar.subheader("Resource Configuration")
    num_resources = st.sidebar.slider("Number of Resources", 2, 10, 3, key="num_resources_csv")
    resources = [f"R{i+1}" for i in range(num_resources)]
    
    total_resources = np.zeros(num_resources)
    available_resources = np.zeros(num_resources)
    
    for j, r in enumerate(resources):
        total_resources[j] = st.sidebar.number_input(
            f"Total units of {r}", min_value=1, value=3, step=1, key=f"total_csv_{j}"
        )
        available_resources[j] = st.sidebar.number_input(
            f"Available units of {r}", min_value=0, value=1, step=1, key=f"avail_csv_{j}"
        )
    
    if allocation_file is not None and max_file is not None:
        try:
            allocation_df = pd.read_csv(allocation_file, index_col=0)
            max_df = pd.read_csv(max_file, index_col=0)
            
            processes = allocation_df.index.tolist()
            if set(allocation_df.columns) != set(max_df.columns):
                st.error("Resource columns in allocation and maximum matrices must match")
                processes, resources, allocation_matrix, max_matrix, total_resources, available_resources = generate_demo_data()
            else:
                resources = allocation_df.columns.tolist()
                allocation_matrix = allocation_df.values
                max_matrix = max_df.values
                
                # Validate inputs
                allocated = np.sum(allocation_matrix, axis=0)
                for j, r in enumerate(resources):
                    if allocated[j] + available_resources[j] > total_resources[j]:
                        st.sidebar.warning(
                            f"Warning: Allocated ({allocated[j]}) + Available ({available_resources[j]}) "
                            f"exceeds Total ({total_resources[j]}) for {r}"
                        )
                
                st.success("CSV files loaded successfully!")
                
                # Display the loaded matrices
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Allocation Matrix")
                    st.dataframe(allocation_df)
                with col2:
                    st.subheader("Maximum Matrix")
                    st.dataframe(max_df)
                
        except Exception as e:
            st.error(f"Error loading CSV files: {e}")
            processes, resources, allocation_matrix, max_matrix, total_resources, available_resources = generate_demo_data()
    else:
        st.info("Please upload both CSV files to continue")
        processes, resources, allocation_matrix, max_matrix, total_resources, available_resources = generate_demo_data()

# Create tabs for the main content
tab1, tab2, tab3, tab4 = st.tabs(["Analysis", "Visualization", "Resolution Strategies", "System Monitor"])

# Tab 1: Analysis
with tab1:
    st.header("Deadlock Analysis (Banker's Algorithm)")
    
    # Display matrices and available resources
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Allocation Matrix")
        alloc_df = pd.DataFrame(allocation_matrix, index=processes, columns=resources)
        st.dataframe(alloc_df.style.highlight_max(axis=None, color='lightgreen'))
    
    with col2:
        st.subheader("Maximum Matrix")
        max_df = pd.DataFrame(max_matrix, index=processes, columns=resources)
        st.dataframe(max_df.style.highlight_max(axis=None, color='lightsalmon'))
    
    with col3:
        st.subheader("Available Resources")
        avail_df = pd.DataFrame(available_resources, index=resources, columns=["Available"])
        st.dataframe(avail_df)
    
    # Analysis button
    if st.button("Run Deadlock Analysis", key="analyze_btn"):
        with st.spinner("Analyzing system for safe state..."):
            # Simulate computation time
            time.sleep(1.5)
            
            # Check safe state
            safe_sequence, need_matrix = check_safe_state(processes, resources, allocation_matrix, max_matrix, available_resources)
            
            # Store in session state
            st.session_state['safe_sequence'] = safe_sequence
            st.session_state['need_matrix'] = need_matrix
            
            # Display results
            if safe_sequence:
                st.success("✅ System is in a SAFE STATE.")
                st.subheader("Safe State Execution Order")
                ordinals = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"]
                execution_order = [f"{ordinals[i]}: {process}" for i, process in enumerate(safe_sequence)]
                st.markdown("**Process Execution Order**:\n- " + "\n- ".join(execution_order))
                st.markdown(f"**Sequence**: {' -> '.join(safe_sequence)}")
                st.markdown("""
                This execution order indicates the sequence in which processes can safely complete without causing a deadlock.
                Each process acquires its needed resources, completes, and releases its resources, allowing the next process to proceed.
                """)
                
                # Display need matrix
                st.subheader("Need Matrix (Max - Allocation)")
                need_df = pd.DataFrame(need_matrix, index=processes, columns=resources)
                st.dataframe(need_df.style.highlight_max(axis=None, color='lightblue'))
            else:
                st.error("⚠️ System is in an UNSAFE STATE. Potential deadlock detected.")
                st.subheader("Need Matrix (Max - Allocation)")
                need_df = pd.DataFrame(need_matrix, index=processes, columns=resources)
                st.dataframe(need_df.style.highlight_max(axis=None, color='lightblue'))
                
                # Generate resolution strategies
                strategies = suggest_resolution_strategies(processes, resources, allocation_matrix, max_matrix, need_matrix)
                st.session_state['strategies'] = strategies

# Tab 2: Visualization
with tab2:
    st.header("Resource Allocation Graph")
    
    if st.button("Generate Visualization", key="viz_btn"):
        with st.spinner("Generating resource allocation graph..."):
            # Get safe sequence and need matrix
            if 'safe_sequence' not in st.session_state:
                safe_sequence, need_matrix = check_safe_state(
                    processes, resources, allocation_matrix, max_matrix, available_resources
                )
                st.session_state['safe_sequence'] = safe_sequence
                st.session_state['need_matrix'] = need_matrix
            else:
                safe_sequence = st.session_state['safe_sequence']
                need_matrix = st.session_state['need_matrix']
            
            # Visualize the graph
            fig = visualize_graph(processes, resources, allocation_matrix, need_matrix, safe_sequence)
            st.pyplot(fig)
            
            # Legend explanation
            st.markdown("""
            **Legend:**
            - **Blue nodes**: Processes (safe state)
            - **Green nodes**: Resources
            - **Red nodes**: Processes (unsafe state)
            - **Green edges**: Allocation (resource → process)
            - **Red edges**: Need (process → resource)
            - **Edge labels**: Number of resource units
            """)
            
            # Graph explanation
            st.subheader("Graph Explanation")
            st.markdown("""
            The resource allocation graph shows:
            - **Processes** (P1, P2, ...) and **Resources** (R1, R2, ...).
            - **Allocation edges**: Indicate resources currently held by processes.
            - **Need edges**: Show resources that processes still require to complete.
            - In an **unsafe state**, process nodes are highlighted in red, indicating potential deadlock risks.
            """)

# Tab 3: Resolution Strategies
with tab3:
    st.header("Deadlock Resolution Strategies")
    
    if 'strategies' in st.session_state:
        strategies = st.session_state['strategies']
        
        if strategies:
            st.subheader("Recommended Strategies")
            
            for i, strategy in enumerate(strategies):
                with st.expander(f"{i+1}. {strategy['strategy_type']}: {strategy['description']}"):
                    st.markdown(f"**Impact**: {strategy['impact']}")
                    st.markdown(f"**Details**: {strategy['details']}")
                    
                    if st.button(f"Implement this strategy", key=f"impl_{i}"):
                        st.success(f"Strategy implemented: {strategy['description']}")
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for percent_complete in range(101):
                            if percent_complete < 33:
                                status_text.text("Initiating deadlock resolution process...")
                            elif percent_complete < 66:
                                status_text.text("Applying resolution strategy...")
                            elif percent_complete < 99:
                                status_text.text("Verifying system stability...")
                            else:
                                status_text.text("Resolution applied!")
                            
                            progress_bar.progress(percent_complete)
                            time.sleep(0.02)
                        
                        # Update matrices based on strategy
                        if strategy["strategy_type"] == "Process Termination":
                            process_name = strategy["description"].split()[-1]
                            process_idx = processes.index(process_name)
                            
                            allocation_matrix[process_idx] = 0
                            max_matrix[process_idx] = 0
                            
                            st.info(f"Process {process_name} has been terminated, releasing all held resources.")
                        
                        elif strategy["strategy_type"] == "Resource Preemption":
                            desc_parts = strategy["description"].split()
                            units = int(desc_parts[1])  # Number of units to preempt
                            resource_name = desc_parts[5]  # Resource name (e.g., 'R1')
                            process_name = desc_parts[8]  # Process name (e.g., 'P2')
                            
                            try:
                                resource_idx = resources.index(resource_name)
                                process_idx = processes.index(process_name)
                                
                                # Validate preemption
                                if allocation_matrix[process_idx][resource_idx] < units:
                                    st.error(
                                        f"Cannot preempt {units} units of {resource_name} from {process_name}: "
                                        f"only {allocation_matrix[process_idx][resource_idx]} units allocated."
                                    )
                                    continue
                                
                                # Preempt resources
                                allocation_matrix[process_idx][resource_idx] -= units
                                
                                # Find a waiting process to allocate the resource to
                                for p_idx, p in enumerate(processes):
                                    if st.session_state['need_matrix'][p_idx][resource_idx] >= units:
                                        allocation_matrix[p_idx][resource_idx] += units
                                        st.info(
                                            f"{units} units of resource {resource_name} preempted from {process_name} "
                                            f"and allocated to {p}."
                                        )
                                        break
                                else:
                                    st.info(
                                        f"{units} units of resource {resource_name} preempted from {process_name} "
                                        f"but not reallocated, as no process needs them."
                                    )
                            except ValueError as e:
                                st.error(f"Error processing preemption: {e}")
                                continue
                        
                        # Recompute available resources
                        allocated = np.sum(allocation_matrix, axis=0)
                        available_resources = total_resources - allocated
                        
                        # Re-check safe state
                        safe_sequence, need_matrix = check_safe_state(
                            processes, resources, allocation_matrix, max_matrix, available_resources
                        )
                        
                        st.session_state['safe_sequence'] = safe_sequence
                        st.session_state['need_matrix'] = need_matrix
                        
                        if safe_sequence:
                            st.success("✅ System is now in a SAFE STATE.")
                            st.subheader("Safe State Execution Order")
                            ordinals = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"]
                            execution_order = [f"{ordinals[i]}: {process}" for i, process in enumerate(safe_sequence)]
                            st.markdown("**Process Execution Order**:\n- " + "\n- ".join(execution_order))
                            st.markdown(f"**Sequence**: {' -> '.join(safe_sequence)}")
                            st.markdown("""
                            This execution order indicates the sequence in which processes can safely complete without causing a deadlock.
                            """)
                            
                            # Show updated matrices
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.subheader("Updated Allocation")
                                alloc_df = pd.DataFrame(allocation_matrix, index=processes, columns=resources)
                                st.dataframe(alloc_df.style.highlight_max(axis=None, color='lightgreen'))
                            with col2:
                                st.subheader("Updated Maximum")
                                max_df = pd.DataFrame(max_matrix, index=processes, columns=resources)
                                st.dataframe(max_df.style.highlight_max(axis=None, color='lightsalmon'))
                            with col3:
                                st.subheader("Updated Available")
                                avail_df = pd.DataFrame(available_resources, index=resources, columns=["Available"])
                                st.dataframe(avail_df)
                            
                            st.session_state.pop('strategies', None)
                        else:
                            st.warning("⚠️ System remains in an UNSAFE STATE. Additional strategies may be needed.")
                            st.session_state['strategies'] = suggest_resolution_strategies(
                                processes, resources, allocation_matrix, max_matrix, need_matrix
                            )
                            st.rerun()
            
            st.subheader("Preventive Measures")
            st.markdown("""
            To prevent deadlocks:
            1. **Resource Ordering**: Request resources in a defined order.
            2. **Timeouts**: Limit resource wait times.
            3. **Advance Declaration**: Declare maximum resource needs upfront.
            """)
        else:
            st.info("System is in a safe state, no resolution strategies needed.")
    else:
        st.info("Run the deadlock analysis first to get resolution strategies.")

# Tab 4: System Monitor
with tab4:
    st.header("System Performance Monitor")
    
    metrics = generate_system_metrics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("System Resource Usage")
        st.metric("CPU Usage", f"{metrics['CPU Usage (%)']:.1f}%", 
                  f"{random.uniform(-5, 5):.1f}%")
        st.metric("Memory Usage", f"{metrics['Memory Usage (%)']:.1f}%", 
                 f"{random.uniform(-3, 8):.1f}%")
    
    with col2:
        st.subheader("I/O Performance")
        st.metric("Disk I/O", f"{metrics['Disk I/O (MB/s)']:.1f} MB/s", 
                 f"{random.uniform(-2, 6):.1f} MB/s")
        st.metric("Network I/O", f"{metrics['Network I/O (MB/s)']:.1f} MB/s", 
                 f"{random.uniform(-4, 7):.1f} MB/s")
    
    st.subheader("Resource Usage History")
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=20, freq='1min')
    history_data = {
        'CPU': [random.uniform(20, 95) for _ in range(20)],
        'Memory': [random.uniform(30, 90) for _ in range(20)],
        'Disk': [random.uniform(5, 60) for _ in range(20)],
        'Network': [random.uniform(10, 70) for _ in range(20)]
    }
    history_df = pd.DataFrame(history_data, index=timestamps)
    st.line_chart(history_df)
    
    st.subheader("Process Information")
    process_data = {
        'PID': [random.randint(1000, 9999) for _ in range(len(processes))],
        'Process': processes,
        'CPU (%)': [random.uniform(0, 25) for _ in range(len(processes))],
        'Memory (MB)': [random.uniform(50, 500) for _ in range(len(processes))],
        'Status': ['Running' if random.random() > 0.2 else 'Waiting' for _ in range(len(processes))]
    }
    process_df = pd.DataFrame(process_data)
    st.dataframe(process_df.style.highlight_max(subset=['CPU (%)', 'Memory (MB)'], color='yellow'))
    
    if st.toggle("Enable Real-time Monitoring", value=False):
        st.info("Real-time monitoring enabled.")
        status_placeholder = st.empty()
        if st.button("Simulate Monitoring Cycle"):
            for i in range(5):
                status_placeholder.info(f"Monitoring cycle {i+1}/5 - {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(1)
            if random.random() > 0.7:
                status_placeholder.warning("⚠️ Potential resource contention detected")
            else:
                status_placeholder.success("✅ System operating normally")

# Footer
st.markdown("---")
st.markdown("""
**Automated Deadlock Detection Tool** - Uses Banker's Algorithm for safe state analysis.
Supports single and multi-instance resources with resource allocation graph visualization.
""")