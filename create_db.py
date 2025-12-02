from database import Base, engine
import models

def create_database():
    Base.metadata.create_all(bind=engine)
    print("Database created!")

if __name__ == "__main__":
    create_database()