"""
generate_notebook.py — Creates the analysis.ipynb Jupyter notebook programmatically.
Run:  python scripts/generate_notebook.py
"""
import json, os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_PATH = os.path.join(PROJECT, "notebooks", "analysis.ipynb")
os.makedirs(os.path.dirname(NB_PATH), exist_ok=True)

def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.split("\n")}

def code(source):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source.split("\n")}

cells = []

# ═══════════════════════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md(
"""# 🌍 Global Military Expenditure Analysis
---
**Subject:** Python for Business — CIA Project  
**Data Source:** [Wikipedia — Countries with Highest Military Expenditures](https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures)  
**Datasets:** SIPRI 2024, IISS 2025, % of GDP rankings  

This notebook performs **Exploratory Data Analysis (EDA)** and **Data Visualization** on global military spending data using `pandas`, `matplotlib`, `seaborn`, and other Python libraries."""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("## 1. Import Libraries"))
cells.append(md("We begin by importing all the necessary Python libraries for data analysis and visualization."))
cells.append(code(
"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import squarify
import warnings

# Configuration
warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid', palette='deep')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 11

print("✅ All libraries imported successfully!")"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — READ DATA
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("## 2. Read the Datasets"))
cells.append(md("""We load four CSV files scraped from Wikipedia. Each dataset provides a different perspective on military spending worldwide.

| Dataset | Description | Rows |
|---------|------------|------|
| `sipri` | Top 40 spenders — SIPRI 2024 | 40 |
| `iiss` | Top 15 spenders — IISS 2025 | 15 |
| `gdp_sipri` | % of GDP — SIPRI 2024 | 25 |
| `gdp_iiss` | % of GDP — IISS 2020 | 15 |"""))
cells.append(code(
"""# Read CSV files
sipri = pd.read_csv('../data/military_spending_sipri_2024.csv')
iiss  = pd.read_csv('../data/military_spending_iiss_2025.csv')
gdp_sipri = pd.read_csv('../data/gdp_pct_sipri_2024.csv')
gdp_iiss  = pd.read_csv('../data/gdp_pct_iiss_2020.csv')

print("✅ All datasets loaded successfully!")
print(f"   SIPRI 2024:      {sipri.shape[0]} rows × {sipri.shape[1]} columns")
print(f"   IISS 2025:       {iiss.shape[0]} rows × {iiss.shape[1]} columns")
print(f"   GDP % (SIPRI):   {gdp_sipri.shape[0]} rows × {gdp_sipri.shape[1]} columns")
print(f"   GDP % (IISS):    {gdp_iiss.shape[0]} rows × {gdp_iiss.shape[1]} columns")"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — VIEW DATAFRAMES
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("## 3. View the DataFrames"))

cells.append(md("### 3.1  First 5 Rows — `head()`"))
cells.append(code("sipri.head()"))

cells.append(md("### 3.2  Last 5 Rows — `tail()`"))
cells.append(code("sipri.tail()"))

cells.append(md("### 3.3  Shape of the DataFrame"))
cells.append(code(
"""print(f"SIPRI shape : {sipri.shape}")
print(f"IISS shape  : {iiss.shape}")
print(f"GDP SIPRI   : {gdp_sipri.shape}")
print(f"GDP IISS    : {gdp_iiss.shape}")"""))

cells.append(md("### 3.4  Column Names"))
cells.append(code("print(sipri.columns.tolist())"))

cells.append(md("### 3.5  Data Types — `dtypes`"))
cells.append(code("sipri.dtypes"))

cells.append(md("### 3.6  DataFrame Info — `info()`"))
cells.append(code("sipri.info()"))

cells.append(md("### 3.7  Summary Statistics — `describe()`"))
cells.append(code("sipri.describe()"))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — DATA CLEANING
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("## 4. Data Cleaning"))
cells.append(md("Check for missing values and duplicate rows."))
cells.append(code(
"""# 4.1 Check for null values
print("=== Null Values ===")
print(sipri.isnull().sum())
print()

# 4.2 Check for duplicates
print("=== Duplicate Rows ===")
print(f"SIPRI duplicates:     {sipri.duplicated().sum()}")
print(f"IISS duplicates:      {iiss.duplicated().sum()}")
print(f"GDP SIPRI duplicates: {gdp_sipri.duplicated().sum()}")
print(f"GDP IISS duplicates:  {gdp_iiss.duplicated().sum()}")"""))

cells.append(md("### 4.1  Verify Data Types & Convert if Needed"))
cells.append(code(
"""# Ensure numeric columns are correct types
sipri['Spending (US$ bn)'] = pd.to_numeric(sipri['Spending (US$ bn)'], errors='coerce')
sipri['% of GDP'] = pd.to_numeric(sipri['% of GDP'], errors='coerce')
sipri['% of global spending'] = pd.to_numeric(sipri['% of global spending'], errors='coerce')

print("✅ Data types verified and cleaned.")
print(sipri.dtypes)"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — INDEXING & SLICING
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("## 5. Indexing & Slicing"))

cells.append(md("### 5.1  Select specific columns"))
cells.append(code("sipri[['Country', 'Spending (US$ bn)']].head(10)"))

cells.append(md("### 5.2  Using `iloc` — position-based indexing"))
cells.append(code(
"""# Select rows 0-4, columns 1-3
sipri.iloc[0:5, 1:4]"""))

cells.append(md("### 5.3  Using `loc` — label-based indexing"))
cells.append(code(
"""# Set Country as index for label-based access
sipri_indexed = sipri.set_index('Country')
sipri_indexed.loc[['United States', 'China', 'India', 'Russia']]"""))

cells.append(md("### 5.4  Boolean Filtering"))
cells.append(code(
"""# Countries spending more than $50 billion
high_spenders = sipri[sipri['Spending (US$ bn)'] > 50]
print(f"Countries spending over $50 bn: {len(high_spenders)}")
high_spenders[['Country', 'Spending (US$ bn)', '% of GDP']]"""))

cells.append(code(
"""# Countries where military spending exceeds 3% of GDP
high_gdp = sipri[sipri['% of GDP'] > 3.0]
print(f"Countries with >3% GDP military spending: {len(high_gdp)}")
high_gdp[['Country', 'Spending (US$ bn)', '% of GDP']]"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — SORTING
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("## 6. Sorting"))

cells.append(md("### 6.1  Sort by Spending (Descending)"))
cells.append(code("sipri.sort_values('Spending (US$ bn)', ascending=False).head(10)"))

cells.append(md("### 6.2  Sort by % of GDP (Descending)"))
cells.append(code("sipri.sort_values('% of GDP', ascending=False).head(10)"))

cells.append(md("### 6.3  Sort by Multiple Columns"))
cells.append(code(
"""sipri.sort_values(['% of GDP', 'Spending (US$ bn)'], ascending=[False, False]).head(10)"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — GROUPBY & AGGREGATION
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("## 7. GroupBy & Aggregation"))
cells.append(md("We add a **Region/Continent** column to group countries and compute aggregate statistics."))
cells.append(code(
"""# Map countries to regions for groupby operations
region_map = {
    'United States': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
    'Brazil': 'South America', 'Colombia': 'South America',
    'China': 'Asia', 'India': 'Asia', 'Japan': 'Asia', 'South Korea': 'Asia',
    'Taiwan': 'Asia', 'Singapore': 'Asia', 'Indonesia': 'Asia', 'Pakistan': 'Asia',
    'Philippines': 'Asia', 'Iran': 'Asia',
    'Russia': 'Europe', 'Germany': 'Europe', 'United Kingdom': 'Europe',
    'Ukraine': 'Europe', 'France': 'Europe', 'Poland': 'Europe', 'Italy': 'Europe',
    'Spain': 'Europe', 'Netherlands': 'Europe', 'Sweden': 'Europe', 'Norway': 'Europe',
    'Denmark': 'Europe', 'Romania': 'Europe', 'Belgium': 'Europe', 'Greece': 'Europe',
    'Finland': 'Europe', 'Switzerland': 'Europe', 'Czech Republic': 'Europe',
    'Turkey': 'Middle East', 'Saudi Arabia': 'Middle East', 'Israel': 'Middle East',
    'Kuwait': 'Middle East', 'Iraq': 'Middle East',
    'Algeria': 'Africa',
    'Australia': 'Oceania'
}

sipri['Region'] = sipri['Country'].map(region_map)
print("✅ Region column added.")
sipri[['Country', 'Region']].head(10)"""))

cells.append(md("### 7.1  Total Spending by Region"))
cells.append(code(
"""region_spending = sipri.groupby('Region')['Spending (US$ bn)'].sum().sort_values(ascending=False)
print("Total Military Spending by Region (US$ bn):")
print(region_spending)"""))

cells.append(md("### 7.2  Mean Spending by Region"))
cells.append(code(
"""region_mean = sipri.groupby('Region')['Spending (US$ bn)'].mean().sort_values(ascending=False)
print("Average Military Spending by Region (US$ bn):")
print(region_mean.round(2))"""))

cells.append(md("### 7.3  Multiple Aggregations with `agg()`"))
cells.append(code(
"""region_stats = sipri.groupby('Region').agg({
    'Spending (US$ bn)': ['sum', 'mean', 'max', 'count'],
    '% of GDP': ['mean', 'max']
}).round(2)

print("Comprehensive Regional Statistics:")
region_stats"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — MERGE & CONCAT
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("## 8. Merge & Concatenate DataFrames"))

cells.append(md("### 8.1  Merge SIPRI and IISS data on Country"))
cells.append(code(
"""# Inner merge — only countries in both datasets
merged = pd.merge(
    sipri[['Country', 'Spending (US$ bn)', '% of GDP']],
    iiss[['Country', 'Spending (US$ bn)']],
    on='Country',
    how='inner',
    suffixes=('_SIPRI', '_IISS')
)
merged['Difference (US$ bn)'] = merged['Spending (US$ bn)_SIPRI'] - merged['Spending (US$ bn)_IISS']
print(f"Countries common to both datasets: {len(merged)}")
merged"""))

cells.append(md("### 8.2  Concatenate GDP % tables"))
cells.append(code(
"""# Concatenate SIPRI and IISS GDP% tables
gdp_sipri_copy = gdp_sipri.copy()
gdp_iiss_copy = gdp_iiss.copy()
gdp_sipri_copy['Source'] = 'SIPRI 2024'
gdp_iiss_copy['Source'] = 'IISS 2020'

gdp_combined = pd.concat([gdp_sipri_copy, gdp_iiss_copy], ignore_index=True)
print(f"Combined GDP % dataset: {gdp_combined.shape[0]} rows")
gdp_combined.head(10)"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — BAR CHART
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 9. Visualization — Bar Chart
Bar charts are ideal for comparing discrete categories. We'll plot the top 10 military spenders."""))

cells.append(md("### 9.1  Vertical Bar Chart — Top 10 Spenders"))
cells.append(code(
"""top10 = sipri.nlargest(10, 'Spending (US$ bn)')

fig, ax = plt.subplots(figsize=(12, 6))
colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, 10))
bars = ax.bar(top10['Country'], top10['Spending (US$ bn)'], color=colors, edgecolor='black', linewidth=0.5)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'${height:.0f}B', ha='center', va='bottom', fontweight='bold', fontsize=9)

ax.set_title('Top 10 Countries by Military Spending (SIPRI 2024)', fontsize=14, fontweight='bold')
ax.set_xlabel('Country', fontsize=12)
ax.set_ylabel('Spending (US$ Billion)', fontsize=12)
ax.set_xticklabels(top10['Country'], rotation=45, ha='right')
plt.tight_layout()
plt.show()"""))

cells.append(md("### 9.2  Horizontal Bar Chart — Top 15 Spenders"))
cells.append(code(
"""top15 = sipri.nlargest(15, 'Spending (US$ bn)').iloc[::-1]  # reverse for horizontal

fig, ax = plt.subplots(figsize=(10, 8))
colors = plt.cm.viridis(np.linspace(0.2, 0.9, 15))
bars = ax.barh(top15['Country'], top15['Spending (US$ bn)'], color=colors, edgecolor='black', linewidth=0.3)

for bar in bars:
    width = bar.get_width()
    ax.text(width + 3, bar.get_y() + bar.get_height()/2.,
            f'${width:.0f}B', ha='left', va='center', fontsize=9)

ax.set_title('Top 15 Countries by Military Spending (SIPRI 2024)', fontsize=14, fontweight='bold')
ax.set_xlabel('Spending (US$ Billion)', fontsize=12)
plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10 — PIE CHART
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 10. Visualization — Pie Chart
A pie chart showing the share of **global military spending** for the top 5 countries vs. the rest."""))
cells.append(code(
"""top5 = sipri.nlargest(5, '% of global spending')
others = pd.DataFrame({
    'Country': ['Rest of World'],
    '% of global spending': [100 - top5['% of global spending'].sum()]
})
pie_data = pd.concat([top5[['Country', '% of global spending']], others], ignore_index=True)

fig, ax = plt.subplots(figsize=(9, 9))
explode = [0.05] * len(pie_data)
colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6', '#95a5a6']
wedges, texts, autotexts = ax.pie(
    pie_data['% of global spending'], labels=pie_data['Country'],
    autopct='%1.1f%%', startangle=140, explode=explode,
    colors=colors, textprops={'fontsize': 11},
    pctdistance=0.75, shadow=True
)
for autotext in autotexts:
    autotext.set_fontweight('bold')

ax.set_title('Share of Global Military Spending (2024)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11 — LINE CHART
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 11. Visualization — Line Chart
We compare **SIPRI vs IISS** spending estimates for the countries present in both datasets."""))
cells.append(code(
"""fig, ax = plt.subplots(figsize=(14, 6))

x = range(len(merged))
ax.plot(x, merged['Spending (US$ bn)_SIPRI'], marker='o', linewidth=2,
        label='SIPRI 2024', color='#e74c3c', markersize=8)
ax.plot(x, merged['Spending (US$ bn)_IISS'], marker='s', linewidth=2,
        label='IISS 2025', color='#3498db', markersize=8)

ax.set_xticks(list(x))
ax.set_xticklabels(merged['Country'], rotation=45, ha='right')
ax.set_title('SIPRI 2024 vs IISS 2025: Military Spending Comparison', fontsize=14, fontweight='bold')
ax.set_ylabel('Spending (US$ Billion)', fontsize=12)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 12 — SCATTER PLOT
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 12. Visualization — Scatter Plot
Exploring the relationship between **absolute spending** and **% of GDP**."""))
cells.append(code(
"""fig, ax = plt.subplots(figsize=(12, 7))

scatter = ax.scatter(
    sipri['Spending (US$ bn)'], sipri['% of GDP'],
    s=sipri['% of global spending'] * 200,  # bubble size by global share
    c=sipri['% of GDP'], cmap='YlOrRd',
    alpha=0.7, edgecolors='black', linewidth=0.5
)

# Annotate key countries
for _, row in sipri.head(10).iterrows():
    ax.annotate(row['Country'],
                (row['Spending (US$ bn)'], row['% of GDP']),
                textcoords="offset points", xytext=(5, 5),
                fontsize=8, alpha=0.8)

plt.colorbar(scatter, label='% of GDP', shrink=0.8)
ax.set_title('Military Spending vs % of GDP (Bubble Size = Global Share)', fontsize=14, fontweight='bold')
ax.set_xlabel('Spending (US$ Billion)', fontsize=12)
ax.set_ylabel('% of GDP', fontsize=12)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 13 — HEATMAP
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 13. Visualization — Heatmap (Correlation Matrix)
A heatmap visualizes correlations between numerical variables in the SIPRI dataset."""))
cells.append(code(
"""numeric_cols = sipri[['Spending (US$ bn)', '% of GDP', '% of global spending']].copy()
correlation = numeric_cols.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0,
            square=True, linewidths=2, fmt='.3f',
            annot_kws={'size': 14, 'fontweight': 'bold'})
ax.set_title('Correlation Matrix — Military Spending Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 14 — BOX PLOT
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 14. Visualization — Box Plot
Box plots reveal the distribution, median, quartiles, and outliers in the data."""))
cells.append(code(
"""fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Box plot — Spending
sns.boxplot(y=sipri['Spending (US$ bn)'], ax=axes[0], color='#3498db', width=0.4)
axes[0].set_title('Distribution of Military Spending\\n(US$ Billion)', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Spending (US$ Billion)')

# Box plot — % of GDP
sns.boxplot(y=sipri['% of GDP'], ax=axes[1], color='#e74c3c', width=0.4)
axes[1].set_title('Distribution of Military Spending\\nas % of GDP', fontsize=13, fontweight='bold')
axes[1].set_ylabel('% of GDP')

plt.suptitle('Box Plots — Military Spending Distribution (SIPRI 2024)', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()"""))

cells.append(md("### 14.1  Box Plot by Region"))
cells.append(code(
"""fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=sipri, x='Region', y='Spending (US$ bn)', palette='Set2', ax=ax)
ax.set_title('Military Spending by Region (SIPRI 2024)', fontsize=14, fontweight='bold')
ax.set_xlabel('Region', fontsize=12)
ax.set_ylabel('Spending (US$ Billion)', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 15 — CUSTOM MARKERS & COLORS
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 15. Custom Markers & Colors
This section demonstrates how to customise chart **markers**, **colors**, **labels**, and **styles** — as required for the additional Word document submission."""))

cells.append(md("### 15.1  Custom Line Markers"))
cells.append(code(
"""fig, ax = plt.subplots(figsize=(14, 6))
top8 = sipri.nlargest(8, 'Spending (US$ bn)')

markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h']
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']

for i, (_, row) in enumerate(top8.iterrows()):
    ax.plot(i, row['Spending (US$ bn)'],
            marker=markers[i], color=colors[i],
            markersize=15, linewidth=0, markeredgecolor='black',
            label=row['Country'])

ax.set_xticks(range(len(top8)))
ax.set_xticklabels(top8['Country'], rotation=45, ha='right')
ax.set_title('Custom Markers for Top 8 Military Spenders', fontsize=14, fontweight='bold')
ax.set_ylabel('Spending (US$ Billion)', fontsize=12)
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\\nMarker styles used: o (circle), s (square), ^ (triangle up),")
print("D (diamond), v (triangle down), p (pentagon), * (star), h (hexagon)")"""))

cells.append(md("### 15.2  Custom Color Palettes"))
cells.append(code(
"""fig, axes = plt.subplots(2, 2, figsize=(14, 10))
top10 = sipri.nlargest(10, 'Spending (US$ bn)')

# Palette 1 — Viridis
axes[0, 0].barh(top10['Country'], top10['Spending (US$ bn)'],
                color=plt.cm.viridis(np.linspace(0.2, 0.9, 10)))
axes[0, 0].set_title('Viridis Palette', fontweight='bold')
axes[0, 0].invert_yaxis()

# Palette 2 — Plasma
axes[0, 1].barh(top10['Country'], top10['Spending (US$ bn)'],
                color=plt.cm.plasma(np.linspace(0.2, 0.9, 10)))
axes[0, 1].set_title('Plasma Palette', fontweight='bold')
axes[0, 1].invert_yaxis()

# Palette 3 — Seaborn Pastel
axes[1, 0].barh(top10['Country'], top10['Spending (US$ bn)'],
                color=sns.color_palette('pastel', 10))
axes[1, 0].set_title('Seaborn Pastel', fontweight='bold')
axes[1, 0].invert_yaxis()

# Palette 4 — Custom Hex Colors
custom_hex = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
              '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
axes[1, 1].barh(top10['Country'], top10['Spending (US$ bn)'],
                color=custom_hex)
axes[1, 1].set_title('Custom Hex Palette', fontweight='bold')
axes[1, 1].invert_yaxis()

plt.suptitle('Same Data — Different Color Palettes', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()"""))

cells.append(md("### 15.3  Changing Bar Colors & Adding Patterns"))
cells.append(code(
"""fig, ax = plt.subplots(figsize=(12, 6))
top5 = sipri.nlargest(5, 'Spending (US$ bn)')
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
hatches = ['/', '\\\\', 'x', '.', 'o']

bars = ax.bar(top5['Country'], top5['Spending (US$ bn)'], color=colors,
              edgecolor='black', linewidth=1.5)

for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)

ax.set_title('Top 5 Spenders with Custom Colors & Hatch Patterns',
             fontsize=14, fontweight='bold', fontstyle='italic')
ax.set_ylabel('Spending (US$ Billion)', fontsize=12, fontfamily='serif')
ax.set_xlabel('Country', fontsize=12, fontfamily='serif')
plt.tight_layout()
plt.show()

print("\\nHatch patterns used: / (diagonal), \\\\\\\\ (back diagonal), x (cross), . (dots), o (circles)")"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 16 — BONUS: TREEMAP
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 16. 🎯 Bonus: Treemap Visualization
A treemap shows proportional areas — larger spending countries get larger rectangles. This uses the `squarify` library."""))
cells.append(code(
"""fig, ax = plt.subplots(figsize=(16, 9))
top20 = sipri.nlargest(20, 'Spending (US$ bn)')

labels = [f"{row['Country']}\\n${row['Spending (US$ bn)']:.0f}B" for _, row in top20.iterrows()]
sizes = top20['Spending (US$ bn)'].values
colors = plt.cm.RdYlGn_r(np.linspace(0.15, 0.85, len(sizes)))

squarify.plot(sizes=sizes, label=labels, color=colors,
              alpha=0.85, edgecolor='white', linewidth=2,
              text_kwargs={'fontsize': 9, 'fontweight': 'bold'})

ax.set_title('Treemap of Military Spending — Top 20 Countries (SIPRI 2024)',
             fontsize=16, fontweight='bold', pad=20)
ax.axis('off')
plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 17 — BONUS: STACKED BAR CHART
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 17. 🎯 Bonus: Stacked Bar — SIPRI vs IISS Comparison
A grouped bar chart comparing how two different research institutes estimate military spending for the same countries."""))
cells.append(code(
"""fig, ax = plt.subplots(figsize=(14, 7))

x = np.arange(len(merged))
width = 0.35

bars1 = ax.bar(x - width/2, merged['Spending (US$ bn)_SIPRI'], width,
               label='SIPRI 2024', color='#e74c3c', edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x + width/2, merged['Spending (US$ bn)_IISS'], width,
               label='IISS 2025', color='#3498db', edgecolor='black', linewidth=0.5)

ax.set_xticks(x)
ax.set_xticklabels(merged['Country'], rotation=45, ha='right')
ax.set_title('SIPRI 2024 vs IISS 2025: Side-by-Side Comparison',
             fontsize=14, fontweight='bold')
ax.set_ylabel('Spending (US$ Billion)', fontsize=12)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)

# Add difference annotations for top 5
for i in range(min(5, len(merged))):
    diff = merged['Difference (US$ bn)'].iloc[i]
    max_val = max(merged['Spending (US$ bn)_SIPRI'].iloc[i], merged['Spending (US$ bn)_IISS'].iloc[i])
    ax.annotate(f'+${diff:.0f}B' if diff > 0 else f'${diff:.0f}B',
                (i, max_val + 5), ha='center', fontsize=8, fontweight='bold',
                color='green' if diff > 0 else 'red')

plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 18 — BONUS: RADAR CHART
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md("""## 18. 🎯 Bonus: Radar (Spider) Chart
A radar chart comparing multiple metrics for selected countries. We normalise each metric to 0–1 scale for fair comparison."""))
cells.append(code(
"""from math import pi

# Select top 5 countries for radar comparison
radar_countries = ['United States', 'China', 'Russia', 'India', 'United Kingdom']
radar_df = sipri[sipri['Country'].isin(radar_countries)].copy()

# Metrics to compare (normalised 0-1)
metrics = ['Spending (US$ bn)', '% of GDP', '% of global spending']
for col in metrics:
    radar_df[col + '_norm'] = radar_df[col] / radar_df[col].max()

categories = ['Absolute\\nSpending', '% of\\nGDP', '% of Global\\nSpending']
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']

for i, (_, row) in enumerate(radar_df.iterrows()):
    values = [row[col + '_norm'] for col in metrics]
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=row['Country'], color=colors[i])
    ax.fill(angles, values, alpha=0.1, color=colors[i])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
ax.set_title('Radar Chart — Top 5 Military Powers\\n(Normalised Metrics)',
             fontsize=14, fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
plt.tight_layout()
plt.show()"""))

# ═══════════════════════════════════════════════════════════════════════════════
# CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
cells.append(md(
"""## 📋 Summary & Key Findings

### Key Observations:
1. **The United States dominates** global military spending at **$997 billion** (35.5% of global total).
2. The **top 5 countries** account for over **58%** of all military spending worldwide.
3. **Ukraine** has the highest spending as a % of GDP (**34%**) due to the ongoing conflict.
4. **SIPRI and IISS** estimates differ notably — SIPRI generally reports higher figures.
5. **Regional patterns**: North America and Asia lead, followed by Europe and the Middle East.

### Techniques Demonstrated:
| Category | Techniques |
|----------|-----------|
| **EDA** | head, tail, shape, info, describe, dtypes, isnull, duplicated, groupby, agg, merge, concat, sort_values, iloc, loc, boolean filtering |
| **Visualization** | Bar chart, Horizontal bar, Pie chart, Line chart, Scatter plot, Heatmap, Box plot, Treemap, Grouped bar, Radar chart |
| **Customisation** | Custom markers (o, s, ^, D, v, p, *, h), color palettes (viridis, plasma, pastel, hex), hatch patterns, font styles, annotations |

---
*Data Source: [Wikipedia — Countries with Highest Military Expenditures](https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures)*"""))

# ─── Build notebook JSON ─────────────────────────────────────────────────────
# Fix: each source line needs \n at the end
for cell in cells:
    lines = cell["source"]
    cell["source"] = [line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"Notebook created: {NB_PATH}")
print(f"Total cells: {len(cells)}")
