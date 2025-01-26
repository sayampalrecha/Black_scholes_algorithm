import streamlit as st
from PIL import Image
import pandas as pd




# Header
st.title("About Me")



st.header("Sayam Palrecha")
st.write("""
    I am Sayam Palrecha, recently admitted to the M.S Data Science program at George Washington University (GWU) joining this Fall.

    I possess a strong foundation in Machine Learning thanks to my experience in two research internships.

    My key strengths include: Deep Neural Networks based algorithms (Worked on Computer Vision and ML projects)

    Leadership and communication (Lead the project team and AI-ML lead of the college AI club) making me an all-around and worthy candidate.
""")

# Skills section
st.header("Skills")
col4, col5 = st.columns(2)

with col4:
    st.subheader("Scripting Language")
    st.write("""
    - Python (Machine Learning and Deep Learning Libraries)
    - C++
    - SQL (MySQL)
    - R Programming Language (RStudio)
    - NoSQL (Graph Database)
    """)

with col5:
    st.subheader("Soft Skills")
    st.write("""
    - Team Leadership
    - Project Management
    - Problem Solving
    - Communication
    - Quantitative Reasoning
    """)

# Experience Timeline
st.header("Experience")
experience = {
    "June 2023- September 2023": "Medical Intern at Carnegie Mellon University",

    "Jan 2023- May 2023": "Medical Research Intern IIT-Roorke",
}

for period, role in experience.items():
    st.write(f"**{period}**")
    st.write(role)
    st.write("---")

# Projects
st.header("Featured Projects")
with st.expander("Market Strategy and Visualization of Portfolio Returns using ML"):
    st.write("""
    - Sourced historical stock price data for S&P 500 using YFinance api. Cleaned data to minimize error by 12%
    - Calculated Fama-french curve and rolling average for each stock to identify features for clustering and portfolio optimization
    - Implement a K-Means clustering algorithm to group stocks based feature similarities
    - Construct portfolios using a mean-variance optimization framework to maximize the Sharpe ratio, backtest portfolios against
    benchmark index like S&P500 to evaluate their historical performance and risk-adjusted returns
    """)
    # st.image("")

with st.expander("WeedGuard- Smart Weed Detection Using Computer Vision "):
    st.write("""
    - Full-stack Computer Vision project that can identify weed, decreasing overall crop wastage by 12% in rural India
    - Applied YOLOv5 for model building which had an accuracy of 88.34% mean loss error of about 0.45
    - Conducted EDA 1000 image dataset and annotated data by CVAT reducing outliers by 5% and increased data quality by 22%
    """)


# Contact Form
st.header("Get in Touch")
contact_form = st.form("contact_form")
with contact_form:
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submit = st.form_submit_button("Send Message")

if submit:
    st.success("Thanks for reaching out! I'll get back to you soon.")

# Footer
st.markdown("---")
st.markdown("Connect with me on [LinkedIn](https://www.linkedin.com/in/sayampalrecha/) | [GitHub](https://github.com/sayampalrecha)")
