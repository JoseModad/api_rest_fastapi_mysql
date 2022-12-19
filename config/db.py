# Sqlalchemy

from sqlalchemy import create_engine, MetaData


# Connection to the database

engine = create_engine("mysql+pymysql://turko:123@localhost:3306/fastapi_users")

meta_data = MetaData()