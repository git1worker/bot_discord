import discord, sqlite3, time, asyncio, time
from config import *
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)

flag = False
list_warnings = []
messages = {}


def member_messenger(id):  # Подсчет сообщений
    global messages
    if id in messages:
        messages[id] = messages[id] + 1
    else:
        messages[id] = 1


async def antispam(k):  # Вызов предупреждения по спаму
    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
    num = cursor.fetchone()[4]
    cursor.execute(f"""UPDATE dis_users SET warnings = {num + 1} WHERE id_discord = {k}""")

    user = client.get_user(k)
    if num + 1 > 3:
        await k.send("Ты был кикнут за спам")
        await guild.kick(user=k, reason="Спам")
    elif num + 1 > 2:
        await text_chann.send(f"Последнее предупреждение у участника {user.name} за спам")
    else:
        await text_chann.send(f"{num + 1} предупреждение у участника {user.name} за спам")
    conn.commit()


async def timer_messages(num_messages_in_3_sec):
    global flag
    global messages
    global list_warnings
    flag = True

    await asyncio.sleep(3)

    for k, v in messages.items():

        if v > num_messages_in_3_sec:  # Количество сообщений за 3 секунды # Антиспам!
            await antispam(k)  # Вызов предупреждения по спаму
        cursor.execute(f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {k}""")  # Обнуление счетчика афк
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
        num = cursor.fetchone()[2]
        cursor.execute(f"""UPDATE dis_users SET num_mess = {num + v} WHERE id_discord = {k}""")
        conn.commit()

    flag = False
    messages = {}


async def timer_min():
    global afk_voice
    while True:
        members = guild.members
        for member in members:
            if member.bot:
                continue
            if member.voice is not None and member.voice.channel != afk_voice:  # Если участник в войсе и не в афк

                cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
                num = cursor.fetchone()[3]
                cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                = {num + 1} WHERE id_discord = {member.id}""")  # Счет времени в войсе
                cursor.execute(f"""UPDATE dis_users SET time_afk = 
                0 WHERE id_discord = {member.id}""")  # Обнуление счетчика афк
                conn.commit()
            cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
            num = cursor.fetchone()[5]
            if num > 20160:  # Если афк больше 2 недель кик
                await member.send("Ты был кикнут за неактивность")
                await guild.kick(user=member, reason="Неактивность")
            elif num > 10080: # Если время афк больше недели добавление роли трупак
                await member.add_roles(dead)
            cursor.execute(f"""UPDATE dis_users SET time_afk = {num + 1} WHERE id_discord = {member.id}""")
            conn.commit()
        print(1)
        await asyncio.sleep(60)



@client.event
async def on_ready():
    global text_chann
    global conn
    global cursor
    global guild
    global new_role
    global afk_voice
    global dead

    text_chann = client.get_channel(938411811173199955)  # текстовый канал куда пишет bot
    guild = client.get_guild(938411811173199952)  # Объект сервера
    new_role = guild.get_role(941606299144171591)  # Роль для новичка
    afk_voice = guild.get_channel(944144703148937216)  # Объект афк канала
    dead = guild.get_role(944202377500717126)  # Роль Труп

    conn = sqlite3.connect("./mydatabase.db") # Соединение с бд
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE dis_users SET warnings = 0 WHERE id_discord = 869217405862305822""")  # Обнуление предупреждений
    conn.commit()
    await timer_min()  # Обновление каждую минуту время в войсе и афк


@client.event
async def on_member_join(member):
    await member.send(f"Welcome {member.name}")  # Бот пишет в лс
    await text_chann.send(f"welcome {member.name}")  # Бот пишет в text chann
    await member.add_roles(new_role)  # Добавление новичку роли
    cursor.execute(f"""INSERT INTO dis_users
                      VALUES ('{member.id}', '1', '0',
                      '0', '0', '0')""")
    conn.commit()  # Сохранение изменений в бд


@client.event
async def on_message(message):
    if message.author.bot:  # Проверка на сообщение от пользователя
        return

    if message.channel.id == 938411811173199955:  # Проверка на основной канал
        member_messenger(message.author.id)  # Подсчет сообщений
        if not flag:
            if len(str(message.content)) > 400:  # Если больше 400 сим удаление и предупреждение
                await antispam(message.author.id)
                await message.delete()
            else:
                await timer_messages(3)  # Если меньше 400 символов за 3 секунд ограничение - 4 сообщений
    elif message.channel.id == 944209923645001728:  # Канал для комманд боту
        await client.process_commands(message)

    """КОМАНДЫ"""

@client.command()
async def help_me(ctx):  # Команда help_me Выводит доступные команды
    await ctx.send("$get_info_voice id  - Сколько участник сидел в голосовом чате (id человека)\n"
                   "\n$get_info_messages id  - Сколько участник писал в текстовом чате (id человека)\n"
                   "\n$get_info_warnings id  - Сколько у участника предупреждений (id человека)")

@client.command()
async def get_info_voice(ctx, arg):  # Команда get_info_voice Выводит время в голосовых чатах
    global cursor
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")

        user = guild.get_member(int(arg))
        num = cursor.fetchone()[3]

        if num > 60:
            num = num / 60
            await ctx.send(f"{user.name} сидел в голосовом чате {num} ч.")
        else:
            await ctx.send(f"{user.name} сидел в голосовом чате {num} м.")
    except:
        await ctx.send("Произошла ошибка")

@client.command()
async def get_info_messages(ctx, arg):  # Команда get_info_messages Выводит число сообщений за все время
    global cursor
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        user = guild.get_member(int(arg))
        num = cursor.fetchone()[2]
        await ctx.send(f"{user.name} написал {num} сообщ.")

    except:
        await ctx.send("Произошла ошибка")

@client.command()
async def get_info_warnings(ctx, arg):  # Команда get_info_warnings Выводит число предупреждений
    global cursor
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        user = guild.get_member(int(arg))
        num = cursor.fetchone()[4]
        await ctx.send(f"{user.name} получил {num} предупр.")
    except:
        await ctx.send("Произошла ошибка")

if __name__ == '__main__':
    client.run(token)
