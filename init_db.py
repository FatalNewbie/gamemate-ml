from database import engine, Base
from user.user_model import User, Genre, PlayTime

Base.metadata.create_all(bind=engine)
