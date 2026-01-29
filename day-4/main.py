import streamlit as st

# header 
st.header("Bourojju")

# title 
st.title("Akshay")

# subheader 
st.subheader("Anurag university")

# horizontal line
st.markdown("********")

# text 
st.text("Text")

#write
st.write("Hello, welcome to Streamlit!")
st.write(1234)
st.write(["Streamlit", "is", "great!"])
st.write({"name": "babu", "age": 51,"name": "prabhas", "age": 45})
st.write(3.14159)

st.markdown("----------")

#markdown
st.markdown("# This is a markdown header")
st.markdown("**This text is bold**")
st.markdown("*This text is italicized*")
st.markdown("- Item 1\n- Item 2\n- Item 3")
st.markdown("<h3 style='color:blue;'>header</h3>", unsafe_allow_html=True)

#caption
st.caption("This is a caption text.")

#code 
st.code("def add(a,b):" \
"\n    return a + b", language='python')

#latex
st.latex(r"E = mc^2")

#divider method to seperate sections
st.divider()

#button 
if st.button("submit"):
    st.write("Button clicked!")
    st.success("Success message!")
    st.balloons()
else:
    st.write("Button not clicked yet.")
    st.error("Error!")

#text input

name = st.text_input("Enter your name:")
if not name.isalpha():
    st.warning("Please enter a valid name containing only letters.")
else:
    st.write("Hello",name)

#number input
age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)
st.write("your age is ",age)

#feedback
feedback = st.text_area("Provide your feedback:")
st.write("Your feedback:", feedback)

#checkbox
if st.checkbox("I agree to the terms and conditions"):
    st.write("Thank you for agreeing!")
else:
    st.write("You must agree to continue.")
st.divider()

#radio button
gender = st.radio("Select your gender:", ("Male", "Female", "Other"))
st.write("You selected:", gender)   
st.divider()

#selectbox
country = st.selectbox("Select your country:", ["Hyderabad", "kashmir", "India", "Ap"])
st.write("You selected:", country)
st.divider()

#multiselect 
cars = st.multiselect("Select your favorite cars:", ["BMW", "Audi", "Tesla", "Toyota"])
st.write("You selected:", cars)
st.divider()

#slider
satisfaction = st.slider("Rate your satisfaction level:", 0, 10, 1)
st.write("Your satisfaction level is:", satisfaction)
st.divider()

#upload file
uploaded_file = st.file_uploader("Upload a file:")
if uploaded_file is not None:
    st.write("File uploaded:", uploaded_file.name)
else:
    st.write("No file uploaded yet.")
st.divider()

#form method to create a form
with st.form("login"):
    st.write("Enter User detail")
    name = st.text_input("username")
    age = st.text_input("Password")
    submitted = st.form_submit_button("login")
    if submitted:
        st.write("Form submitted!")
        st.write("Name:", name)
        st.write("Age:", age)
st.divider()

#columns method to create columns
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Name ")
    st.text("Bourojju")
with col2:
    st.header("Name")
    st.text("Babu")
with col3:
    st.header("Name")
    st.text("Prabhas")
st.divider()

#create table with table method
import pandas as pd
data = {
    'Name': ['Bourojju', 'Babu', 'Prabhas'],
    'Age': [51, 45, 48],
    'City': ['Hyderabad', 'kashmir', 'India']
}
df = pd.DataFrame(data)
st.table(df)
st.divider()

#sidebar method to create sidebar
st.sidebar.header("Sidebar Example")
sidebar_option = st.sidebar.selectbox("Select an option:", ["Option 1", "Option 2", "Option 3"])
st.sidebar.write("You selected:", sidebar_option)
st.divider()

#cache method to cache results
@st.cache_data
def load_data():
    return[{"name": "Bourojju", "age": 51}, {"name": "Babu", "age": 45}, {"name": "Prabhas", "age": 48}]
data = load_data()
st.write("Cached Data:", data)