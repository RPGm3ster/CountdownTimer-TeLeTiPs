from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from plugins.teletips_t import *
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.raw.functions.messages import UpdatePinnedMessage

bot=Client(
    "Countdown-TeLeTiPs",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"],
    channel_id =  os.environ["CHANNEL_ID"]
)

footer_message = os.environ["FOOTER_MESSAGE"]

stoptimer = False

TELETIPS_MAIN_MENU_BUTTONS = [
            [
                InlineKeyboardButton('❓ HELP', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('👥 SUPPORT', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('📣 CHANNEL', url='https://t.me/kekkkkk'),
                InlineKeyboardButton('👨‍💻 CREATOR', url='https://t.me/kekkkkk')
            ],
            [
                InlineKeyboardButton('➕ CREATE YOUR BOT ➕', callback_data="TUTORIAL_CALLBACK")
            ]
        ]

@bot.on_message(filters.command(['start','help']) & filters.private)
async def start(client, message):
    text = START_TEXT
    reply_markup = InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
    await message.reply(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

@bot.on_callback_query()
async def callback_query(client: Client, query: CallbackQuery):
    if query.data=="HELP_CALLBACK":
        TELETIPS_HELP_BUTTONS = [
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK")
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_HELP_BUTTONS)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="GROUP_CALLBACK":
        TELETIPS_GROUP_BUTTONS = [
            [
                InlineKeyboardButton("TeLe TiPs Chat [EN]", url="https://t.me/kekkkkk")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_GROUP_BUTTONS)
        try:
            await query.edit_message_text(
                GROUP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    

    elif query.data=="TUTORIAL_CALLBACK":
        TELETIPS_TUTORIAL_BUTTONS = [
            [
                InlineKeyboardButton("🎥 Video", url="https://t.me/kekkkkk")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_TUTORIAL_BUTTONS)
        try:
            await query.edit_message_text(
                TUTORIAL_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass      
          
    elif query.data=="START_CALLBACK":
        TELETIPS_START_BUTTONS = [
            [
                InlineKeyboardButton('❓ HELP', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('👥 SUPPORT', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('📣 CHANNEL', url='https://t.me/kekkkkk'),
                InlineKeyboardButton('👨‍💻 CREATOR', url='https://t.me/kekkkkk')
            ],
            [
                InlineKeyboardButton('➕ CREATE YOUR BOT ➕', callback_data="TUTORIAL_CALLBACK")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_START_BUTTONS)
        try:
            await query.edit_message_text(
                START_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    

@bot.on_message(filters.command('set') & (filters.group | filters.channel))
async def set_timer(client, message):
    global stoptimer
    try:
        chat_type = message.chat.type
        if chat_type == "private":
            return await message.edit_text('⛔️ Try this command in a **group chat or channel**.')
        
        if chat_type == "channel":
            if message.chat.id != CHANNEL_ID:
                return await message.edit_text('⛔️ You can only use this command in the specified channel.')

        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if not member.privileges:
            return await message.reply('👮🏻‍♂️ Sorry, **only admins** can execute this command.')    
        
        if len(message.command) < 3:
            return await message.reply('❌ **Incorrect format.**\n\n✅ Format should be like,\n<code> /set seconds "event"</code>\n\n**Example**:\n <code>/set 10 "10 seconds countdown"</code>')    
        
        user_input_time = int(message.command[1])
        user_input_event = str(message.command[2])
        get_user_input_time = await bot.send_message(message.chat.id, user_input_event)
        await get_user_input_time.pin()
        
        if stoptimer:
            stoptimer = False
        
        if 0 < user_input_time <= 10:
            while user_input_time and not stoptimer:
                seconds = user_input_time % 60
                if seconds < 10:
                    seconds = "0" + str(seconds)
                timer_msg = f"🕒 **Countdown:** `{user_input_time}:{seconds}`\n\n{user_input_event}"
                try:
                    await get_user_input_time.edit(timer_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await get_user_input_time.edit(timer_msg)
                await asyncio.sleep(1)
                user_input_time -= 1
        
        if not stoptimer:
            await get_user_input_time.unpin()
            await message.reply('🔔 Countdown ended.')
    except Exception as e:
        print(e)
        await message.reply('❌ An error occurred while processing the command.')  
        
        
        user_input_time = int(input("How long do you want your tip to be displayed in seconds? "))
        user_input_event = str(message.command[2])
        get_user_input_time = await bot.send_message(message.chat.id, user_input_event)
        await bot.send(UpdatePinnedMessage(
        channel_id=message.chat.id,
        id=get_user_input_time.message_id,
        flags=1
    ))
        if stoptimer: stoptimer = False
        if user_input_time < 10:
                while user_input_time and not stoptimer:
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, s, footer_message)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(1)
                    user_input_time -=1
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 10 <= user_input_time <= 60:
                while user_input_time>0 and not stoptimer:
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, s, footer_message)   
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(3)
                    user_input_time -=3
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 60<=user_input_time<3600:
                while user_input_time>0 and not stoptimer:
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**m** : {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, m, s, footer_message)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(3)
                    user_input_time -=3
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 3600<=user_input_time<86400:
                while user_input_time>0 and not stoptimer:
                    h=user_input_time%(3600*24)//3600
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**h** : {:02d}**m** : {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, h, m, s, footer_message)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(7)
                    user_input_time -=7
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif user_input_time>=86400:
                while user_input_time>0 and not stoptimer:
                    d=user_input_time//(3600*24)
                    h=user_input_time%(3600*24)//3600
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**d** : {:02d}**h** : {:02d}**m** : {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, d, h, m, s, footer_message)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(9)
                    user_input_time -=9
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            else:
                await get_user_input_time.edit(f"🤷🏻‍♂️ I can't countdown from {user_input_time}")
                await get_user_input_time.unpin()
    except FloodWait as e:
        await asyncio.sleep(e.value)

@bot.on_message(filters.command('stopc'))
async def stop_timer(client, message):
    global stoptimer
    try:
        chat_id = message.chat.id or message.channel.id
        user_id = message.from_user.id
        chat_member = await bot.get_chat_member(chat_id, user_id)
        if chat_member.can_manage_chat:
            stoptimer = True
            await message.reply('🛑 Countdown stopped.')
        else:
            await message.reply('👮🏻‍♂️ Sorry, **only admins** can execute this command.')
    except FloodWait as e:
        await asyncio.sleep(e.value)

print("Countdown Timer is alive!")
bot.run()
