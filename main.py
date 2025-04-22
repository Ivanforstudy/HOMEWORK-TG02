
import asyncio
import os
import random

from aiogram import Bot, Dispatcher, F, types
from aiogram import executor
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator
from config import TOKEN

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from aiogram.executor import start_polling
from googletrans import AsyncTranslator  # Используем AsyncTranslator

bot = Bot(token='YOUR_BOT_TOKEN')
storage = MemoryStorage()
dp = Dispatcher(storage)
translator = AsyncTranslator()  # Создаем экземпляр AsyncTranslator

@dp.message(F.text & F.command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Отправь мне текст для перевода.")

@dp.message(F.text)
async def translate_text(message: types.Message):
    # Теперь используем await для вызова метода translate
    translated = await translator.translate(message.text, dest='en')  # Используем await
    await message.answer(translated.text)

async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())