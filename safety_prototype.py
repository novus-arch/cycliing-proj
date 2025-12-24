import pandas as pd
from urllib.parse import quote

# 1. Setup the NYC Open Data Source
BASE_URL = "https://data.cityofnewyork.us/resource/h9gi-nx95.csv"
# The query filters for cyclist injuries/deaths to find "Black Spots"
RAW_QUERY = "?$where=number_of_cyclist_injured > 0 OR number_of_cyclist_killed > 0&$limit=5000"
# We encode the query to fix the 'InvalidURL' error (handling spaces and symbols)
ENCODED_URL = BASE_URL + quote(RAW_QUERY, safe='?&$=')

def run_plan_a_prototype():
    try:
        print("Connecting to NYC Safety Database...")
        # Read the data directly from the encoded URL
        df = pd.read_csv(ENCODED_URL)
        
        # 2. Define "Human Error" categories based on our project goals
        human_error_factors = [
            'Driver Inattention/Distraction',
            'Failure to Yield Right-of-Way',
            'Looked But Did Not See',
            'Unsafe Lane Changing',
            'Passing or Lane Usage Improper'
        ]
        
        # 3. Filter for incidents caused by human error
        # This aligns with the "Safety First" and "Respect the Road" pillars
        df_filtered = df[df['contributing_factor_vehicle_1'].isin(human_error_factors)].copy()
        
        # 4. Clean GPS data
        df_filtered = df_filtered.dropna(subset=['latitude', 'longitude'])
        
        # 5. Export the specific coordinates for our awareness service
        output_file = "proactive_awareness_zones.csv"
        df_filtered.to_csv(output_file, index=False)
        
        print(f"--- SUCCESS ---")
        print(f"Total incidents analyzed: {len(df)}")
        print(f"Human error zones identified: {len(df_filtered)}")
        print(f"Data saved to: {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_plan_a_prototype()