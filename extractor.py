import zipfile
import os
import shutil

DOWNLOADS_DIR = r'C:\Users\Rishi Sharma\Downloads'
RAW_DATA_DIR = os.path.join(os.getcwd(), 'data', 'raw')

ZIP_MAPPING = {
    'archive (1).zip': ['A_Z_medicines_dataset_of_India.csv'],
    'archive (2).zip': ['enhanced_fever_medicine_recommendation.csv'],
    'archive (3).zip': ['medicine_dataset.csv'],
    'archive (4).zip': [
        'Symptom-severity.csv', 'Training.csv', 'description.csv',
        'diets.csv', 'medications.csv', 'precautions_df.csv',
        'symtoms_df.csv', 'workout_df.csv'
    ],
    'archive (5).zip': ['db_drug_interactions.csv'],
    'archive (6).zip': ['Symptom2Disease.csv'],
    'archive (7).zip': ['drugs_side_effects_drugs_com.csv']
}

def extract_all():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    print(f"Extracting zip files to: {RAW_DATA_DIR}")
    
    extracted_files = []
    for zip_name, target_csvs in ZIP_MAPPING.items():
        zip_path = os.path.join(DOWNLOADS_DIR, zip_name)
        if not os.path.exists(zip_path):
            print(f"Warning: Zip file {zip_name} not found in Downloads.")
            continue
            
        print(f"Extracting from {zip_name}...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for csv_name in target_csvs:
                if csv_name in zf.namelist():
                    zf.extract(csv_name, RAW_DATA_DIR)
                    extracted_path = os.path.join(RAW_DATA_DIR, csv_name)
                    extracted_files.append(extracted_path)
                    print(f"  -> Extracted: {csv_name}")
                else:
                    print(f"  -> Warning: {csv_name} not found in {zip_name}")
                    
    print(f"Extraction completed. Total files extracted: {len(extracted_files)}")
    return extracted_files

if __name__ == '__main__':
    extract_all()
