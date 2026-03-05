# PYTHON CIA II - Global Military Expenditure Analysis

**Class:** 4 BBA FIB B
**Teacher:** DR. Avisek Kundu

### Team Members
*   **Varshith Sai** - 2423672
*   **Kaushik G L** - 2423634
*   **Raunak** - 2423659
*   **Ananya Dubey** - 2423610
*   **Mishkha Kumar** - 2423644
*   **Akshath Kumar** - 2423608

---

## Project Overview
This project is an end-to-end Python data analysis pipeline that investigates global military expenditure. We extracted, cleaned, analyzed, and visualized military spending data to understand global trends and compare different research estimates.

## What We Did

### 1. Data Collection (`scripts/scrape_data.py`)
We built a Python web scraper using the `requests` and `pandas` libraries to programmatically extract military expenditure data directly from Wikipedia. 
The script successfully pulled data from two major sources:
*   **SIPRI (Stockholm International Peace Research Institute) 2024:** Top 40 spending nations and military spending as a % of GDP.
*   **IISS (International Institute for Strategic Studies) 2025:** Top 15 spending nations and historical % of GDP spending.
These datasets were cleaned and exported as four separate CSV files in our `data/` directory.

### 2. Exploratory Data Analysis (EDA) & Visualization (`notebooks/analysis.ipynb`)
We used a Python script (`scripts/generate_notebook.py`) to construct our main analytical Jupyter Notebook. The notebook utilizes `pandas`, `matplotlib`, `seaborn`, and `squarify` to perform comprehensive EDA.
*   **Data Cleaning & Manipulation:** We handled missing values, converted data types, merged dataframes (to compare SIPRI vs IISS), and grouped data by geographic regions.
*   **Visualizations:** We generated 10 different types of charts to uncover insights:
    *   Vertical & Horizontal Bar Charts (Top spenders)
    *   Pie Charts (Global spending share)
    *   Line Charts (Comparing SIPRI and IISS estimates side-by-side)
    *   Scatter / Bubble Plots (Absolute spending vs % of GDP)
    *   Correlation Heatmaps
    *   Box Plots (Distribution of spending by region)
    *   Treemaps (Proportional area of the top 20 spenders)
    *   Grouped Bar Charts (Direct comparison of estimates)
    *   Radar / Spider Charts (Multi-metric comparison of the top 5 powers)

### 3. Custom Formatting & Documentation (`docs/additional_codes.docx`)
To fulfill specific formatting requirements, we used the `python-docx` library to programmatically generate a Microsoft Word document (`scripts/generate_docx.py`). This document details the custom markers, colors, hatch patterns, and font stylings applied to our charts using Times New Roman 12pt formatting.

### 4. Interactive Dashboard (`app/app.py`)
To make our findings accessible and interactive, we built a web dashboard using the **Streamlit** framework and **Plotly** for interactive graphs.
The dashboard allows users to:
*   Switch between SIPRI and IISS datasets.
*   Filter the number of top countries displayed.
*   Change the types of charts (Bar, Pie, Scatter, Treemap) and their color schemes in real-time.
*   View the raw data tables and summary statistics.
*   Compare the differing estimates between the two research institutes dynamically.

## Key Findings
1.  **The United States** is the undisputed leader in military spending at **$997 billion**, accounting for 35.5% of the entire world's military expenditure.
2.  The top 5 nations (US, China, Russia, Germany, India) account for over 58% of all global spending.
3.  **Ukraine** currently has the highest military spending relative to its economic size, allocating over 34% of its GDP to defense due to the ongoing conflict.
4.  There are notable discrepancies between research institutes; SIPRI generally estimates higher spending figures compared to IISS for the same nations.
