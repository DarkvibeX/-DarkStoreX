
    import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8300855538:AAHC2Q_06NqApt-MSSqqjV40Vc4oGRSA8bk"
ADMIN_ID = 5487567171

bot = Bot(token=TOKEN)
dp = Dispatcher()

CARD_NUMBER = "5614 6822 1054 1860"
LOCATION_LINK = "https://maps.google.com/?q=Megaplanet+Tashkent"


# =========================
# 📦 ДАННЫЕ
# =========================

robux_products = {
    "40 Robux": 15000,
    "80 Robux": 25000,
    "120 Robux": 40000,
    "200 Robux": 50000,
    "400 Robux": 110000,
    "800 Robux": 180000,
    "1000 Robux": 250000,
    "24000 Robux": 4500000
}

const brainrot_products = {
  "Booppin bunny": { price: 285000, available: true },
  "Spooky and Pumpkin": { price: 350000, available: true },
  "Fragrama and Chocrama": { price: 320000, available: true },
  "Cerberus": { price: 270000, available: true },
  "Cash or Card": { price: 300000, available: true },
  "La Caso Boo": { price: 540000, available: true },
  "Foxini Lanterini": { price: 500000, available: true },
  "Reinito Sleighito": { price: 270000, available: true },
  "Frago La La La": { price: 360000, available: true },
  "Gym Broos": { price: 1000000, available: true },
  "Camera Ramena": { price: 60000, available: true },
  "Rosey and Teddy": { price: 600000, available: true },

  "Los chilinis": { price: 1300000, available: false },
  "Fortunu and Cashuru": { price: 250000, available: true },

  "Dragon Caneloni": { price: 1000000, available: true },
  "Hydra Dragon": { price: 1450000, available: true },

  "Dragon Gingerini": { price: 2000000, available: false },
  "Rico Dinero": { price: 1700000, available: false },

  "Acrodragon": { price: 6000000, available: false },

  "Pancake and Syrup": { price: 4000000, available: false },

  "Cookie and Milki": { price: 270000, available: true },
  "Los Amigos": { price: 270000, available: true },
  "Los Sekolah": { price: 300000, available: true },
  "Ketupat Bros": { price: 870000, available: true },

  "Elefanto Frigo": { price: 1800000, available: false },

  "Cloverat Calapat": { price: 200000, available: true },

  "Signore Carapace": { price: 4000000, available: false },

  "Skibidi Toilet": { price: 40000000, available: true },
  "Griffin": { price: 50000000, available: true },

  "Headless Horsemen": { price: 150000000, available: false },

  "Hydra Bunny": { price: 1800000, available: true },
  "Bunny and Eggy": { price: 1400000, available: true },

  "Meowl": { price: 70000000, available: true },

  "Strawberry Elephant": { price: 100000000, available: false }
};

user_cart = {}
user_category = {}


# =========================
# 📌 КЛАВИАТУРЫ
# =========================

def category_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Robux")],
            [KeyboardButton(text="🧠 Brainrots")]
        ],
        resize_keyboard=True
    )


def robux_kb():
    kb = []
    row = []

    for name in robux_products.keys():
        row.append(KeyboardButton(text=name))
        if len(row) == 2:
            kb.append(row)
            row = []

    if row:
        kb.append(row)

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def brainrots_kb():
    kb = []
    row = []

    for name in brainrot_products.keys():
        row.append(KeyboardButton(text=name))
        if len(row) == 2:
            kb.append(row)
            row = []

    if row:
        kb.append(row)

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


pay_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💵 Наличные")],
        [KeyboardButton(text="💳 Карта")]
    ],
    resize_keyboard=True
)


# =========================
# 🚀 START
# =========================

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "🔥 Выберите категорию:",
        reply_markup=category_kb()
    )


# =========================
# 📂 КАТЕГОРИИ
# =========================

@dp.message(lambda m: m.text in ["🎮 Robux", "🧠 Brainrots"])
async def choose_category(message: Message):

    user_category[message.from_user.id] = message.text

    if message.text == "🎮 Robux":
        await message.answer("Выберите Robux:", reply_markup=robux_kb())

    if message.text == "🧠 Brainrots":
        await message.answer("Выберите товар:", reply_markup=brainrots_kb())


# =========================
# 📦 ВЫБОР ТОВАРА
# =========================

@dp.message(lambda m: m.text in robux_products or m.text in brainrot_products)
async def select_product(message: Message):

    product = message.text

    # ROBUX
    if product in robux_products:
        price = robux_products[product]
        available = True

    # BRAINROTS
    else:
        item = brainrot_products[product]
        price = item["price"]
        available = item["available"]

    # ❌ SOLD OUT
    if not available:
        await message.answer(
            "❌ SOLD OUT!\nВыберите другой товар 👇",
            reply_markup=brainrots_kb()
        )
        return

    user_cart[message.from_user.id] = product

    await message.answer(
        f"🛒 Товар: {product}\n💰 Цена: {price} UZS\n\nВыберите оплату:",
        reply_markup=pay_kb
    )


# =========================
# 💵 НАЛИЧКА
# =========================

@dp.message(F.text == "💵 Наличные")
async def cash(message: Message):

    user = message.from_user
    product = user_cart.get(user.id, "Неизвестно")

    await message.answer(
        f"📍 Придите сюда:\n{LOCATION_LINK}\n\n📦 Заказ принят"
    )

    await bot.send_message(
        ADMIN_ID,
        f"🆕 ЗАКАЗ (НАЛИЧКА)\n"
        f"Товар: {product}\n"
        f"User: @{user.username if user.username else user.first_name}\n"
        f"ID: {user.id}"
    )


# =========================
# 💳 КАРТА
# =========================

@dp.message(F.text == "💳 Карта")
async def card(message: Message):

    user = message.from_user
    product = user_cart.get(user.id, "Неизвестно")

    await message.answer(
        f"💳 Переведите:\n{CARD_NUMBER}\n\n📸 Отправьте чек"
    )

    await bot.send_message(
        ADMIN_ID,
        f"💳 ЗАКАЗ\nТовар: {product}\nID: {user.id}\nОжидается чек"
    )


# =========================
# 📸 ЧЕК
# =========================

@dp.message(F.photo)
async def check(message: Message):

    user = message.from_user

    await bot.send_message(
        ADMIN_ID,
        f"📸 ЧЕК\nUser: @{user.username if user.username else user.first_name}\nID: {user.id}"
    )

    await message.answer("✅ Чек получен!")


# =========================
# ▶️ RUN
# =========================

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())