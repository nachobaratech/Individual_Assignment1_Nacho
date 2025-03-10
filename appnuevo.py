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

# This ensures that the numerical columns are converted properly
df["bill_length_mm"] = pd.to_numeric(df["bill_length_mm"], errors="coerce")
df["species"] = df["species"].astype(str)

# This computes the average bill length per species
bill_length_avg = df.groupby("species")["bill_length_mm"].mean().to_dict()

# Streamlit UI
st.title("Which Species Has the Longest Bill?")

# This creates the state environment for the charts
if 'chart' not in st.session_state:
    st.session_state.chart = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'answered' not in st.session_state:
    st.session_state.answered = None

# Asks the question related to the dataset chosen
st.write("Answer the following question:")
st.write("Which species of penguins has the longest average bill length?")

# This is the code for visualization 1:  A Histogram
def plot_chart_a():
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df, x="bill_length_mm", hue="species", kde=True, ax=ax)
    ax.set_title("Histogram: Distribution of Bill Length Across Species")
    ax.set_xlabel("Bill Length (mm)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

def plot_chart_d():
    fig, ax = plt.subplots(figsize=(10, 5))
    species_list = list(bill_length_avg.keys())
    avg_lengths = list(bill_length_avg.values())

    ax.plot(species_list, avg_lengths, marker="o", linestyle="-", color="blue", linewidth=2, markersize=8)
    ax.set_title("Trend of Average Bill Length Across Species")
    ax.set_xlabel("Species")
    ax.set_ylabel("Average Bill Length (mm)")
    ax.grid(True)
    st.pyplot(fig)

# This is the code for visualization 2: A Boxplot
def plot_chart_b():
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x="species", y="bill_length_mm", ax=ax)
    ax.set_title("Boxplot: Bill Length Distribution by Species")
    ax.set_xlabel("Species")
    ax.set_ylabel("Bill Length (mm)")
    st.pyplot(fig)

def plot_chart_c():
    fig, ax = plt.subplots(figsize=(10, 5))
    species_list = list(bill_length_avg.keys())
    avg_lengths = list(bill_length_avg.values())

    sns.barplot(x=species_list, y=avg_lengths, ax=ax, palette="viridis")
    ax.set_title("Average Bill Length per Species")
    ax.set_xlabel("Species")
    ax.set_ylabel("Average Bill Length (mm)")
    st.pyplot(fig)


# This creates a button to randomly show a chart after being clicked
if st.button("Show a Chart"):
    st.session_state.chart = random.choice(["A", "B"])
    st.session_state.start_time = time.time()
    st.session_state.answered = False

# This shows the chart
if st.session_state.chart:
    if st.session_state.chart == "A":
        plot_chart_a()
    elif st.session_state.chart == "B":
        plot_chart_b()
    elif st.session_state.chart == "C":
        plot_chart_c()
    else: 
        plot_chart_d()


 
    # This records the time taken to answer the question by the user 
    if st.button("I Submitted my Answer"):
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.answered = True

        # This finds the correct answer (species with the longest bill)
        correct_species = max(bill_length_avg, key=bill_length_avg.get)
        st.success(f"Congrats, you have answered the question in {elapsed_time:.2f} seconds")

# This is the streamlit deployment and GitHub repo links
st.markdown("[GitHub Repository](https://github.com/nachobaratech/Individual_Assignment1_Nacho.git)")
st.markdown("[Live Streamlit App](https://individual-assignment1.streamlit.app/)")
                                                                       