import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import altair as alt
from google import genai

FILE_PATH = "/Users/sahilalyakhtar/Desktop/PROJECTS/ensamble/career_cluster_data/user_data.csv"
PROMPT_FILE = "prompt.txt"

def initialize_genai_client():
    """Initializes the GenAI client."""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    if not client:
        st.error("API key not found.")
        st.stop()
    return client

def setup_streamlit_ui():
    """Sets up the Streamlit UI elements and returns user input."""
    st.set_page_config(page_title="ensamble.ai", page_icon=":tada:", layout="wide")
     # Apply CSS for rounded corner rectangle behind the title
    st.markdown(
        """
        <style>
        .title-wrapper {
            background-color: #13367d; /* Background color */
            font-size: 1.5em; /* Adjust the size as needed */
            padding: 0.5em 1em; /* Padding around the title */
            border-radius: 25px; /* Rounded corners */
            display: inline-block; /* Make the background fit the title */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="title-wrapper">ensamble_sociolytics</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    

    #st.sidebar.success("Home")
    st.markdown("<br>", unsafe_allow_html=True)  # to get blank lines
    st.write(" ## find your tribe!!!")
    st.write(
        "This is an AI tool that help you connect with people based on shared interests."
    )

    name = st.text_input("Name:")
    st.write("Please write in brief your career goals and values ;)")

    user_input = st.text_area("Start here!", height=150)
    word_count = len(user_input.split()) if user_input else 0  # for showing live word count
    st.write(f"word count:{word_count}")
    return name, user_input

def generate_ai_response(client, name, user_input, prompt_file):
    """Generates the AI response using the GenAI model."""
    try:
        with open(prompt_file, "r") as file:
            file_contents = file.read()
        prompt = file_contents.replace("{user_input}", user_input).replace("{name}", name)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text
    except FileNotFoundError:
        st.error(f"Prompt file '{prompt_file}' not found.")
        st.stop()
    except Exception as e:
        st.error(f"Error generating AI response: {e}")
        st.stop()

def String_to_dict(response_text):
    """ converts string like str:int to {str:int} i.e dictionary format"""
    response_dict={}
    response_element_list = response_text.split(',')
    for element in response_element_list:
        try:
            key,value = element.split(':')
            response_dict[key.strip()] = int(value.strip())
        except ValueError:
            continue
    return response_dict

def create_donut_chart(response_text, title="Strengths Donut Chart"):
    """
    Creates and displays a donut chart using the provided strengths dictionary {"str":int}.
    """
    response_dict=String_to_dict(response_text)
    labels = list(response_dict.keys())
    values = list(response_dict.values())

    col1, col2 = st.columns([1.5, 1]) #for setting layout
   
    #using altair
    with col1:
        source = pd.DataFrame({
        "Field of Interests": labels,
        "value": values })

        chart = alt.Chart(source).mark_arc(innerRadius=70).encode(
        theta="value:Q",
        color="Field of Interests:N",)
        st.altair_chart(chart , use_container_width=True)

def display_results(name, user_input, response_text):
    """Displays the results in the Streamlit app."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write(response_text)
   
    #creating donut chart
   
    create_donut_chart(response_text)

    df = pd.DataFrame(
        {"name": [name], "user_text": [user_input], "ai_summary": [response_text]}
    )
    st.write("Your input:")
    st.dataframe(df)

def save_data_to_csv(name, user_input, response_text, file_path):
    """Saves the data to the CSV file."""
    df = pd.DataFrame(
        {"name": [name], "user_text": [user_input], "ai_summary": [response_text]}
    )
    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)
    st.success(f"Your response has been saved.")

def main():
    """Main function to run the Streamlit app."""
    client = initialize_genai_client()
    name, user_input = setup_streamlit_ui()

    if st.button("Submit"):
        if name.strip() and user_input.strip():
            with st.spinner("Please wait, Analysis may take 1-2 minutes..."):
                time.sleep(1)
                response_text = generate_ai_response(client, name, user_input, PROMPT_FILE)
            display_results(name, user_input, response_text)
            save_data_to_csv(name, user_input, response_text, FILE_PATH)
        else:
            st.warning("Please enter some text first!")

if __name__ == "__main__":
    main()