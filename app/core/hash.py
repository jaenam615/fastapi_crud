import asyncio

from passlib.context import CryptContext

pwd = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10,
)


async def hash_password(password: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pwd.hash, password)


async def verify_password(password, hashed):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pwd.verify, password, hashed)
