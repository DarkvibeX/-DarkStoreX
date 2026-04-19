import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8300855538:AAHC2Q_06NqApt-MSSqqjV40Vc4oGRSA8bk"
ADMIN_ID = 5487567171

bot = Bot(token=TOKEN)
dp = Dispatcher()

CARD_NUMBER = "5614 6822 1054 1860"
LOCATION_LINK = "https://maps.google.com/?q=Megaplanet+Tashkent"

# 🛒 ТОВАРЫ
products = {
     "Booppin bunny": 285000,
    "Spooky and Pumpkin": 350000,
    "Fragrama and Chocrama": 320000,
    "Cerberus": 270000,
    "Cash or Card": 300000,
    "La Caso Boo": 540000,
    "Foxini Lanterini": 500000,
    "Reinito Sleighito": 270000,
    "Frago La La La": 360000,
    "Gym Broos": 1000000,
    "Camera Ramena": 60000,
    "Rosey and Teddy": 600000,
    "Los chilinis": 1300000,
    "Fortunu and Cashuru": 250000,
    "Dragon Caneloni": 1000000,
    "Hydra Dragon": 1450000,
    "Dragon Gingerini": 2000000,
    "Rico Dinero": 1700000,
    "Acrodragon": 6000000,
    "Pancake and Syrup": 4000000,
    "Cookie and Milki": 270000,
    "Los Amigos": 270000,
    "Los Sekolah": 300000,
    "Ketupat Bros": 870000,
    "Elefanto Frigo": 1800000,
    "Cloverat Calapat": 200000,
    "Signore Carapace": 4000000,
    "Skibidi Toilet": 40000000,
    "Griffin": 50000000,
    "Headless Horsemen": 150000000,
    "Hydra Bunny": 1800000,
    "Bunny and Eggy": 1400000,
    "Meowl": 70000000,
    "Strawberry Elephant": 100000000
}

user_cart = {}

# 📦 клавиатура товаров
def product_kb():
    kb = []
    row = []

    for name in products.keys():
        row.append(KeyboardButton(text=name))
        if len(row) == 2:
            kb.append(row)
            row = []

    if row:
        kb.append(row)

    kb.append([KeyboardButton(text="🛒 Купить")])

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# 💳 оплата
pay_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💵 Наличные")],
        [KeyboardButton(text="💳 Карта")]
    ],
    resize_keyboard=True
)

# /start
@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "🔥 Добро пожаловать в DarkStoreX!\nВыберите товар:",
        reply_markup=product_kb()
    )

# выбор товара
@dp.message(lambda m: m.text in products)
async def select_product(message: Message):

    user_cart[message.from_user.id] = message.text

    price = products[message.text]

    await message.answer(
        f"🛒 Вы выбрали: {message.text}\n💰 Цена: {price} UZS\n\nВыберите оплату:",
        reply_markup=pay_kb
    )

# 💵 наличка
@dp.message(F.text == "💵 Наличные")
async def cash(message: Message):

    user = message.from_user
    product = user_cart.get(user.id, "Неизвестно")
    price = products.get(product, 0)

    username = f"@{user.username}" if user.username else user.first_name

    await message.answer(
        f"📍 Придите сюда:\n{LOCATION_LINK}\n\n📦 Заказ принят"
    )

    await bot.send_message(
        ADMIN_ID,
        f"🆕 ЗАКАЗ (НАЛИЧКА)\n"
        f"Товар: {product}\n"
        f"Цена: {price} UZS\n"
        f"Пользователь: {username}\n"
        f"ID: {user.id}"
    )

    await message.answer("✅ Заказ отправлен владельцу")

# 💳 карта
@dp.message(F.text == "💳 Карта")
async def card(message: Message):

    user = message.from_user
    product = user_cart.get(user.id, "Неизвестно")
    price = products.get(product, 0)

    username = f"@{user.username}" if user.username else user.first_name

    await message.answer(
        f"💳 Переведите:\n{CARD_NUMBER}\n\n📸 Отправьте чек"
    )

    await bot.send_message(
        ADMIN_ID,
        f"💳 ЗАКАЗ (КАРТА)\n"
        f"Товар: {product}\n"
        f"Цена: {price} UZS\n"
        f"Пользователь: {username}\n"
        f"ID: {user.id}\n"
        f"⚠️ Ожидается чек"
    )

# 📸 чек
@dp.message(F.photo)
async def check(message: Message):

    user = message.from_user
    username = f"@{user.username}" if user.username else user.first_name

    await bot.send_message(
        ADMIN_ID,
        f"📸 ЧЕК\n"
        f"Пользователь: {username}\n"
        f"ID: {user.id}"
    )

    await message.answer("✅ Чек получен! Скоро свяжемся.")

# запуск
async def main():
    print("DarkStoreX PRO запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())