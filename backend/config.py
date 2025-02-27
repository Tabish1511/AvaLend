import os

SECRET_KEY = os.getenv("JWT_SECRET", "tabish_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/AvaDB")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://khaqantabish:vFVkMo27hQwt@ep-snowy-sun-13421324-pooler.us-east-2.aws.neon.tech/AvaDB?sslmode=require")















































# import os

# MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_db")

# JWT_SECRET = os.getenv("JWT_SECRET", "myjwtsecret")
# JWT_ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
