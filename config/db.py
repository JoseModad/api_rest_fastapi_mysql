# Sqlalchemy

from sqlalchemy import create_engine, MetaData


engine = create_engine("mysql+pymysql://turko:123@localhost:3306/fastapi_users")

conn = engine.connect()

meta_data = MetaData()