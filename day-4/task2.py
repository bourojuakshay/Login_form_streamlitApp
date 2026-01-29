import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Student CRUD App", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("📚 Student Management System")
st.markdown("---")

# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "VFFarmy@123"
DB_NAME = "Student_db"
DB_TABLE = "Student"

# Function to create database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Function to execute query
def execute_query(query, data=None):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        st.error(f"Error executing query: {e}")
        return False

# Function to fetch data
def fetch_all_students():
    conn = get_db_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {DB_TABLE}")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        st.error(f"Error fetching data: {e}")
        return []

# Function to fetch student by ID
def fetch_student_by_id(student_id):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {DB_TABLE} WHERE id = %s", (student_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        st.error(f"Error fetching data: {e}")
        return None

# Sidebar Navigation
st.sidebar.title("🎯 Navigation")
operation = st.sidebar.radio("Select Operation", ["📖 Read", "➕ Create", "✏️ Update", "❌ Delete"])

st.sidebar.markdown("---")
st.sidebar.info("Select an operation from above to manage student records.")

# READ Operation
if operation == "📖 Read":
    st.header("📖 View All Students")
    
    students = fetch_all_students()
    
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📊 Total Students: {len(students)}")
        with col2:
            if st.button("🔄 Refresh"):
                st.rerun()
    else:
        st.warning("No students found in the database.")
    
    st.markdown("---")
    st.subheader("🔍 Search Student by ID")
    search_id = st.number_input("Enter Student ID:", min_value=1, step=1)
    if st.button("Search"):
        student = fetch_student_by_id(search_id)
        if student:
            st.success("✅ Student Found!")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ID", student['id'])
            with col2:
                st.metric("Name", student['name'])
            with col3:
                st.metric("Age", student['age'])
        else:
            st.error("❌ Student not found!")

# CREATE Operation
elif operation == "➕ Create":
    st.header("➕ Add New Student")
    
    with st.form("create_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            student_id = st.number_input("Student ID:", min_value=1, step=1)
        with col2:
            student_name = st.text_input("Student Name:")
        with col3:
            student_age = st.number_input("Student Age:", min_value=1, max_value=100, step=1)
        
        submit_button = st.form_submit_button("✅ Add Student", use_container_width=True)
    
    if submit_button:
        if student_id and student_name and student_age:
            # Check if ID already exists
            existing_student = fetch_student_by_id(student_id)
            if existing_student:
                st.error("❌ Student ID already exists!")
            else:
                query = f"INSERT INTO {DB_TABLE} (id, name, age) VALUES (%s, %s, %s)"
                if execute_query(query, (student_id, student_name, student_age)):
                    st.success("✅ Student added successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to add student!")
        else:
            st.warning("⚠️ Please fill all fields!")

# UPDATE Operation
elif operation == "✏️ Update":
    st.header("✏️ Update Student Information")
    
    students = fetch_all_students()
    
    if students:
        student_ids = [s['id'] for s in students]
        selected_id = st.selectbox("Select Student ID to Update:", student_ids)
        
        student = fetch_student_by_id(selected_id)
        
        if student:
            st.info(f"Current Info - ID: {student['id']}, Name: {student['name']}, Age: {student['age']}")
            
            with st.form("update_form"):
                new_name = st.text_input("New Name:", value=student['name'])
                new_age = st.number_input("New Age:", min_value=1, max_value=100, step=1, value=student['age'])
                
                submit_button = st.form_submit_button("✅ Update Student", use_container_width=True)
            
            if submit_button:
                query = f"UPDATE {DB_TABLE} SET name = %s, age = %s WHERE id = %s"
                if execute_query(query, (new_name, new_age, selected_id)):
                    st.success("✅ Student updated successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to update student!")
    else:
        st.warning("No students available to update!")

# DELETE Operation
elif operation == "❌ Delete":
    st.header("❌ Delete Student")
    
    students = fetch_all_students()
    
    if students:
        student_ids = [s['id'] for s in students]
        selected_id = st.selectbox("Select Student ID to Delete:", student_ids)
        
        student = fetch_student_by_id(selected_id)
        
        if student:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ID", student['id'])
            with col2:
                st.metric("Name", student['name'])
            with col3:
                st.metric("Age", student['age'])
            
            st.warning("⚠️ Warning: This action cannot be undone!")
            
            if st.button("🗑️ Delete Student", use_container_width=True):
                query = f"DELETE FROM {DB_TABLE} WHERE id = %s"
                if execute_query(query, (selected_id,)):
                    st.success("✅ Student deleted successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to delete student!")
    else:
        st.warning("No students available to delete!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Student Management System | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
