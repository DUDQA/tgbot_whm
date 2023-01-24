import logging

from aiogram import Bot, Dispatcher, executor, types

from settings import TOKEN, send_task, callback_handler, play_button
from gamelogic import gen_q
from database import DataBase

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

db = DataBase()


@dp.message_handler(commands=['help'])
async def info(message: types.Message):
    await message.answer(
        text=f'bot is made for fun\nstreaming data taken from Spotify\nсomments and suggestions: @noe3g',
        reply_markup=play_button)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # user_id = message.from_user.id
    # user_first_name = message.from_user.first_name
    # user_full_name = message.from_user.full_name
    # logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')

    await message.answer(
        text=f'Hi! WhoHasMoreBot here!\n\nYou have to choose between two songs and guess the most popular track!\n\nJust push the /play putton!',
        reply_markup=play_button)


@dp.message_handler(commands=['play'])
async def sender(message: types.Message = None, new_task1=None, new_task2=None, user_id=None):
    if new_task1 is None:  # если это первый вопрос в викторине
        try:
            user_id = message.from_user.id
        except AttributeError:
            user_id = user_id
        if db.get_user_data(user_id) is None:  # если это первая игра пользователя
            db.set_user_data(user_id=user_id,
                             in_game_status=True,
                             current_points=0,
                             max_points=0)
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

        else:  # это не первая игра пользователя,
            q_data = gen_q()  # но первый вопрос, поэтому статус=в_игре, текущие_очки=0
            db.change_points(user_id=user_id, current_points=0)
            db.change_status(user_id, True)
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


@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
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
