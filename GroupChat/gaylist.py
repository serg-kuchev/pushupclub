import threading
from datetime import datetime, timedelta
from dispatcher import bot

#код ниже будет изменён под scheduler поскольку нам нужно вызывать функцию каждый день в одно и тоже время, а не через один и тот же промежуток

# now = datetime.now()
# tomorrow = datetime(now.year, now.month, now.day + 1, 12, 0)
# print(tomorrow)
# print((tomorrow - now).seconds)
#
# def setInterval(interval):
#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             stopped = threading.Event()
#             def loop(): # executed in another thread
#                 while not stopped.wait(interval): # until stopped
#                     function(*args, **kwargs)
#             t = threading.Thread(target=loop)
#             t.daemon = True # stop if the program exits
#             t.start()
#             return stopped
#         return wrapper
#     return decorator
#
#
# @setInterval((tomorrow - now).seconds)
# def printer():
#     wasted = []  # <-- сюда надо из гугл щита вытащить всех челиков, по желанию можем и их вытащить
#     wasted_joined = '\n'.join(wasted)
#     if wasted:
#         await bot.send_message(f"Список провалившихся участников {wasted_joined}")
#
#
# stop = printer()