from sqlalchemy.ext.asyncio import async_sessionmaker

from .engine import engine


session_factory = async_sessionmaker(engine)
