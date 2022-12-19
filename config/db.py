# Sqlalchemy

from sqlalchemy import create_engine, MetaData


# Connection to the database

## Replacing turko with your database username.
## Replacing 123 with your database password.
## The server runs by default on port 3306. Check and replace the port if necessary.
## Change the name of your database,  in my case it is called fastapi_users

engine = create_engine("mysql+pymysql://turko:123@localhost:3306/fastapi_users")

meta_data = MetaData()