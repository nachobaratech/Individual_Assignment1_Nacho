import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
import seaborn as sns
import gspread
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read()

# Authenticate Google Sheets
SERVICE_ACCOUNT_FILE = "JSON_individual-task-453011-2bfd3a329abb.json"
SHEET_ID = "1g3DVcrxEt2jT3oPBAFGJ8G1o4DjgZghChD21ez0ZriM"
SHEET_NAME = "Sheet1"

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# Fetch data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Ensure numerical columns are converted properly
df["bill_length_mm"] = pd.to_numeric(df["bill_length_mm"], errors="coerce")
df["species"] = df["species"].astype(str)

# Compute the average bill length per species
bill_length_avg = df.groupby("species")["bill_length_mm"].mean().to_dict()

# Streamlit UI
st.title("Which Species Has the Longest Bill?")
st.header("This app tests which visualization best answers the question above.")

# Create the state environment for the charts
if 'chart' not in st.session_state:
    st.session_state.chart = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'answered' not in st.session_state:
    st.session_state.answered = None

# Ask the question
st.write("Answer the following question:")
st.write("Which species of penguins has the longest average bill length?")

# Visualization 1: Histogram
def plot_chart_a():
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df, x="bill_length_mm", hue="species", kde=True, ax=ax)
    ax.set_title("Histogram: Distribution of Bill Length Across Species")
    ax.set_xlabel("Bill Length (mm)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Visualization 2: Boxplot
def plot_chart_b():
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x="species", y="bill_length_mm", ax=ax)
    ax.set_title("Boxplot: Bill Length Distribution by Species")
    ax.set_xlabel("Species")
    ax.set_ylabel("Bill Length (mm)")
    st.pyplot(fig)

# Create a button to randomly show a chart after being clicked
if st.button("Show a Chart"):
    st.session_state.chart = random.choice(["A", "B"])
    st.session_state.start_time = time.time()
    st.session_state.answered = False

# Show the chart
if st.session_state.chart:
    if st.session_state.chart == "A":
        plot_chart_a()
    else:
        plot_chart_b()

    # Allow user to select an answer
    species_options = list(bill_length_avg.keys())  # Get species names
    user_answer = st.radio("Which species has the longest average bill length?", species_options)

    # Record the time taken to answer the question
    if st.button("Submit"):
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.answered = True

        # Find the correct answer (species with the longest bill)
        correct_species = max(bill_length_avg, key=bill_length_avg.get)

        if user_answer == correct_species:
            st.success(f"Correct! The {correct_species} penguin has the longest bill. You answered in {elapsed_time:.2f} seconds.")
        else:
            st.error(f"Incorrect. The correct answer is: {correct_species}. You answered in {elapsed_time:.2f} seconds.")

# Streamlit deployment and GitHub repo links (replace with your own)
st.markdown("### [GitHub Repository](https://github.com/nachobaratech/Individual_Assignment1_Nacho.git)")
st.markdown("### [Live Streamlit App](https://your-streamlit-app-url)")

print("hello world")
                                                                       