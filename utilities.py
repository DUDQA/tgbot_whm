from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from gamelogic import task_generator
from database import DataBase
from creds_ import TOKEN

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


async def send_task(user_id: int, question_data: dict) -> None:
    """Sends two messages as a game task to user."""
    answer_button_1 = InlineKeyboardMarkup(row_width=1)
    game_a1 = InlineKeyboardButton(text=question_data['option_1'],
                                   callback_data='1')
    answer_button_1.add(game_a1)

    answer_button_2 = InlineKeyboardMarkup(row_width=1)
    game_b1 = InlineKeyboardButton(text=question_data['option_2'],
                                   callback_data='2')
    answer_button_2.add(game_b1)

    task1 = await bot.send_photo(chat_id=user_id,
                                 photo=question_data['photo_1'],
                                 reply_markup=answer_button_1)
    task2 = await bot.send_photo(chat_id=user_id,
                                 photo=question_data['photo_2'],
                                 reply_markup=answer_button_2)
    if db.get_msgid(user_id=user_id) is None:
        db.set_msgid(user_id=user_id,
                     message_id1=task1.message_id,
                     message_id2=task2.message_id)
    else:
        db.upd_msgid(user_id=user_id,
                     message_id1=task1.message_id,
                     message_id2=task2.message_id)


async def callback_handler(user_id: int, variant: str) -> None:
    """Decides if the answer is correct."""
    if variant == db.get_user_data(user_id)['comparison']:
        db.change_points(user_id, True)
        await bot.delete_message(chat_id=user_id, message_id=db.get_msgid(user_id)[0])
        await bot.delete_message(chat_id=user_id, message_id=db.get_msgid(user_id)[1])
        reply_correct = f"Correct!\n\n{db.get_user_data(user_id)['task_1']}:\n" \
                        f"{'{:,}'.format(db.get_user_data(user_id)['streams_1'])}\n" \
                        f"{db.get_user_data(user_id)['task_2']}:\n" \
                        f"{'{:,}'.format(db.get_user_data(user_id)['streams_2'])}\n\n" \
                        f"Score: {db.get_user_data(user_id)['current_points']}"
        await bot.send_message(user_id, reply_correct)

        question_data = task_generator()
        db.upd_user_data(user_id,
                         task1=question_data['option_1'],
                         task2=question_data['option_2'],
                         number1=question_data['streams_1'],
                         number2=question_data['streams_2'],
                         comp=question_data['comparison'])
        await send_task(user_id, question_data)

    else:
        db.change_status(user_id)
        if db.get_user_data(user_id)['current_points'] > db.get_user_data(user_id)['max_points']:
            db.change_points(user_id, max_points=db.get_user_data(user_id)['current_points'])
        await bot.delete_message(chat_id=user_id, message_id=db.get_msgid(user_id)[0])
        await bot.delete_message(chat_id=user_id, message_id=db.get_msgid(user_id)[1])
        reply_incorrect = f"You're wrong!\n\n{db.get_user_data(user_id)['task_1']}:\n" \
                          f"{'{:,}'.format(db.get_user_data(user_id)['streams_1'])}\n" \
                          f"{db.get_user_data(user_id)['task_2']}:\n" \
                          f"{'{:,}'.format(db.get_user_data(user_id)['streams_2'])}\n\n" \
                          f"Your score: {db.get_user_data(user_id)['current_points']}\n" \
                          f"Best result: {db.get_user_data(user_id)['max_points']}\n\nTry again!"
        await bot.send_message(user_id, reply_incorrect, reply_markup=playagain_button)

#