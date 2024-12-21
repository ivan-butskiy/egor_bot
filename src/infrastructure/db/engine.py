import os

from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(os.getenv('SQLALCHEMY_URL'))
