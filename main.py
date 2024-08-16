import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import TOKEN, FOOTBALL_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения списка лиг
def get_leagues():
    url = 'https://api-football-v1.p.rapidapi.com/v3/leagues'
    headers = {"x-rapidapi-key": FOOTBALL_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Функция для получения команд и их положения
def get_standings(league_id):
    url = f'https://api-football-v1.p.rapidapi.com/v3/standings?season=2023&league={league_id}'
    headers = {"x-rapidapi-key": FOOTBALL_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Функция для получения информации о лиге по названию страны
def get_league_info(country_name):
    leagues = get_leagues()
    for league in leagues['response']:
        if league['country']['name'].lower() == country_name.lower():
            return league['league']['id']
    return None

@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет! Я твой информационный бот о футбольных лигах. Введи название страны на английском языке.")

@dp.message()
async def send_league_info(message: Message):
    country = message.text
    league_id = get_league_info(country)

    if league_id:
        standings = get_standings(league_id)
        if standings['response']:
            teams_info = standings['response'][0]['league']['standings'][0]

            response = "Текущие команды в лиге:\n"
            for team in teams_info:
                response += f"{team['team']['name']}: {team['points']} очков\n"

            await message.reply(response)
        else:
            await message.reply("Извините, не удалось получить данные о турнирной таблице.")
    else:
        await message.reply("Извините, ничего не удалось найти.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())