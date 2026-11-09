import pandas as pd
import requests

def fetch_raw_dem_campaigns(limit=500):
    print(f"🌊 Fetching Top {limit} Democratic Campaign Finance Data...")
    
    candidates = []
    per_page = 100  # OpenFEC max limit per request
    pages_needed = limit // per_page
    
    for page in range(1, pages_needed + 1):
        print(f"   Pulling page {page} of {pages_needed}...")
        url = f"https://api.open.fec.gov/v1/candidates/totals/?party=DEM&cycle=2026&sort=-receipts&per_page={per_page}&page={page}&api_key=DEMO_KEY"
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"❌ Request failed on page {page} with status code: {response.status_code}")
                break
                
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                break
                
            for cand in results:
                # Clean conversion to numbers, default to 0.0 if missing
                try:
                    receipts = float(cand.get('receipts') or 0)
                except (ValueError, TypeError):
                    receipts = 0.0

                try:
                    cash_on_hand = float(cand.get('cash_on_hand_end_period') or 0)
                except (ValueError, TypeError):
                    cash_on_hand = 0.0

                candidates.append({
                    'Candidate_ID': cand.get('candidate_id'),
                    'Candidate_Name': cand.get('name'),
                    'Party': cand.get('party'),
                    'Office': cand.get('office_full', 'Unknown'),
                    'State': cand.get('state'),
                    'District': cand.get('district', 'N/A'),
                    'Total_Raised': receipts,
                    'Cash_On_Hand': cash_on_hand
                })
                
        except Exception as e:
            print(f"❌ Error on page {page}: {e}")
            break
            
    if not candidates:
        print("❌ No raw data collected!")
        return None

    df = pd.DataFrame(candidates)
    df = df.sort_values(by='Total_Raised', ascending=False)
    
    output_file = "raw_500_democratic_campaigns.xlsx"
    df.to_excel(output_file, index=False)
    
    print(f"\n Success! Saved raw data for {len(df)} campaigns into '{output_file}'.")
    return df

if __name__ == "__main__":
    fetch_raw_dem_campaigns(500)