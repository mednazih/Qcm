import streamlit as st
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime


def add_question_to_database(question_data):
    ref = db.reference('/questions')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Push the question data to the 'questions' node with timestamp as key
    ref.child(timestamp).set(question_data)

# Function to save dictionary to JSON file
def add_to_json(data):
    # Generate a unique key using the current timestamp
    key = datetime.now().strftime("%Y/%m/%d/%H:%M:%S")

    # Load existing data from the JSON file
    try:
        with open('data.json', 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}

    # Add the new data with the generated key
    existing_data[key] = data

    # Write the updated data back to the JSON file
    with open('data.json', 'w') as file:
        json.dump(existing_data, file)


def main():
    if not firebase_admin._apps:
        cred = credentials.Certificate("qcms-c2f47-firebase-adminsdk-yuuay-25ef959b57.json")
        firebase_admin.initialize_app(cred,{'databaseURL': 'https://qcms-c2f47-default-rtdb.firebaseio.com/'})


    st.title("Multiple Choice Question Platform")

    # Input question
    question = st.text_input("Enter the question:")

    # Number of options
    num_options = st.number_input("Number of options:", min_value=2, max_value=6, value=2, step=1)

    # Create a dictionary to store question, options, and explanations
   
    option_dict={}
    data={}
    # Add input fields for options and explanations
    for i in range(num_options):
        option_key = f"option_{i+1}"
        explanation_key = f"explanation_{i+1}"
        is_correct_key = f"is_correct_{i+1}"

        option = st.text_input(f"Option {i+1}:",key=option_key)
        explanation = st.text_input(f"Explanation {i+1}:",key=explanation_key)
        is_correct = st.checkbox(f"Correct Option {i+1}",key=is_correct_key)
        
        option_dict[option_key] = {"option":option,"explanation": explanation, "is_correct": is_correct}
    
    data = {f"Question": question,"Options": option_dict}
    #add_to_json(data)
    # Button to display the collected data
    if st.button("Show Data"):
        # Add the question to the database
        add_question_to_database(data)
        st.write("Collected Data:")
        st.write(data)

if __name__ == "__main__":
    main()
