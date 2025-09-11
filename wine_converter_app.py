import streamlit as st
import pandas as pd
import json
import re
from io import StringIO

def clean_text(text, preserve_line_breaks=False):
    """Clean and normalize text fields"""
    if not text or str(text).strip() == '' or str(text).lower() == 'nan':
        return ""
    
    text = str(text)
    
    # Remove quotes if they wrap the entire string
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    
    if preserve_line_breaks:
        # For harmonization field, preserve line breaks as \n
        # First normalize different line break types to \n
        text = re.sub(r'\r\n|\r', '\n', text)
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        # Remove empty lines
        lines = [line for line in lines if line]
        # Join with \n
        return '\n'.join(lines)
    else:
        # Remove extra whitespace and newlines
        cleaned = re.sub(r'\s+', ' ', text.strip())
        return cleaned

def parse_number(text, is_float=False):
    """Parse text to number, return None if invalid"""
    if not text or str(text).strip() == '' or str(text).lower() == 'nan':
        return None
    
    # Clean the text
    cleaned = clean_text(str(text))
    
    try:
        # For harvest years, just extract the number
        if not is_float:
            # Extract year (4 digits)
            year_match = re.search(r'\b(\d{4})\b', cleaned)
            if year_match:
                return int(year_match.group(1))
            # If no year found, try to parse as regular integer
            return int(float(cleaned))
        else:
            # For alcohol level, extract the percentage number and divide by 100
            percent_match = re.search(r'([\d.]+)%?', cleaned)
            if percent_match:
                return float(percent_match.group(1)) / 100.0
            return float(cleaned) / 100.0
    except (ValueError, TypeError):
        return None

def convert_csv_to_json(df):
    """Convert DataFrame to wine JSON format"""
    wines = []
    
    # Create header mapping
    header_mapping = {}
    for i, col in enumerate(df.columns):
        col_clean = clean_text(col).lower()
        if col_clean == 'id':
            header_mapping['id'] = i
        elif col_clean == 'referralid':
            header_mapping['referralId'] = i
        elif col_clean == 'name':
            header_mapping['name'] = i
        elif col_clean == 'producer':
            header_mapping['producer'] = i
        elif col_clean == 'origincountry':
            header_mapping['originCountry'] = i
        elif col_clean == 'region':
            header_mapping['region'] = i
        elif col_clean == 'grapetype':
            header_mapping['grapeType'] = i
        elif col_clean == 'winetype':
            header_mapping['wineType'] = i
        elif col_clean == 'harvest':
            header_mapping['harvest'] = i
        elif col_clean == 'alcohollevel':
            header_mapping['alcoholLevel'] = i
        elif col_clean == 'agingprocess':
            header_mapping['agingProcess'] = i
        elif col_clean == 'harmonization':
            header_mapping['harmonization'] = i
        elif col_clean == 'tastedescription':
            header_mapping['tasteDescription'] = i
    
    # Process each row
    for index, row in df.iterrows():
        # Create wine object with proper data types
        wine = {
            "id": parse_number(row.iloc[header_mapping.get('id', 0)] if header_mapping.get('id', 0) < len(row) else ""),
            "referralId": parse_number(row.iloc[header_mapping.get('referralId', 1)] if header_mapping.get('referralId', 1) < len(row) else ""),
            "name": clean_text(row.iloc[header_mapping.get('name', 2)] if header_mapping.get('name', 2) < len(row) else ""),
            "producer": clean_text(row.iloc[header_mapping.get('producer', 3)] if header_mapping.get('producer', 3) < len(row) else ""),
            "originCountry": clean_text(row.iloc[header_mapping.get('originCountry', 4)] if header_mapping.get('originCountry', 4) < len(row) else ""),
            "region": clean_text(row.iloc[header_mapping.get('region', 5)] if header_mapping.get('region', 5) < len(row) else ""),
            "grapeType": clean_text(row.iloc[header_mapping.get('grapeType', 6)] if header_mapping.get('grapeType', 6) < len(row) else ""),
            "wineType": clean_text(row.iloc[header_mapping.get('wineType', 7)] if header_mapping.get('wineType', 7) < len(row) else ""),
            "harvest": parse_number(row.iloc[header_mapping.get('harvest', 8)] if header_mapping.get('harvest', 8) < len(row) else ""),
            "alcoholLevel": parse_number(row.iloc[header_mapping.get('alcoholLevel', 9)] if header_mapping.get('alcoholLevel', 9) < len(row) else "", is_float=True),
            "price": None,
            "importedBy": None,
            "agingProcess": clean_text(row.iloc[header_mapping.get('agingProcess', 10)] if header_mapping.get('agingProcess', 10) < len(row) else ""),
            "harmonization": clean_text(row.iloc[header_mapping.get('harmonization', 11)] if header_mapping.get('harmonization', 11) < len(row) else "", preserve_line_breaks=True),
            "tasteDescription": clean_text(row.iloc[header_mapping.get('tasteDescription', 12)] if header_mapping.get('tasteDescription', 12) < len(row) else ""),
        }
        
        # Only add wines with at least a name or ID
        if wine['name'] or wine['id']:
            wines.append(wine)
    
    return wines

