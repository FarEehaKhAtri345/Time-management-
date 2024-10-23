import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Create a session state to hold task data
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Function to start a task
def start_task(task_name):
    start_time = time.time()  # Record the start time
    return task_name, start_time

# Function to end a task
def end_task(task_name, start_time):
    end_time = time.time()  # Record the end time
    duration = end_time - start_time  # Calculate duration
    task_info = {
        'Task': task_name,
        'Start Time': datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'),
        'End Time': datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S'),
        'Duration (seconds)': round(duration, 2)
    }
    return task_info

# Streamlit UI
st.title("Time Management App")

# Input for task name
task_name = st.text_input("Enter Task Name")

# Button to start a task
if st.button("Start Task"):
    if task_name:
        task_name, start_time = start_task(task_name)
        st.session_state.current_task = (task_name, start_time)
        st.success(f"Task '{task_name}' started!")
    else:
        st.warning("Please enter a task name.")

# Button to end a task
if st.button("End Task"):
    if 'current_task' in st.session_state:
        task_name, start_time = st.session_state.current_task
        task_info = end_task(task_name, start_time)
        st.session_state.tasks.append(task_info)
        st.session_state.current_task = None
        st.success(f"Task '{task_name}' ended!")
    else:
        st.warning("No task is currently running.")

# Display the task log
if st.session_state.tasks:
    task_df = pd.DataFrame(st.session_state.tasks)
    st.subheader("Task Log")
    st.dataframe(task_df)

# Button to download the task log
if st.button("Download Log as CSV"):
    if st.session_state.tasks:
        task_df.to_csv('time_management_log.csv', index=False)
        st.success("Log saved as 'time_management_log.csv'")
    else:
        st.warning("No tasks to save.")
