import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8511239792:AAEY5eksJtfvFpLstMFUQE9tN7QDU5nrWw8"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    
    # ВАЖНО: Замените URL на ваш реальный GitHub Pages URL
    github_url = "https://ваш-логин.github.io/telegram-quiz-app/"
    
    keyboard = [
        [InlineKeyboardButton("🎮 Открыть викторину", web_app=WebAppInfo(url=github_url))],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "🎮 Нажмите кнопку ниже, чтобы открыть викторину.\n"
        "Игра откроется прямо в Telegram!",
        reply_markup=reply_markup
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статистика"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("🎮 Играть", callback_data="play")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📊 Статистика\n\n"
        "🎮 Откройте мини-приложение для игры и просмотра статистики!",
        reply_markup=reply_markup
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("🎮 Играть", callback_data="play")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "❓ Помощь\n\n"
        "1. Нажмите '🎮 Открыть викторину'\n"
        "2. Выберите режим игры\n"
        "3. Отвечайте на вопросы\n"
        "4. Зарабатывайте очки!\n\n"
        "⏱️ На каждый вопрос дается 30 секунд(вы чето зажрались",
        reply_markup=reply_markup
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начать игру"""
    query = update.callback_query
    await query.answer()
    
    github_url = "https://ваш-логин.github.io/telegram-quiz-app/"
    
    keyboard = [[InlineKeyboardButton("🎮 Открыть викторину", web_app=WebAppInfo(url=github_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎮 Нажмите кнопку ниже, чтобы начать игру!",
        reply_markup=reply_markup
    )

def main():
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(stats, pattern='^stats$'))
    application.add_handler(CallbackQueryHandler(help, pattern='^help$'))
    application.add_handler(CallbackQueryHandler(play, pattern='^play$'))
    
    print("✅ Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