def create_full_json_structure(wines_data):
    """Create the complete JSON structure with wines, steaks, and sommelier suggestions"""
    
    # Static steak data
    steaks_data = [
        {
            "id": 2009,
            "name": "Short Rib Angus",
            "producer": "Puro Taglio",
            "cutType": "Short Rib",
            "originCountry": "Brasil",
            "breed": "Angus",
            "tasteDescription": "",
            "price": 0,
            "referralId": 2009
        },
        {
            "id": 2026,
            "name": "Prime Rib Angus",
            "producer": "Puro Taglio",
            "cutType": "Prime Rib",
            "originCountry": "Brasil",
            "breed": "Angus",
            "tasteDescription": "",
            "price": 0,
            "referralId": 2026
        },
        {
            "id": 2013,
            "name": "T-Bone Steak Angus",
            "producer": "Puro Taglio",
            "cutType": "T-Bone Steak",
            "originCountry": "Brasil",
            "breed": "Angus",
            "tasteDescription": "",
            "price": 0,
            "referralId": 2013
        },
        {
            "id": 2004,
            "name": "Flat Iron Angus",
            "producer": "Puro Taglio",
            "cutType": "Flat Iron",
            "originCountry": "Brasil",
            "breed": "Angus",
            "tasteDescription": "",
            "price": 0,
            "referralId": 2004
        }
    ]
    
    # Static sommelier suggestions data
    sommelier_suggestions = [
        {
            "name": "Kit Executivo - 10% OFF",
            "wineId": 3760245210066,
            "steakId": 2009,
            "id": "executivo"
        },
        {
            "name": "Kit Elegante - 15% OFF",
            "wineId": 7798145140141,
            "steakId": 2026,
            "id": "elegante"
        },
        {
            "name": "Kit Premium - 15% OFF",
            "wineId": 8052080990001,
            "steakId": 2013,
            "id": "premium"
        }
    ]
    
    # Create the complete structure
    complete_data = {
        "wine": wines_data,
        "steak": steaks_data,
        "sommelierSuggestions": sommelier_suggestions
    }
    
    return complete_data

