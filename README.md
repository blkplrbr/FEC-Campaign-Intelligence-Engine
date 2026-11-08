# FEC Campaign Intelligence & Lead Scoring Engine

## Project Overview
Developed an automated Python data pipeline for a political consulting firm to scrape, clean, and analyze Federal Election Commission (FEC) campaign finance data. The goal was to identify which campaigns were financially healthy enough to afford premium consulting services, and to categorize them into strategic marketing tiers based on their budget and cash burn rate.

## The Problem
The firm needed an efficient way to identify high-value leads without manually researching hundreds of campaigns. Pitching services to campaigns with high burn rates (overspending) resulted in wasted time and lost revenue. 

## Technical Stack
*   **Language:** Python
*   **Libraries:** Pandas, NumPy
*   **Data Source:** Federal Election Commission (FEC) Open API
*   **Input/Output:** Automated `.xlsx` generation for business development teams.

## Methodology & Code Architecture

### 1. Data Extraction & Loading
The pipeline reads raw campaign data (pulled from the FEC API) into a Pandas DataFrame, utilizing `try/except` blocks to handle file loading errors gracefully. 

### 2. Feature Engineering (The Lead Score)
To determine financial health, the script calculates the **Cash Retention Percentage** using a custom NumPy formula that guards against division-by-zero errors:
*   `Cash_Retention_Pct = (Cash_On_Hand / Total_Raised) * 100`

### 3. Budget Tiering
A custom Python function (`assign_budget_tier`) evaluates the `Total_Raised` column and categorizes campaigns into three tiers:
*   **Tier 1:** Mega ($500k+)
*   **Tier 2:** Mid-Tier ($100k - $500k)
*   **Tier 3:** Grassroots (<$100k)

### 4. Strategic Targeting Quadrants (Dynamic Segmentation)
To ensure the marketing team knew exactly *how* to approach the leads, the pipeline calculates the **median** cash retention and total raised for the entire dataset. Using these dynamic medians, it segments the campaigns into strategic quadrants:
*   **Q1: Mega Whale (High Raised, High Cash):** Priority 2: Executive White-Glove Consult.
*   **Q2: High Burner (High Raised, Low Cash):** Priority 3: Nurture / Watch Burn Rate.
*   **Q3: Grassroots:** Low priority for premium services.

## Business Impact
*   Transformed raw, unstructured FEC data into a highly targeted marketing intelligence spreadsheet (`marketing_campaign_intelligence.xlsx`).
*   Provided the business development team with a prioritized list of viable clients and specific action plans for how to pitch them.
*   Automated a research process that would have taken dozens of manual hours.
