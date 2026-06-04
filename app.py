import streamlit as st
import pandas as pd
import pdfplumber
import re
import matplotlib.pyplot as plt

st.title("Student Result Analysis Dashboard")

uploaded_files = st.file_uploader(
    "Upload Student Marksheets",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    all_data = []

    pattern = r'([A-Z]{2,3}\d+)-\s*\[[TP]\]\s+\d+\s+\d+\s+([A-Z]\+?)'

    for uploaded_file in uploaded_files:

        text = ""

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        matches = re.findall(pattern, text)

        student_name = uploaded_file.name.replace(".pdf", "")

        for subject, grade in matches:

            all_data.append([
                student_name,
                subject,
                grade
            ])

    df = pd.DataFrame(
        all_data,
        columns=["Student", "Subject", "Grade"]
    )

    st.success(f"{len(uploaded_files)} marksheets processed")

    subject = st.selectbox(
        "Select Subject",
        sorted(df["Subject"].unique())
    )

    subject_df = df[df["Subject"] == subject]

    grade_count = subject_df["Grade"].value_counts()

    st.subheader(f"{subject} Grade Distribution")

    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        grade_count.values,
        labels=grade_count.index,
        autopct='%1.1f%%',
        startangle=90
    )

    st.pyplot(fig)

    st.subheader("Student Records")

    st.dataframe(subject_df)
