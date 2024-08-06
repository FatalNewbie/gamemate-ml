from data.database import engine, Base
from user.user_model import User

Base.metadata.create_all(bind=engine)
