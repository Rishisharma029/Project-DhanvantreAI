import pandas as pd
import re
import os
import json
from typing import Dict, List, Any

class UniHackProductProcessor:
    """
    Processor for UniHack Industrial Product Intelligence.
    Transforms raw part descriptions into enriched, structured data.
    """
    
    EXPECTED_HEADERS = [
        "MFR URL", "Ref URL 1", "Ref URL 2", "Ref URL 3", "Ref URL 4", "Ref URL 5",
        "PART_NUMBER", "Dept", "Class", "Fine", "SKU - MY_PART_NUMBER", "Mfg_Part_Num",
        "Part_Desc", "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf",
        "MANUFACTURER_NAME", "BRAND_NAME", "TRADE_NAME", "MANUFACTURER_PART_NUMBER",
        "ALTERNATE_PART_NUMBER", "Classpath", "MOBILE_DESC", "INVOICE_DESC",
        "SHORT_DESC", "LONG_DESC1", "RETAIL_DESC", "MARKETING_DESCRIPTION"
    ] + [f"ITEM_FEATURES_{i}" for i in range(1, 21)] + [
        "With", "Standard/Approvals", "Prop 65", "Application", "Includes", "Product Name"
    ] + [val for i in range(1, 51) for val in [f"ATTRIBUTE_LABEL {i}", f"ATTRIBUTE_VALUE {i}", f"ATTRIBUTE_UOM {i}"]]

    def __init__(self):
        self.brand_mapping = {
            "-- Unbranded --": "",
            "-- No Unilog Brand --": "",
            "-- No DIB Brand --": ""
        }

    def clean_value(self, val: Any) -> str:
        if pd.isna(val) or str(val).strip() in self.brand_mapping:
            return ""
        return str(val).strip()

    def generate_invoice_desc(self, part_desc: str) -> str:
        """Invoice Desc (<=40 char, CAPS)"""
        clean = re.sub(r'[^A-Z0-9\s\-\/\.]', '', part_desc.upper())
        return clean[:40].strip()

    def generate_mobile_desc(self, manufacturer: str, brand: str, part_desc: str) -> str:
        """Mobile Desc (60–80 char)"""
        mfr = manufacturer if manufacturer else brand
        desc = f"{mfr} {part_desc}"
        if len(desc) > 80:
            return desc[:77] + "..."
        return desc

    def extract_attributes(self, part_desc: str) -> Dict[str, str]:
        """Simple rule-based attribute extraction for industrial parts."""
        attributes = {}
        # Example: 1/2"x18" -> Size: 1/2" x 18"
        size_match = re.search(r'(\d+[\/\.]?\d*["\']?)\s*x\s*(\d+[\/\.]?\d*["\']?)', part_desc)
        if size_match:
            attributes["Size"] = f"{size_match.group(1)} x {size_match.group(2)}"
        
        # Example: P150 -> Grit: 150
        grit_match = re.search(r'\bP(\d+)\b', part_desc)
        if grit_match:
            attributes["Grit"] = grit_match.group(1)
            
        return attributes

    def process_row(self, row: pd.Series) -> Dict[str, Any]:
        part_num = self.clean_value(row.get('Mfg_Part_Num', ''))
        part_desc = self.clean_value(row.get('Part_Desc', ''))
        mfr = self.clean_value(row.get('Part_Manuf', ''))
        brand = self.clean_value(row.get('E1_Brand', ''))
        
        enriched = {h: "" for h in self.EXPECTED_HEADERS}
        
        enriched["PART_NUMBER"] = part_num
        enriched["Mfg_Part_Num"] = part_num
        enriched["Part_Desc"] = part_desc
        enriched["Part_Manuf"] = mfr
        enriched["MANUFACTURER_NAME"] = mfr
        enriched["BRAND_NAME"] = brand if brand else mfr
        enriched["MANUFACTURER_PART_NUMBER"] = part_num
        
        enriched["INVOICE_DESC"] = self.generate_invoice_desc(part_desc)
        enriched["MOBILE_DESC"] = self.generate_mobile_desc(mfr, brand, part_desc)
        enriched["SHORT_DESC"] = f"{enriched['BRAND_NAME']} {part_desc}"
        enriched["LONG_DESC1"] = f"{enriched['BRAND_NAME']} {part_desc} - High quality industrial component."
        
        attrs = self.extract_attributes(part_desc)
        for i, (label, value) in enumerate(attrs.items(), 1):
            if i > 50: break
            enriched[f"ATTRIBUTE_LABEL {i}"] = label
            enriched[f"ATTRIBUTE_VALUE {i}"] = value
            
        return enriched

    def process_csv(self, input_path: str, output_path: str):
        df = pd.read_csv(input_path)
        results = [self.process_row(row) for _, row in df.iterrows()]
        output_df = pd.DataFrame(results)
        
        # Ensure all expected headers are present and in order
        for col in self.EXPECTED_HEADERS:
            if col not in output_df.columns:
                output_df[col] = ""
        
        output_df = output_df[self.EXPECTED_HEADERS]
        
        if output_path.endswith('.xlsx'):
            output_df.to_excel(output_path, index=False)
        else:
            output_df.to_csv(output_path, index=False)
        
        return len(output_df)

if __name__ == "__main__":
    processor = UniHackProductProcessor()
    input_file = "/home/ubuntu/upload/Unihack_SampleDataset-Input.csv"
    output_file = "/home/ubuntu/repo/unihack_delivery_prototype.csv"
    
    if os.path.exists(input_file):
        count = processor.process_csv(input_file, output_file)
        print(f"Processed {count} rows. Delivery format generated at {output_file}")
    else:
        print("Input file not found.")
