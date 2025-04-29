from app.database import engine
from app.db_models import Base

Base.metadata.create_all(bind=engine)
print("✅ Tables created in MySQL")

