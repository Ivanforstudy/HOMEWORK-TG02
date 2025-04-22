import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ContentType
from aiogram.fsm.storage.memory import MemoryStorage
from deep_translator import GoogleTranslator
from gtts import gTTS

API_TOKEN = '8035496523:AAHcY13y2KLb5tmFc6llXsDdFuiEzt9DrAQ'

# Создаём папку для изображений
os.makedirs("img", exist_ok=True)

# Инициализация бота и хранилища
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 📷 Обработка фотографий
@dp.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]  # самое большое по качеству
    file = await bot.get_file(photo.file_id)
    file_name = f"img/{photo.file_id}.jpg"
    await bot.download_file(file.file_path, destination=file_name)
    await message.answer("Фото сохранено ✅")

# 🗣 Обработка текста
@dp.message(F.text & ~F.text.startswith('/'))
async def handle_text(message: Message):
    # Перевод текста
    translated_text = GoogleTranslator(source='auto', target='en').translate(message.text)
    await message.answer(f"Перевод на английский:\n{translated_text}")

    # Озвучка
    tts = gTTS(translated_text, lang='en')
    voice_path = f"voice_{message.message_id}.ogg"
    tts.save(voice_path)

    # Отправка голосового
    voice_file = FSInputFile(voice_path)
    await message.answer_voice(voice_file)

    # Удаление временного файла
    os.remove(voice_path)

# 🔊 Обработка команды /voice
@dp.message(F.text == "/voice")
async def send_sample_voice(message: Message):
    voice_path = "1718883178_sample4.ogg"
    if os.path.exists(voice_path):
        voice = FSInputFile(voice_path)
       
        await message.answer_voice(voice)
    else:
        await message.answer("Аудиофайл не найден 😥")

# 🚀 Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
