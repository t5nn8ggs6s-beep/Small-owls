import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery

# ВСТАВЬ СВОЙ ТОКЕН СЮДА В КАВЫЧКАХ
TOKEN = "8757534074:AAGQRn0nJbK3VtsoFW1PcVNICLhoa3pX9M0" 
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = [[types.InlineKeyboardButton(text="Оплатить 250 ⭐", callback_data="pay_stars")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer(
        "Привет, юный друг! Хочешь получить мануалы? "
        "Но тогда нужно оплатить и там оплата будет только 250 звезд навсегда!",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "pay_stars")
async def send_payment(callback: types.CallbackQuery):
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Доступ к мануалам",
        description="Оплата доступа навсегда",
        payload="manuals_access",
        provider_token="", # Для Stars ВСЕГДА пусто
        currency="XTR",    # Валюта Stars
        prices=[LabeledPrice(label="Мануалы", amount=250)]
    )
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    # ОБЯЗАТЕЛЬНОЕ ПОДТВЕРЖДЕНИЕ ПЛАТЕЖА
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def got_payment(message: types.Message):
    # Бот ничего не пишет пользователю после оплаты, как ты и просил
    print(f"Успешная оплата от {message.from_user.id}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
