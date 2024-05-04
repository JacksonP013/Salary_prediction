import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

# loading data=============================
@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel","YearsCodePro", "Employment", "ConvertedCompYearly","DevType","Industry"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 200000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    df['Country'] = df['Country'].replace({'United Kingdom of Great Britain and Northern Ireland': 'UK'})
    data = df["Country"].value_counts()

    
    fig1, ax1 = plt.subplots()
    # Customize pie chart design
    colors = plt.cm.tab20c(np.linspace(0, 1, len(data)))  # Use tab20c color map for more colors

    fig, ax = plt.subplots()
    ax.bar(data.index, data, color=colors)


    explode = [0.1] * len(data)  # explode all slices
    ax1.pie(data, labels=None, autopct="%1.1f%%", shadow=True, startangle=90, colors=colors, explode=explode)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.legend(data.index, loc="center left", bbox_to_anchor=(1, 0.5))  # Display legend

    # Set background color
    fig1.patch.set_facecolor('black')

    # Remove labels on chart
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Display labels in a list beside the chart
    st.write("#### Number of Data from different countries")
    st.write(data)

    st.pyplot(fig1)



# bargraph ==================================


    
    st.write("""
    #### Mean Salary Based On Country
    """)

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)

    # Custom color palette for bars
    colors = plt.cm.tab10(np.linspace(0, 1, len(data)))

    fig, ax = plt.subplots()
    ax.bar(data.index, data, color=colors)

    # Set background color for the entire page
    st.markdown(
        """
        <style>
        body {
            background-color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Set background color for the plot
    fig.patch.set_facecolor('#000000')

    # Customize plot aesthetics
    ax.set_xlabel('Country', color='white')  # X-axis label
    ax.set_ylabel('Mean Salary', color='white')  # Y-axis label
    ax.tick_params(axis='x', colors='white')  # X-axis tick labels color
    ax.tick_params(axis='y', colors='white')  # Y-axis tick labels color
    ax.set_title('Mean Salary Based On Country', color='white')  # Plot title
    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Add gridlines

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Show plot
    st.pyplot(fig)



    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )
    df['Country'] = df['Country'].replace({'United Kingdom of Great Britain and Northern Ireland': 'UK'})
    df['Country'] = df['Country'].replace({'United States of America': 'US'})
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
    

    #multiple line
    chart_data = pd.DataFrame(
        {
            "col1": np.random.randn(20),
            "col1": np.random.randn(20),
            "col1": np.random.randn(20),
        }
    )
    
    
    








    