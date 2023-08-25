from dispatcher import bot


async def print_wasted():
    wasted = []
    wasted_joined = '\n'.join(wasted)
    if wasted:
         await bot.send_message(503889403,f"Список провалившихся участников {wasted_joined}")
    await bot.send_message(503889403, 'timed')
