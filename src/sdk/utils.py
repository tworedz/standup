import asyncio


async def wait_for(seconds: int = 10) -> None:
    """Подождать seconds секунд"""

    await asyncio.sleep(seconds)
