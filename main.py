import discord, sqlite3, asyncio, time, os, datetime
from config import *
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)
DiscordComponents(client)

flag = False
list_warnings = []
authors_messages = []
messages = {}
moders = []

"""

-----START-----

"""


def member_messenger(id):  # Подсчет сообщений
    global messages
    if id in messages:
        messages[id] = messages[id] + 1
    else:
        messages[id] = 1
    # print(messages)


async def antispam(k):  # Вызов предупреждения по спаму
    if k in moders:
        return
    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
    num = cursor.fetchone()[4]
    num = int(num) + 1
    cursor.execute(f"""UPDATE dis_users SET warnings = {num} WHERE id_discord = {k}""")

    user = client.get_user(k)
    if num > 2:
        await user.send("Ты был кикнут за спам")
        await guild.kick(user=user, reason="Спам")
    elif num > 1:
        await text_chann.send(f"Последнее предупреждение у участника {user.name} за спам")
    else:
        await text_chann.send(f"{num} предупреждение у участника {user.name} за спам")
    conn.commit()


async def timer_messages(num_messages_in_3_sec):
    global flag
    global messages
    global list_warnings
    flag = True

    await asyncio.sleep(3)
    # t = time.time()
    for k, v in messages.items():
        user = guild.get_member(k)
        if v > num_messages_in_3_sec:  # Количество сообщений за 3 секунды # Антиспам!
            await antispam(k)  # Вызов предупреждения по спаму
        if dead in user.roles:
            await user.remove_roles(dead)
        # print("v", v)

        cursor.execute(f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {k}""")  # Обнуление счетчика афк
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
        num = cursor.fetchone()[1]
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
        num2 = cursor.fetchone()[2]

        if num2 + v > 200 and int(num) == 2:
            # Если человек написал больше 200 сообщений и звание сержант выдается роль майор
            cursor.execute(f"""UPDATE dis_users SET role = 2 WHERE id_discord = {k}""")
            user = guild.get_member(k)
            await user.remove_roles(sergeant)  # Удаление сержанта
            await user.add_roles(major)  # Добавление майора
            await text_chann.send(f"{user.name} повышен до {sergeant.name}")

        if num2 + v > 100 and int(num) == 1:
            # Если человек написал больше 100 сообщений и звание новобранец выдается роль сержант
            cursor.execute(f"""UPDATE dis_users SET role = 2 WHERE id_discord = {k}""")
            user = guild.get_member(k)
            await user.remove_roles(recruit)  # Удаление новобранца
            await user.add_roles(sergeant)  # Добавление сержанта
            await text_chann.send(f"{user.name} повышен до {sergeant.name}")

        cursor.execute(f"""UPDATE dis_users SET num_mess = {num2 + v} WHERE id_discord = {k}""")
        conn.commit()
    # print(time.time()-t)
    flag = False
    messages = {}


"""

-----TIMER-----

"""


async def timer_min():  # Таймер на каждую минуту
    global authors_messages

    while True:

        for i in authors_messages:
            cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {i}""")
            num = cursor.fetchone()[7]

            cursor.execute(f"""UPDATE dis_users SET chat_time 
                        = {num + 1} WHERE id_discord = {i}""")  # Счет времени в chat
            conn.commit()
        authors_messages = []
        t = time.time()
        members = guild.members
        for member in members:
            if member.bot:
                continue

            cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
            role = cursor.fetchone()[1]

            if moder in member.roles and role != 99:
                cursor.execute(f"""INSERT INTO dis_users (id_discord, role) VALUES ('{member.id}', '99')""")
                conn.commit()
                moders.append(member.id)


            if member.voice is not None and member.voice.channel != guild.get_channel(
                    944144703148937216):  # Если участник в войсе и не в афк

                cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
                num = cursor.fetchone()[3]
                cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                = {num + 1} WHERE id_discord = {member.id}""")  # Счет времени в войсе
                cursor.execute(f"""UPDATE dis_users SET time_afk = 
                0 WHERE id_discord = {member.id}""")  # Обнуление счетчика афк
                conn.commit()
            cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
            num = cursor.fetchone()[5]
            if dead in member.roles and num < 10080:  # Удаление роли трупа если число афк меньше недели
                member.remove_roles(dead)

            if num > 20160:  # Если афк больше 2 недель кик
                await member.send("Ты был кикнут за неактивность")
                await guild.kick(user=member, reason="Неактивность")
            elif num > 10080:  # Если время афк больше недели добавление роли трупак
                await member.add_roles(dead)

            cursor.execute(f"""UPDATE dis_users SET time_afk = {num + 1} WHERE id_discord = {member.id}""")
            conn.commit()

        cursor.execute(f"""SELECT * FROM dis_users WHERE time_after_leaving > 0 """)  # Обновление покинувших сервер
        users = cursor.fetchall()
        for i in users:
            if i[6] > 10080:  # Если время ухода с сервера больше недели удаление из базы данных
                cursor.execute(f"""DELETE FROM dis_users WHERE id_discord = {i[0]}""")
            else:
                cursor.execute(f"""UPDATE dis_users SET time_after_leaving = {i[6] + 1} WHERE id_discord = {i[0]}""")
        conn.commit()
        # print(1)
        await asyncio.sleep(60)




"""

