import streamlit as st
import mysql.connector
import pandas as pd

# ---------- DB Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="VFFarmy@123",
        autocommit=True
    )

conn = get_connection()
cursor = conn.cursor(buffered=True)

# ---------- Setup DB ----------
cursor.execute("CREATE DATABASE IF NOT EXISTS LoginDB")
cursor.execute("USE LoginDB")

cursor.execute("""
CREATE TABLE IF NOT EXISTS User_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(50)
)
""")

# ---------- Sidebar Navigation ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Register", "Login", "All Users","Profile"])

# ================= HOME PAGE =================
if page == "Home":
    st.title("Home Page")
    st.subheader("Welcome to the System")
    st.write("Use sidebar to Register or Login")

#REGISTER PAGE
elif page == "Register":
    st.title("Register Page")

    def register_user(name, email, password):
        cursor.execute(
            "INSERT INTO User_details (name,email, password) VALUES (%s,%s,%s)",
            (name, email, password)
        )
        conn.commit()
        st.success("✅ User registered successfully!")

    reg_name = st.text_input("Enter your name", key="reg_name")
    reg_email = st.text_input("Enter your email", key="reg_email")
    reg_password = st.text_input("Enter your password", type="password", key="reg_pass")

    if st.button("Register"):
        if reg_name and reg_email and reg_password:
            register_user(reg_name, reg_email, reg_password)
        else:
            st.warning("⚠ Please fill all fields")

# LOGIN PAGE 
elif page == "Login":
    st.title("Login Page")

    def login_user(name, email, password):
        cursor.execute(
            "SELECT * FROM User_details WHERE name=%s AND email=%s AND password=%s",
            (name, email, password)
        )
        result = cursor.fetchone()
        if result:
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid credentials")

    login_name = st.text_input("Enter your name", key="login_name")
    login_email = st.text_input("Enter your email", key="login_email")
    login_password = st.text_input("Enter your password", type="password", key="login_pass")

    if st.button("Login"):
        if login_name and login_email and login_password:
            login_user(login_name, login_email, login_password)
        else:
            st.warning("⚠ Please fill all fields")

# ================= ALL USERS PAGE =================
elif page == "All Users":
    st.title("📄 All Registered Users")

    if st.button("Show Users"):
        cursor.execute("SELECT * FROM User_details")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["ID", "Name", "Email", "Password"])
        st.dataframe(df)
# ================= PROFILE PAGE =================
elif page == "Profile":
    st.title("👤 User Profile")
    