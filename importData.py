import pandas as pd
from config.database import Engine, SessionLocal
from models import Case
import numpy as np

def import_csv_to_database():
    db = SessionLocal()
    
    try:
        print("Reading CSV file...")
        df = pd.read_csv('globalterrorismdb_0522dist.csv')
        
        # Convert NaN values to None for SQL compatibility
        df = df.replace({np.nan: None})
        print(f"Found {len(df)} records. Starting import...")
        
        batch_size = 10000
        total_records = len(df)
        
        for i in range(0, total_records, batch_size):
            batch_df = df.iloc[i:min(i+batch_size, total_records)]
            
            cases = []
            for _, row in batch_df.iterrows():
                case_dict = {}
                
                for column in row.index:
                    column_lower = column.lower()
                    if hasattr(Case, column_lower):
                        case_dict[column_lower] = row[column]
                
                case = Case(**case_dict)
                cases.append(case)
            
            db.add_all(cases)
            db.commit()
            
            print(f"Imported {min(i+batch_size, total_records)} of {total_records} records")
        
        print("Import completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error during import: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_csv_to_database()
