from contextlib import asynccontextmanager

import asyncpg

from tg.core.settings import settings


@asynccontextmanager
async def db_connect():
    conn = await asyncpg.connect(settings.psql_url)
    try:
        yield conn
    finally:
        await conn.close()


async def get_user_info(user_id: int):
    async with db_connect() as conn:
        return await conn.fetchrow("select * from users where id=$1", user_id)


async def get_files_count(user_id: int):
    async with db_connect() as conn:
        return await conn.fetchrow(
            "select count(*) from files where user_id=$1", user_id
        )


async def get_files_size(user_id: int):
    async with db_connect() as conn:
        return await conn.fetchrow(
            "select sum(size) from files where user_id=$1", user_id
        )


async def get_files(user_id: int):
    async with db_connect() as conn:
        return await conn.fetch("select * from files where user_id=$1", user_id)


async def get_file_status(file_id: str):
    async with db_connect() as conn:
        return await conn.fetchrow("select status from files where id=$1", file_id)


async def get_user_id(tg_name: str):
    async with db_connect() as conn:
        return await conn.fetchrow(
            "select id from users where telegram_name=$1", tg_name
        )