-----EVENTS-----

"""


@client.event
async def on_ready():
    global text_chann
    global conn
    global cursor
    global guild
    global recruit
    global dead
    global sergeant
    global major
    global moder

    text_chann = client.get_channel(938411811173199955)  # текстовый канал куда пишет bot
    guild = client.get_guild(938411811173199952)  # Объект сервера
    recruit = guild.get_role(944498408163524628)  # Роль для новичка
    sergeant = guild.get_role(944498493836365847)  # Роль сержант
    major = guild.get_role(944498549775806464)  # Роль майор
    dead = guild.get_role(944202377500717126)  # Роль труп
    moder = guild.get_role(943952964576501821)  # Роль модера

    if not os.path.isfile("./mydatabase.db"):
        """
        
        Если базы данных нет она создается и всем участникам дается роль новичка
        и записываются в бд
        
        """

        conn = sqlite3.connect("./mydatabase.db")  # Соединение с бд
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE dis_users (id_discord INTEGER UNIQUE, role INTEGER,
            num_mess INTEGER, time_on_voice INTEGER, warnings INTEGER, time_afk INTEGER,
            time_after_leaving INTEGER, chat_time INTEGER);""")
        for member in guild.members:
            if member.bot:
                continue
            await member.add_roles(recruit)
            cursor.execute(f"""INSERT INTO dis_users
                                          VALUES ('{member.id}', '1', '0',
                                          '0', '0', '0', '0', '0')""")
        conn.commit()
    else:
        conn = sqlite3.connect("./mydatabase.db")  # Соединение с бд
        cursor = conn.cursor()

    cursor.execute(
        f"""UPDATE dis_users SET warnings = 0 WHERE id_discord = 869217405862305822""")  # Обнуление предупреждений
    conn.commit()

    cursor.execute(f"""SELECT * FROM dis_users WHERE role == 99""")
    for i in cursor.fetchall():
        moders.append(i[0])

    print("ready")
    await timer_min()  # Обновление каждую минуту время в войсе и афк


@client.event
async def on_member_remove(member):
    cursor.execute(f"""UPDATE dis_users SET time_after_leaving = 1 WHERE id_discord = {member.id}""")
    conn.commit()


