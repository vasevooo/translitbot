import os
import logging

from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.getenv('TOKEN')


#set up a logging file 'mylog'
logging.basicConfig(filename='mylog.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Send a message asking for the user's full name
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    reply_text = f'{user_name}, please enter your full name (in Cyrillic):'
    logging.info(f'{user_name=} {user_id=} sent message: {message.text}')
    await message.reply(reply_text)

#transliterate a message of a user
@dp.message_handler()
async def process_full_name(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    full_name = message.text
    
    if not is_cyrillic(full_name):
        await bot.send_message(user_id, "Please enter your full name in Cyrillic.")
        return

    transliterated_name = transliterate(full_name)
    logging.info(f'{user_name=} {user_id=} sent message: {message.text}')
    await bot.send_message(user_id, f"Your transliterated name is {transliterated_name}")


# transliterate function according to the rules of Ministry of Foreign Affairs
def transliterate(text):
    translit_map = {
       
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'Zh', 'З': 'Z',
        'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
        'Ъ': 'IE', 'Ы': 'Y', 'Ь': '', 'Э': 'IE', 'Ю': 'IU', 'Я': 'IA'
    }
    
    result = ''
    text = text.upper()
    for char in text:
        if char in translit_map:
            result += translit_map[char]
        else:
            result += char
    return result


# Check if all characters in the text are in the Cyrillic Unicode range or '-'
def is_cyrillic(text):
    text = text.replace (' ', '')
    return all(ord(char) >= 0x0400 and ord(char) <= 0x04FF or ord(char) == 45 for char in text)



if __name__ == '__main__':
    executor.start_polling(dp)




