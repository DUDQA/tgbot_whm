from aiogram import Bot, Dispatcher, executor, types

from creds_ import TOKEN
from utilities import send_task, callback_handler, play_button
from gamelogic import task_generator
from database import DataBase

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

db = DataBase()


@dp.message_handler(commands=['help'])
async def info(message: types.Message) -> None:
    await message.answer(
        text=f'bot is made for fun\nstreaming data taken from Spotify\nсomments and suggestions: @noe3g',
        reply_markup=play_button)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message) -> None:
    await message.answer(
        text=f'Hi! WhoHasMoreBot here!\n\nYou have to choose between two songs and guess the most popular track!\n\nJust push the /play button!',
        reply_markup=play_button)


@dp.message_handler(commands=['play'])
async def sender(message: types.Message = None, new_task1=None, new_task2=None, user_id=None) -> None:
    if new_task1 is None:
        try:
            user_id = message.from_user.id
        except AttributeError:
            user_id = user_id
        if db.get_user_data(user_id) is None:
            db.set_user_data(user_id=user_id,
                             in_game_status=True,
                             current_points=0,
                             max_points=0)
            question_data = task_generator()
            db.upd_user_data(user_id,
                             task1=question_data['option_1'],
                             task2=question_data['option_2'],
                             number1=question_data['streams_1'],
                             number2=question_data['streams_2'],
                             comp=question_data['comparison'])
            await send_task(user_id, question_data)

        else:
            question_data = task_generator()
            db.change_points(user_id=user_id, current_points=0)
            db.change_status(user_id, True)
            db.upd_user_data(user_id,
                             task1=question_data['option_1'],
                             task2=question_data['option_2'],
                             number1=question_data['streams_1'],
                             number2=question_data['streams_2'],
                             comp=question_data['comparison'])
            await send_task(user_id, question_data)


@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery) -> None:
    if callback.data == '1':
        user_id = callback.from_user.id
        await callback_handler(user_id, '1')

    elif callback.data == '2':
        user_id = callback.from_user.id
        await callback_handler(user_id, '2')

    elif callback.data == 'r':
        user_id = callback.from_user.id
        await sender(user_id=user_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
