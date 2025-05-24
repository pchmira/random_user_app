from .database import Base, engine
from .models import User

print("Создаю таблицы...")
Base.metadata.create_all(bind=engine)
print("Готово.")
