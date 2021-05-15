from contextlib import asynccontextmanager
import asyncpg

import sys

sys.path.append("..")

from settings import settings


@asynccontextmanager
async def db_connect():
    conn = await asyncpg.connect(settings.psql_url)
    try:
        yield conn
    finally:
        await conn.close()
