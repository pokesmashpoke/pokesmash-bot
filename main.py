import asyncio
from datetime import timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# CONFIGURAZIONE
TOKEN = "8775754630:AAGfjESXzayVsiQxnWcM5H8VYWfOa_C6hLY"
BAD_WORDS = ["frocio", "ricchione", "porcoddio", "porco dio", "porcoiddio", "porca madonna", "porcamadonna", "negro", "negri", "ebreo", "checca", "lesbica", "pedofilo"]
MUTE_TIME = 3600 # 1 ora

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.lower()
    
    if any(word in text for word in BAD_WORDS):
        user = update.message.from_user
        chat_id = update.message.chat_id
        
        try:
            # 1. Elimina il messaggio
            await update.message.delete()
            
            # 2. Muta l'utente
            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user.id,
                permissions={},
                until_date=update.message.date + timedelta(seconds=MUTE_TIME)
            )
            
            # 3. Manda l'avviso (specificando il thread_id per i topic)
            avviso = await context.bot.send_message(
                chat_id=chat_id,
                text=f"⚠️ {user.first_name}, sei stato mutato per 1 ora per linguaggio inappropriato.",
                message_thread_id=update.message.message_thread_id
            )
            
            print(f"PULIZIA: {user.first_name} mutato.")

            # 4. Cancella l'avviso dopo 10 secondi per non intasare
            await asyncio.sleep(10)
            await avviso.delete()

        except Exception as e:
            print(f"Errore: {e}")

def main():
    print("--- IL BOT POKESMASH È ONLINE CON AVVISI ---")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_message))
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()