from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from gamelogic import gen_q
from database import DataBase

TOKEN = '5745511209:AAH6fZx8fkX_PXSoASxU74wBVpuKiGs7ofI'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


play_button = ReplyKeyboardMarkup(row_width=2,
                                  resize_keyboard=True,
                                  one_time_keyboard=True)
b1 = KeyboardButton(text='/play')
play_button.add(b1)


playagain_button = InlineKeyboardMarkup(row_width=1)
rb = InlineKeyboardButton(text='Retry!',
                          callback_data='r')
playagain_button.add(rb)


db = DataBase()


async def send_task(user_id: int, task1: str, task2: str, photo1: str, photo2: str):
    game_ikb1 = InlineKeyboardMarkup(row_width=1)
    game_a1 = InlineKeyboardButton(text=task1,
                                   callback_data='1')
    game_ikb1.add(game_a1)

    game_ikb2 = InlineKeyboardMarkup(row_width=1)
    game_b1 = InlineKeyboardButton(text=task2,
                                   callback_data='2')
    game_ikb2.add(game_b1)

    await bot.send_photo(chat_id=user_id,
                         photo=photo1,
                         reply_markup=game_ikb1)

    await bot.send_photo(chat_id=user_id,
                         photo=photo2,
                         reply_markup=game_ikb2)


async def callback_handler(user_id, variant: str):
    if variant == db.get_user_data(user_id)[7]:
        db.change_points(user_id, True)
        reply_correct = f"Correct!\n\n{db.get_user_data(user_id)[3]}:\n{'{:,}'.format(db.get_user_data(user_id)[5])}\n{db.get_user_data(user_id)[4]}:\n{'{:,}'.format(db.get_user_data(user_id)[6])}\n\nScore: {db.get_user_data(user_id)[2]}"
        await bot.send_message(user_id, reply_correct)

        q_data = gen_q()
        db.upd_user_data(user_id,
                         task1=q_data[0],
                         task2=q_data[1],
                         number1=q_data[2],
                         number2=q_data[3],
                         comp=q_data[4])
        await send_task(user_id,
                        task1=q_data[0],
                        task2=q_data[1],
                        photo1=q_data[5],
                        photo2=q_data[6])

    else:
        db.change_status(user_id)
        if db.get_user_data(user_id)[2] > db.get_user_data(user_id)[8]:
            db.change_points(user_id, max_points=db.get_user_data(user_id)[2])
        reply_incorrect = f"You're wrong!\n\n{db.get_user_data(user_id)[3]}:\n{'{:,}'.format(db.get_user_data(user_id)[5])}\n{db.get_user_data(user_id)[4]}:\n{'{:,}'.format(db.get_user_data(user_id)[6])}\n\nYour score: {db.get_user_data(user_id)[2]}\nBest result: {db.get_user_data(user_id)[8]}\n\nTry again!"
        await bot.send_message(user_id, reply_incorrect, reply_markup=playagain_button)

#
# replies = {'correct' :
#
# }
