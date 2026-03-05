"""
scrape_data.py — Wikipedia Military Expenditure Scraper
========================================================
Scrapes military expenditure tables from the Wikipedia page:
https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures

Saves four CSV files into the data/ directory:
  1. military_spending_sipri_2024.csv  – Top 40 spenders (SIPRI, 2024)
  2. military_spending_iiss_2025.csv   – Top 15 spenders (IISS, 2025)
  3. gdp_pct_sipri_2024.csv            – Spending as % of GDP (SIPRI, 2024)
  4. gdp_pct_iiss_2020.csv             – Spending as % of GDP (IISS, 2020)

Usage:
  python scripts/scrape_data.py
"""

import os
import re
import pandas as pd
import requests

# ── Configuration ────────────────────────────────────────────────────────────
URL = "https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# ── Helper functions ─────────────────────────────────────────────────────────

def clean_numeric(series):
    """Remove footnotes, brackets, and convert to float."""
    return (
        series.astype(str)
        .str.replace(r"\[.*?\]", "", regex=True)   # remove citation brackets
        .str.replace(r"[^\d.\-]", "", regex=True)   # keep digits, dots, minus
        .pipe(pd.to_numeric, errors="coerce")
    )


def clean_country(series):
    """Clean country names — remove footnotes and extra whitespace."""
    return (
        series.astype(str)
        .str.replace(r"\[.*?\]", "", regex=True)
        .str.replace(r"\(.*?\)", "", regex=True)
        .str.strip()
    )


def scrape_tables():
    """Fetch and parse all military expenditure tables from Wikipedia."""
    print(f"Fetching data from:\n  {URL}\n")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        print("Using hardcoded fallback data instead.")
        return create_fallback_data()
    
    # Parse all tables from the page
    tables = pd.read_html(response.text)
    print(f"Found {len(tables)} tables on the page.\n")
    
    os.makedirs(DATA_DIR, exist_ok=True)
    saved_files = []
    
    # ── Table 1: SIPRI 2024 — Top 40 spenders ────────────────────────────
    for i, df in enumerate(tables):
        cols = [str(c).lower() for c in df.columns]
        col_str = " ".join(cols)
        # Look for the main SIPRI spending table (has spending + % GDP + % global)
        if "spending" in col_str and "gdp" in col_str and "global" in col_str:
            df.columns = ["Rank", "Country", "Spending (US$ bn)", "% of GDP", "% of global spending"]
            df["Rank"] = range(1, len(df) + 1)
            df["Country"] = clean_country(df["Country"])
            df["Spending (US$ bn)"] = clean_numeric(df["Spending (US$ bn)"])
            df["% of GDP"] = clean_numeric(df["% of GDP"])
            df["% of global spending"] = clean_numeric(df["% of global spending"])
            df = df.dropna(subset=["Country", "Spending (US$ bn)"])
            path = os.path.join(DATA_DIR, "military_spending_sipri_2024.csv")
            df.to_csv(path, index=False)
            saved_files.append(("SIPRI 2024 — Top Spenders", path, len(df)))
            print(f"  ✓ Saved SIPRI 2024 top spenders ({len(df)} rows)")
            break
    
    # ── Table 2: IISS 2025 — Top 15 ──────────────────────────────────────
    for i, df in enumerate(tables):
        cols = [str(c).lower() for c in df.columns]
        col_str = " ".join(cols)
        if "spending" in col_str and "gdp" not in col_str and len(df) <= 20:
            df.columns = ["Rank", "Country", "Spending (US$ bn)"]
            df["Rank"] = range(1, len(df) + 1)
            df["Country"] = clean_country(df["Country"])
            df["Spending (US$ bn)"] = clean_numeric(df["Spending (US$ bn)"])
            df = df.dropna(subset=["Country", "Spending (US$ bn)"])
            path = os.path.join(DATA_DIR, "military_spending_iiss_2025.csv")
            df.to_csv(path, index=False)
            saved_files.append(("IISS 2025 — Top 15 Spenders", path, len(df)))
            print(f"  ✓ Saved IISS 2025 top spenders ({len(df)} rows)")
            break
    
    # If we couldn't find enough tables, use fallback
    if len(saved_files) < 2:
        print("\nCould not match all tables. Using hardcoded fallback for remaining.")
        return create_fallback_data()
    
    # ── Tables 3 & 4: GDP percentage tables ──────────────────────────────
    gdp_tables_found = 0
    for i, df in enumerate(tables):
        cols = [str(c).lower() for c in df.columns]
        col_str = " ".join(cols)
        if "gdp" in col_str and "spending" not in col_str and len(df.columns) <= 4:
            df_clean = df.copy()
            if len(df_clean.columns) == 3:
                df_clean.columns = ["Rank", "Country", "% of GDP"]
            else:
                continue
            df_clean["Rank"] = range(1, len(df_clean) + 1)
            df_clean["Country"] = clean_country(df_clean["Country"])
            df_clean["% of GDP"] = clean_numeric(df_clean["% of GDP"])
            df_clean = df_clean.dropna(subset=["Country", "% of GDP"])
            
            if gdp_tables_found == 0:
                path = os.path.join(DATA_DIR, "gdp_pct_sipri_2024.csv")
                label = "SIPRI 2024 — % of GDP"
            else:
                path = os.path.join(DATA_DIR, "gdp_pct_iiss_2020.csv")
                label = "IISS 2020 — % of GDP"
            
            df_clean.to_csv(path, index=False)
            saved_files.append((label, path, len(df_clean)))
            print(f"  ✓ Saved {label} ({len(df_clean)} rows)")
            gdp_tables_found += 1
            if gdp_tables_found >= 2:
                break
    
    print(f"\n{'='*50}")
    print(f"Total files saved: {len(saved_files)}")
    for name, path, rows in saved_files:
        print(f"  • {name}: {rows} rows → {os.path.basename(path)}")
    print(f"{'='*50}")
    
    return saved_files


