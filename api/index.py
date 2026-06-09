import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler

# --- CONFIGURATION ---
BOT_TOKEN = os.getenv("BOT_TOKEN")

COURSES = [
    {"name": "Primary and Middle School Leadership Training (Module 1)", "url": "https://app.mindsmith.ai/course/cmq2dkj1p010o04icv2shjkel/learn"},
    {"name": "Primary and Middle School Leadership Training (Module 2)", "url": "https://app.mindsmith.ai/course/cmq2xvppe00dg04lb4716kb81/learn"},
    {"name": "Pre-Primary School Leadership Training (Module 1)", "url": "https://app.mindsmith.ai/course/cmpwkef3f02dw04la3bv6vrwn/learn"},
    {"name": "Pre-Primary School Leadership Training (Module 2)", "url": "https://app.mindsmith.ai/course/cmq2yco2m008b04k3ojkz98t0/learn"},
]

app = FastAPI()

# Global variable for the application instance
ptb_app = None

async def get_ptb_app():
    global ptb_app
    if ptb_app is None:
        ptb_app = ApplicationBuilder().token(BOT_TOKEN).build()
        ptb_app.add_handler(CommandHandler("start", start))
        # This is the key: initialize the app before it starts taking requests
        await ptb_app.initialize()
    return ptb_app

async def start(update: Update, context):
    keyboard = []
    for course in COURSES:
        keyboard.append([InlineKeyboardButton(text=f"{course['name']}", web_app=WebAppInfo(url=course['url']))])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Select a course to begin:", reply_markup=reply_markup)

@app.post("/api/webhook")
async def webhook_handler(request: Request):
    bot_instance = await get_ptb_app()
    data = await request.json()
    update = Update.de_json(data, bot_instance.bot)
    
    # Process the update through the library logic
    await bot_instance.process_update(update)
    
    return {"status": "ok"}

@app.get("/")
def index():
    return {"message": "Mindsmith Bot is running!", "token_present": BOT_TOKEN is not None}