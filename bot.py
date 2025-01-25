import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import asyncio


cred = credentials.Certificate('coffe-shop-e6629-firebase-adminsdk-y6bne-5770ed3644.json')  
firebase_admin.initialize_app(cred)
db = firestore.client()


TOKEN = '7098123323:AAFzrt9QJwPD6s-9H42LJymHcbsBWZuC0MY'

bot = Bot(token=TOKEN)


def fetch_messages():
    messages_ref = db.collection('messages')  
    docs = messages_ref.stream()
    
    messages = []
    for doc in docs:
        messages.append({
            "id": doc.id,
            "name": doc.to_dict().get('name', 'No name'),
            "email": doc.to_dict().get('email', 'No email'),
            "subject": doc.to_dict().get('subject', 'No subject'),
            "message": doc.to_dict().get('message', 'No message field')
        })
    
    return messages


def delete_message(doc_id):
    messages_ref = db.collection('messages')
    messages_ref.document(doc_id).delete()


async def send_messages(chat_id, messages):
    for message in messages:
        text = f"Name: {message['name']} | Email: {message['email']} | Subject: {message['subject']} | Message: {message['message']}"
        keyboard = [
            [InlineKeyboardButton("Xabarni o'chirish", callback_data=f'delete_{message["id"]}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        await asyncio.sleep(1)  


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id  
    keyboard = [
        [InlineKeyboardButton("Xabarlarni ko'rish", callback_data='fetch_messages')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(f'Bot ishga tushdi! Sizning chat ID: {chat_id}', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    if query.data == 'fetch_messages':
        messages = fetch_messages()  
        await send_messages(chat_id, messages)  
        await query.answer()

    
    elif query.data.startswith('delete_'):
        doc_id = query.data.split('_')[1]  
        delete_message(doc_id)  
        await query.edit_message_text(text="Xabar o'chirildi.")
        await query.answer()


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    messages = fetch_messages()  
    await send_messages(chat_id, messages)  


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id  
    await update.message.reply_text(f'Xabar qabul qilindi. Sizning chat ID: {chat_id}')
    messages = fetch_messages()  
    await send_messages(chat_id, messages)  

def main():
   
    application = Application.builder().token(TOKEN).build()

    
    application.add_handler(CommandHandler("start", start))

    
    application.add_handler(CommandHandler("messages", messages))

    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    
    application.add_handler(CallbackQueryHandler(button))

    
    application.run_polling()

if __name__ == '__main__':
    main()