# Streamlit App
def main():
    st.set_page_config(
        page_title="Wine CSV to JSON Converter",
        page_icon="🍷",
        layout="wide"
    )
    
    st.title("🍷 Wine CSV to JSON Converter")
    st.markdown("Upload your wine CSV file and convert it to JSON format with proper data types.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file", 
        type="csv",
        help="Upload the wine technical sheet CSV file"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ File uploaded successfully! Found {len(df)} rows.")
            
            # Show preview
            with st.expander("📋 Preview CSV Data", expanded=False):
                st.dataframe(df.head(10))
            
            # Convert button
            if st.button("🔄 Convert to JSON", type="primary"):
                with st.spinner("Converting CSV to JSON..."):
                    wines_data = convert_csv_to_json(df)
                    complete_data = create_full_json_structure(wines_data)
                
                st.success(f"✅ Conversion complete! {len(wines_data)} wines converted.")
                st.info(f"📦 Added {len(complete_data['steak'])} steaks and {len(complete_data['sommelierSuggestions'])} sommelier suggestions.")
                
                # Show preview of JSON structure
                with st.expander("👀 Preview JSON Structure", expanded=True):
                    # Show structure overview
                    st.markdown("### JSON Structure:")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🍷 Wines", len(complete_data['wine']))
                    with col2:
                        st.metric("🥩 Steaks", len(complete_data['steak']))
                    with col3:
                        st.metric("👨‍🍳 Suggestions", len(complete_data['sommelierSuggestions']))
                    
                    # Show sample of each section
                    st.markdown("### Sample Data:")
                    
                    # Wine sample
                    st.markdown("**Wine (first 2 items):**")
                    wine_sample = complete_data['wine'][:2] if len(complete_data['wine']) >= 2 else complete_data['wine']
                    st.json({"wine": wine_sample})
                    
                    # Steak sample
                    st.markdown("**Steak (all items):**")
                    st.json({"steak": complete_data['steak']})
                    
                    # Sommelier suggestions sample
                    st.markdown("**Sommelier Suggestions (all items):**")
                    st.json({"sommelierSuggestions": complete_data['sommelierSuggestions']})
                
                # Download button
                json_string = json.dumps(complete_data, indent=2, ensure_ascii=False)
                
                st.download_button(
                    label="💾 Download JSON File",
                    data=json_string,
                    file_name="appData.json",
                    mime="application/json"
                )
                
                # Show detailed statistics
                st.markdown("### 📊 Data Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🍷 Total Wines", len(wines_data))
                with col2:
                    countries = set(wine['originCountry'] for wine in wines_data if wine['originCountry'])
                    st.metric("🌍 Countries", len(countries))
                with col3:
                    producers = set(wine['producer'] for wine in wines_data if wine['producer'])
                    st.metric("🏭 Producers", len(producers))
                with col4:
                    st.metric("📊 Total Items", len(complete_data['wine']) + len(complete_data['steak']) + len(complete_data['sommelierSuggestions']))
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("Please make sure your CSV file has the correct format with headers: id, referralId, name, producer, originCountry, region, grapeType, wineType, harvest, alcoholLevel, agingProcess, harmonization, tasteDescription")
    
    # Instructions
    with st.expander("📖 Instructions", expanded=False):
        st.markdown("""
        ### How to use this converter:
        
        1. **Upload your CSV file** using the file uploader above
        2. **Preview the data** to make sure it looks correct
        3. **Click "Convert to JSON"** to process the file
        4. **Download the JSON file** using the download button
        
        ### Expected CSV Format:
        Your CSV should have these columns:
        - `id` - Wine barcode/ID (will be converted to number)
        - `referralId` - Reference ID (will be converted to number)
        - `name` - Wine name (string)
        - `producer` - Producer name (string)
        - `originCountry` - Country of origin (string)
        - `region` - Wine region (string)
        - `grapeType` - Grape varieties (string)
        - `wineType` - Type of wine (string)
        - `harvest` - Harvest year (will be converted to number)
        - `alcoholLevel` - Alcohol percentage (will be converted to decimal)
        - `agingProcess` - Aging process description (string)
        - `harmonization` - Food pairing suggestions (string, line breaks preserved)
        - `tasteDescription` - Wine description (string)
        
        ### Output Format:
        The JSON will have a complete structure with three main sections:
        
        **Wine Data:** (from your CSV)
        - Numbers for `id`, `referralId`, `harvest`, and `alcoholLevel`
        - Strings for text fields
        - `null` for `price` and `importedBy`
        - Line breaks preserved in `harmonization` field
        
        **Steak Data:** (static data)
        - 4 predefined steak cuts from Puro Taglio
        - Includes: Short Rib, Prime Rib, T-Bone Steak, Flat Iron
        
        **Sommelier Suggestions:** (static data)
        - 3 predefined wine & steak pairing kits
        - Includes: Kit Executivo, Kit Elegante, Kit Premium
        
        **Final JSON Structure:**
        ```json
        {
          "wine": [your wine data],
          "steak": [steak data],
          "sommelierSuggestions": [pairing suggestions]
        }
        ```
        """)

if __name__ == "__main__":
    main()