@client.event
async def on_member_join(member):  # Когда человек заходит на сервер
    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {member.id} """)
    if cursor.fetchone() is None:  # Если человек не найден в бд
        await member.add_roles(recruit)  # Добавление новичку роли
        cursor.execute(f"""INSERT INTO dis_users
                              VALUES ('{member.id}', '1', '0',
                              '0', '0', '0', '0', '0')""")
        conn.commit()  # Сохранение изменений в бд
        await member.send(f"Welcome {member.name}")  # Бот пишет в лс
        await text_chann.send(f"welcome {member.name}")  # Бот пишет в text chann
    else:  # Если человек найден в бд
        cursor.execute(f"""UPDATE dis_users SET time_after_leaving 
        = 0 WHERE id_discord = {member.id}""")  # Обнуление времени после ухода
        if cursor.fetchone()[1] == 1:  # Проверка из базы данных на роль
            await member.add_roles(recruit)
        elif cursor.fetchone()[1] == 2:
            await member.add_roles(sergeant)
        elif cursor.fetchone()[1] == 3:
            await member.add_roles(major)
        await member.send(f"С возвращением {member.name}")  # Бот пишет в лс
        await text_chann.send(f"С возвращением {member.name}")  # Бот пишет в text chann


@client.event
async def on_message(message):
    global text_chann
    global authors_messages

    if message.author.bot:  # Проверка на сообщение от пользователя
        return

    if message.channel == text_chann:  # Проверка на основной канал
        member_messenger(message.author.id)  # Подсчет сообщений
        if not flag:
            # print(flag)
            if len(str(message.content)) > 400:  # Если больше 400 сим удаление и предупреждение
                await antispam(message.author.id)
                await message.delete()
            else:
                await timer_messages(3)  # Если меньше 400 символов за 3 секунд ограничение - 4 сообщений

        if not message.author.id in authors_messages:
            authors_messages.append(message.author.id)


    elif message.channel.id == 944209923645001728 or str(message.channel.type) == "private":  # Канал для комманд боту или лс
        await client.process_commands(message)


# @client.event
# async def on_raw_reaction_add(reaction):
#     if reaction.channel_id == 949728092253999195 and not reaction.member.bot:
#         print(reaction.emoji)
#         print(reaction.emoji.is_unicode_emoji())
#         print(reaction.emoji.id)


"""

-----COMMANDS-----

"""


@client.command()
async def help_me(ctx):  # Команда help_me Выводит доступные команды
    await ctx.send("$get_info_voice id  - Сколько участник сидел в голосовом чате (id человека)\n"
                   "\n$get_info_messages id  - Сколько участник писал в текстовом чате (id человека)\n"
                   "\n$get_info_warnings id  - Сколько у участника предупреждений (id человека)")


# @client.command()
# async def add_r(ctx, id):  # Команда add_r Добавляет реакции
#     welcome = client.get_channel(949728092253999195)
#     mess = await welcome.fetch_message(id)
#     for i in ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]:
#         await mess.add_reaction(i)


# @client.command()
# async def add_moder(ctx, id):  # Команда add_moder Добавляет модератора в бд
#     try:
#         cursor.execute(f"""INSERT INTO dis_users (id_discord, role) VALUES ('{id}', '99')""")
#         conn.commit()
#         moders.append(id)
#         ctx.send("Успешно добавлен")
#     except:
#         await ctx.send("Произошла ошибка")


@client.command()
async def get_info_voice(ctx, arg):  # Команда get_info_voice Выводит время в голосовых чатах
    global cursor
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")

        user = guild.get_member(int(arg))
        num = cursor.fetchone()[3]

        if num > 60:
            await ctx.send(f"{user.name} сидел в голосовом чате {num // 60} ч. {num % 60} м.")
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


@client.command()
async def button(ctx):
    await ctx.send(
        "Hello, World!",
        components = [
            Button(label = "WOW button!", custom_id = "button1"),
            Button(label="WOW button2!", custom_id="button2"),

        ],
    )


    msg = await client.wait_for("button_click")
    await msg.respond(content = 'Деньги успешно переведены!')


@client.command()
async def select(ctx):
    await ctx.send(
        "Hello, World!",
        components = [
            Select(
                placeholder = "Select something!",
                options = [
                    SelectOption(label = "A", value = "A"),
                    SelectOption(label = "B", value = "B")
                ]
            )
        ]
    )

    interaction = await client.wait_for("select_option")
    await interaction.send(content = f"{interaction.values[0]} selected!")

""" 


-----RUN-----

"""

if __name__ == '__main__':
    client.run(token)