def create_fallback_data():
    """
    Hardcoded fallback data in case Wikipedia scraping fails.
    Data sourced from: https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures
    Last updated: March 2026
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # ── SIPRI 2024 — Top 40 ──────────────────────────────────────────────
    sipri_data = {
        "Rank": list(range(1, 41)),
        "Country": [
            "United States", "China", "Russia", "Germany", "India",
            "United Kingdom", "Saudi Arabia", "Ukraine", "France", "Japan",
            "South Korea", "Israel", "Poland", "Italy", "Australia",
            "Canada", "Turkey", "Spain", "Netherlands", "Algeria",
            "Brazil", "Mexico", "Taiwan", "Colombia", "Singapore",
            "Sweden", "Indonesia", "Norway", "Pakistan", "Denmark",
            "Romania", "Belgium", "Greece", "Iran", "Kuwait",
            "Finland", "Switzerland", "Czech Republic", "Iraq", "Philippines"
        ],
        "Spending (US$ bn)": [
            997.0, 314.0, 149.0, 88.5, 86.1,
            81.8, 80.3, 64.7, 64.7, 55.3,
            47.6, 46.5, 38.0, 38.0, 33.8,
            29.3, 25.0, 24.6, 23.2, 21.8,
            20.9, 16.7, 16.5, 15.1, 15.1,
            12.0, 11.0, 10.4, 10.2, 10.0,
            8.7, 8.6, 8.0, 7.9, 7.8,
            7.0, 6.7, 6.5, 6.2, 6.1
        ],
        "% of GDP": [
            3.4, 1.7, 7.1, 1.9, 2.3,
            2.3, 7.4, 34.0, 2.1, 1.4,
            2.6, 8.8, 4.2, 1.6, 1.9,
            1.3, 1.9, 1.4, 1.9, 8.0,
            1.0, 0.9, 2.1, 3.4, 2.8,
            2.0, 0.8, 2.1, 2.7, 2.4,
            2.3, 1.3, 3.1, 2.0, 4.8,
            2.3, 0.7, 1.9, 2.4, 1.3
        ],
        "% of global spending": [
            35.5, 11.2, 5.5, 3.2, 3.1,
            3.0, 3.0, 2.4, 2.4, 2.0,
            1.8, 1.7, 1.4, 1.4, 1.2,
            1.1, 1.0, 0.9, 0.7, 0.7,
            0.7, 0.6, 0.5, 0.5, 0.4,
            0.4, 0.4, 0.4, 0.4, 0.3,
            0.3, 0.3, 0.3, 0.3, 0.3,
            0.3, 0.2, 0.2, 0.2, 0.2
        ]
    }
    pd.DataFrame(sipri_data).to_csv(
        os.path.join(DATA_DIR, "military_spending_sipri_2024.csv"), index=False
    )
    
    # ── IISS 2025 — Top 15 ───────────────────────────────────────────────
    iiss_data = {
        "Rank": list(range(1, 16)),
        "Country": [
            "United States", "China", "Russia", "Germany", "United Kingdom",
            "India", "Saudi Arabia", "France", "Japan", "Ukraine",
            "South Korea", "Italy", "Israel", "Australia", "Poland"
        ],
        "Spending (US$ bn)": [
            921.0, 251.3, 186.2, 107.3, 94.3,
            78.3, 72.5, 70.0, 58.9, 44.4,
            43.8, 40.1, 39.7, 37.3, 33.2
        ]
    }
    pd.DataFrame(iiss_data).to_csv(
        os.path.join(DATA_DIR, "military_spending_iiss_2025.csv"), index=False
    )
    
    # ── % of GDP — SIPRI 2024 ────────────────────────────────────────────
    gdp_sipri = {
        "Rank": list(range(1, 26)),
        "Country": [
            "Ukraine", "Israel", "Algeria", "Saudi Arabia", "Russia",
            "Myanmar", "Oman", "Armenia", "Azerbaijan", "Kuwait",
            "Jordan", "Burkina Faso", "Mali", "Poland", "Burundi",
            "Brunei", "Morocco", "United States", "Estonia", "Colombia",
            "Latvia", "Greece", "Lithuania", "Chad", "Kyrgyzstan"
        ],
        "% of GDP": [
            34.48, 8.78, 7.97, 7.30, 7.05,
            6.79, 5.59, 5.48, 4.99, 4.84,
            4.80, 4.68, 4.20, 4.15, 3.80,
            3.58, 3.52, 3.42, 3.37, 3.36,
            3.26, 3.13, 3.12, 2.98, 2.97
        ]
    }
    pd.DataFrame(gdp_sipri).to_csv(
        os.path.join(DATA_DIR, "gdp_pct_sipri_2024.csv"), index=False
    )
    
    # ── % of GDP — IISS 2020 ─────────────────────────────────────────────
    gdp_iiss = {
        "Rank": list(range(1, 16)),
        "Country": [
            "Oman", "Afghanistan", "Lebanon", "Kuwait", "Saudi Arabia",
            "Algeria", "Iraq", "UAE", "Azerbaijan", "Morocco",
            "Israel", "Jordan", "Armenia", "Mali", "Qatar"
        ],
        "% of GDP": [
            12.0, 10.6, 10.5, 7.1, 7.1,
            6.7, 5.8, 5.6, 5.4, 5.3,
            5.2, 4.9, 4.8, 4.5, 4.4
        ]
    }
    pd.DataFrame(gdp_iiss).to_csv(
        os.path.join(DATA_DIR, "gdp_pct_iiss_2020.csv"), index=False
    )
    
    print("  ✓ Created all 4 CSV files from hardcoded fallback data.")
    return [
        ("SIPRI 2024 — Top 40", os.path.join(DATA_DIR, "military_spending_sipri_2024.csv"), 40),
        ("IISS 2025 — Top 15", os.path.join(DATA_DIR, "military_spending_iiss_2025.csv"), 15),
        ("SIPRI 2024 — % GDP", os.path.join(DATA_DIR, "gdp_pct_sipri_2024.csv"), 25),
        ("IISS 2020 — % GDP", os.path.join(DATA_DIR, "gdp_pct_iiss_2020.csv"), 15),
    ]


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Military Expenditure Data Scraper")
    print("=" * 50)
    scrape_tables()
    print("\nDone! Data is ready in the data/ folder.")
