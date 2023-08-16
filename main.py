import os
import json
import dotenv

from pyrogram import Client, filters, types


dotenv.load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')


app = Client(
    'client',
    api_id=API_ID,
    api_hash=API_HASH
)


def load_imagen() -> None:
    imagen = None
    
    with open('settings.json', 'r', encoding='utf-8') as f:
        settings: dict = json.load(f)
        imagen = settings.get('imagen_name')
        
    return imagen


def load_chats() -> None:
    chats = []
    
    with open('chats.json', 'r', encoding='utf-8') as f:
        chats_dict: dict = json.load(f)
        chats = chats_dict.get('chats', ['me'])
        
    return chats


def add_chat(chat_id) -> None:
    with open('chats.json', 'r', encoding='utf-8') as f:
        chats_dict: dict = json.load(f)
        chats_dict.get('chats', ['me']).append(chat_id)
        
    with open('chats.json', 'w', encoding='utf-8') as f:
        json.dump(chats_dict, f, indent=4)

      
@app.on_message(filters.me & filters.regex(r'^show chat id$'))
async def show_chat_id(app: Client, message: types.Message):
    await message.delete()
    await app.send_message(
        'me',
        f'Chat ID: {message.chat.id}'
    )


@app.on_message(filters.me & filters.regex(r'^add chat id$'))
async def show_chat_id(app: Client, message: types.Message):
    await message.delete()
    
    add_chat(message.chat.id)
    
    await app.send_message(
        'me',
        f'Add ID: {message.chat.id}\n Tittle: {message.chat.title or message.chat.first_name}'
    )
    

@app.on_message(filters.me & filters.regex(r'^show user id$'))
async def show_user_id(app: Client, message: types.Message):
    await message.delete()
    
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        
        await app.send_message(
            'me',
            f'ID: {user.id}\nFN: {user.first_name}\nUN: {user.username}\n'
        )


@app.on_message(filters.me & filters.regex(r'^send promo$'))
async def send_promo(app: Client, message: types.Message):
    goal_chats = load_chats()
    
    if message.reply_to_message:
        
        if message.reply_to_message.photo:
            
            for chat in goal_chats:
                try:
                    await app.send_photo(
                        chat_id=chat,
                        photo=message.reply_to_message.photo.file_id,
                        caption=message.reply_to_message.caption
                    )
                except Exception as e:
                    print(e)
                
            return
        
        for chat in goal_chats:
            try:
                await app.send_message(
                    chat,
                    message.reply_to_message.text
                )
            except Exception as e:
                    print(e)


def main() -> None:
    if API_ID is None or API_HASH is None:
        exit(1)

    app.run()
    
    
if __name__ == '__main__':
    main()