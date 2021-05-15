from .sql_utils import db_connect


async def get_user_info(user_id: str):
    async with db_connect() as conn:
        return await conn.fetchrow(f"select * from users where id={user_id}")


async def get_files_count(user_id: str):
    async with db_connect() as conn:
        return await conn.fetchrow(
            f"select count(*) from files where user_id={user_id}"
        )


async def get_files_size(user_id: str):
    async with db_connect() as conn:
        return await conn.fetchrow(
            f"select sum(size) from files where user_id={user_id}"
        )


async def get_files(user_id: str):
    async with db_connect() as conn:
        return await conn.fetch(f"select * from files where user_id={user_id}")


async def get_file_status(file_id: str):
    async with db_connect() as conn:
        return await conn.fetchrow(f"select status from files where id={file_id}")


async def get_user_id(tg_name: str):
    async with db_connect() as conn:
        return await conn.fetchrow(
            f"select id from users where telegram_name like '{tg_name}'"
        )
