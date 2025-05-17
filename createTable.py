from models import Base 
from config.database import Engine

def create_all_tables():
    Base.metadata.create_all(bind=Engine)
    print("All tables created successfully")

if __name__ == "__main__":
    create_all_tables()