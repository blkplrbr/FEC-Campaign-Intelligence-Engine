import pandas as pd
import numpy as np

def spin_raw_data_into_gold():
    print("✨ Opening raw dataset and initializing Gold Spinner Pipeline...")
    
    raw_file = "raw_500_democratic_campaigns.xlsx"
    output_file = "marketing_campaign_intelligence.xlsx"
    
    try:
        # Load raw dataset
        df = pd.read_excel(raw_file)
        print(f"📥 Loaded {len(df)} records from '{raw_file}'")
    except Exception as e:
        print(f"❌ Error loading file '{raw_file}': {e}")
        return

    # 1. CASH RETENTION RATIO (%)
    df['Cash_Retention_Pct'] = np.where(
        df['Total_Raised'] > 0,
        ((df['Cash_On_Hand'] / df['Total_Raised']) * 100).round(2),
        0.0
    )

    # 2. BUDGET TIERING
    def assign_budget_tier(raised):
        if raised >= 500000:
            return "Tier 1: Mega ($500k+)"
        elif raised >= 100000:
            return "Tier 2: Mid-Tier ($100k-$500k)"
        else:
            return "Tier 3: Grassroots (<$100k)"

    df['Budget_Tier'] = df['Total_Raised'].apply(assign_budget_tier)

    # 3. STRATEGIC TARGETING QUADRANTS
    # Median calculations for dynamic quadrant threshold splitting
    median_raised = df['Total_Raised'].median()
    median_cash = df['Cash_On_Hand'].median()

    def assign_quadrant(row):
        r = row['Total_Raised']
        c = row['Cash_On_Hand']
        
        if r >= median_raised and c >= median_cash:
            return "Q1: Mega Whale (High Raised, High Cash)"
        elif r >= median_raised and c < median_cash:
            return "Q2: High Burner (High Raised, Low Cash)"
        elif r < median_raised and c >= median_cash:
            return "Q3: Sleeper Hit (Modest Raised, HIGH Cash Ratio) - PRIME TARGET"
        else:
            return "Q4: Grassroots / Low Runway"

    df['Target_Quadrant'] = df.apply(assign_quadrant, axis=1)

    # 4. MARKETING OUTREACH RECOMMENDATION
    def assign_action(row):
        q = row['Target_Quadrant']
        c = row['Cash_On_Hand']
        
        if "Q3: Sleeper Hit" in q:
            return "🎯 Priority 1: Direct Pitch (Eager & High Liquid Capital)"
        elif "Q1: Mega Whale" in q:
            return "💼 Priority 2: Executive White-Glove Consult"
        elif "Q2: High Burner" in q:
            return "⚠️ Priority 3: Nurture / Watch Burn Rate"
        else:
            return "🤖 Priority 4: Low Touch / Automated Email"

    df['Marketing_Action_Plan'] = df.apply(assign_action, axis=1)

    print("📊 Generating Executive Summaries & Aggregations...")

    # SUMMARY TAB 1: Quadrant Breakdown
    quadrant_summary = df.groupby('Target_Quadrant').agg(
        Campaign_Count=('Candidate_ID', 'count'),
        Total_Market_Raised=('Total_Raised', 'sum'),
        Total_Cash_On_Hand=('Cash_On_Hand', 'sum'),
        Avg_Cash_Retention_Pct=('Cash_Retention_Pct', 'mean')
    ).reset_index()

    # SUMMARY TAB 2: State Hotspots
    state_summary = df.groupby(['State', 'Office']).agg(
        Campaign_Count=('Candidate_ID', 'count'),
        Total_Raised=('Total_Raised', 'sum'),
        Total_Cash=('Cash_On_Hand', 'sum')
    ).reset_index().sort_values(by='Total_Cash', ascending=False)

    # SUMMARY TAB 3: Total Addressable Market (TAM)
    total_raised_all = df['Total_Raised'].sum()
    total_cash_all = df['Cash_On_Hand'].sum()
    tam_data = pd.DataFrame([{
        'Total_Campaigns_Analyzed': len(df),
        'Total_Market_Raised_USD': total_raised_all,
        'Total_Liquid_Cash_USD': total_cash_all,
        'Median_Raised_USD': median_raised,
        'Median_Cash_On_Hand_USD': median_cash
    }])

    # 5. EXPORT MULTI-TAB EXCEL WORKBOOK
    print(f"💾 Saving intelligence workbook to '{output_file}'...")
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Leads_Scored_Full', index=False)
        quadrant_summary.to_excel(writer, sheet_name='Strategic_Quadrants', index=False)
        state_summary.to_excel(writer, sheet_name='State_Hotspots', index=False)
        tam_data.to_excel(writer, sheet_name='Market_TAM_Overview', index=False)

    print(f"\n🚀 BOOM! Process completed! Integrated intelligence workbook exported to '{output_file}'.")

if __name__ == "__main__":
    spin_raw_data_into_gold()