from sqlalchemy import create_engine
from config import DATABASE_URL

# DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})


engine = create_engine(DATABASE_URL)