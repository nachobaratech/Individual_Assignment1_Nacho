import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
import seaborn as sns
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# Ensure numerical columns are converted properly
df["bill_length_mm"] = pd.to_numeric(df["bill_length_mm"], errors="coerce")
df["species"] = df["species"].astype(str)

# Compute the average bill length per species
bill_length_avg = df.groupby("species")["bill_length_mm"].mean().to_dict()

# Streamlit UI
st.title("Which Species Has the Longest Bill?")

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

 
    # Record the time taken to answer the question
    if st.button("I Submitted my Answer"):
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.answered = True

        # Find the correct answer (species with the longest bill)
        correct_species = max(bill_length_avg, key=bill_length_avg.get)
        st.success(f"Congrats, you have answered the question in {elapsed_time:.2f} seconds")

# Streamlit deployment and GitHub repo links (replace with your own)
st.markdown("[GitHub Repository](https://github.com/nachobaratech/Individual_Assignment1_Nacho.git)")
st.markdown("[Live Streamlit App](https://individual-assignment1.streamlit.app/)")
                                                                       