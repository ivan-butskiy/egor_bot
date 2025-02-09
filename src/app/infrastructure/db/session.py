from sqlalchemy.ext.asyncio import async_sessionmaker

from .engine import engine


SESSION_FACTORY = async_sessionmaker(engine)
