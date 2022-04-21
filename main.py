import discord, sqlite3, asyncio, time, os, datetime
from config import *
from discord.ext import commands

# from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents)
# DiscordComponents(client)

flag = False
list_warnings = []
# authors_messages = []
messages = {}
admins = []

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
    if k in admins:
        return
    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
    num = cursor.fetchone()
    num = int(num[4]) + 1
    cursor.execute(f"""UPDATE dis_users SET warnings = {num} WHERE id_discord = {k}""")
    conn.commit()
    user = client.get_user(k)
    if num == 1:
        await user.send("Здравствуй. Дружок, может тебе отдохнуть? Пальчики не устали?")
    if num == 2:
        await user.send("Ты живёшь последний понедельник, понял?")

    else:
        await user.send("Довыёбывалась мусорка. Желаю удачного полёта в Казахстан.")
        await guild.ban(user)
        cursor.execute(f"""DELETE FROM dis_users WHERE id_discord = {k}""")
    conn.commit()


async def timer_messages(num_messages_in_2_sec):
    global flag
    global messages
    global list_warnings
    flag = True

    await asyncio.sleep(2)
    # t = time.time()
    for k, v in messages.items():
        user = guild.get_member(k)
        if v > num_messages_in_2_sec:  # Количество сообщений за 2 секунды # Антиспам!
            await antispam(k)  # Вызов предупреждения по спаму
        if dead in user.roles:
            await user.remove_roles(dead)
        # print("v", v)

        cursor.execute(f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {k}""")  # Обнуление счетчика афк
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
        num = cursor.fetchone()
        # if num[2] + v > 200 and int(num[1]) == 2:
        #     # Если человек написал больше 200 сообщений и звание сержант выдается роль майор
        #     # cursor.execute(f"""UPDATE dis_users SET role = 2 WHERE id_discord = {k}""")
        #     # user = guild.get_member(k)
        #     # await user.remove_roles(sergeant)  # Удаление сержанта
        #     # await user.add_roles(major)  # Добавление майора
        #     # await text_chann.send(f"{user.name} повышен до {sergeant.name}")
        #     pass
        # if num[2] + v > 100 and int(num[1]) == 1:
        #     # Если человек написал больше 100 сообщений и звание новобранец выдается роль сержант
        #     # cursor.execute(f"""UPDATE dis_users SET role = 2 WHERE id_discord = {k}""")
        #     # user = guild.get_member(k)
        #     # await user.remove_roles(recruit)  # Удаление новобранца
        #     # await user.add_roles(sergeant)  # Добавление сержанта
        #     # await text_chann.send(f"{user.name} повышен до {sergeant.name}")
        #     pass
        cursor.execute(f"""UPDATE dis_users SET num_mess = {num[2] + v} WHERE id_discord = {k}""")
        conn.commit()
    # print(time.time()-t)
    flag = False
    messages = {}


"""

-----TIMER-----

"""


async def timer_min():  # Таймер на каждую минуту
    # global authors_messages
    while True:
        # for i in authors_messages:
        #     cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {i}""")
        #     num = cursor.fetchone()
        #
        #     cursor.execute(f"""UPDATE dis_users SET chat_time
        #                 = {num[7] + 1} WHERE id_discord = {i}""")  # Счет времени в chat
        #     conn.commit()
        # authors_messages = []
        # t = time.time()
        members = guild.members
        for member in members:
            if member.bot:
                continue
            cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
            member_bd = cursor.fetchone()
            if admin in member.roles:
                admin.append(member.id)
            if member.voice is not None and member.voice.channel != guild.get_channel(
                    948653240512286760):  # Если участник в войсе и не в пивнушке

                cursor.execute(  # Счет времени в войсе
                    f"""UPDATE dis_users SET time_on_voice = {member_bd[3] + 1} WHERE id_discord = {member.id}""")
                cursor.execute(f"""UPDATE dis_users SET time_afk = 
                0 WHERE id_discord = {member.id}""")  # Обнуление счетчика афк
                conn.commit()
            if member_bd[3] > 4200 and (dont_bot and plebey and nash_chel) not in member.roles:
                await member.remove_roles(trust_roles)
                await member.add_roles(civilian)
            elif member_bd[3] > 600 or member_bd[2] > 350 and (dont_bot and civilian and nash_chel) not in member.roles:
                await member.remove_roles(trust_roles)
                await member.add_roles(plebey)
            elif (member_bd[3] > 0 or member_bd[2] > 20) and (civilian and plebey and nash_chel) not in member.roles:
                await member.add_roles(dont_bot)

            if member_bd[3] > 9000 or member_bd[2] > 3500 and zadrot not in member.roles:
                await member.remove_roles(main_roles)
                await member.add_roles(zadrot)
            elif member_bd[3] > 4500 or member_bd[2] > 1500 and worker not in member.roles:
                await member.remove_roles(main_roles)
                await member.add_roles(worker)
            elif member_bd[3] > 2100 or member_bd[2] > 550 and lybitel not in member.roles:
                await member.remove_roles(main_roles)
                await member.add_roles(lybitel)
            elif member_bd[3] > 600 or member_bd[2] > 350 and chel not in member.roles:
                await member.remove_roles(main_roles)
                await member.add_roles(chel)
            elif member_bd[3] > 60 or member_bd[2] > 150 and zymerok not in member.roles:
                await member.remove_roles(main_roles)
                await member.add_roles(zymerok)
            elif member_bd[3] > 0 or member_bd[2] > 20 and no_name not in member.roles:
                await member.remove_roles(main_roles)
                await member.add_roles(no_name)

            if dead in member.roles and member_bd[5] < 10080:  # Удаление роли трупа если число афк меньше недели
                member.remove_roles(dead)

            if member_bd[5] > 25440 and member.id not in admins:  # Если афк больше 424 часов кик
                await member.send("Ты был кикнут за неактивность")
                await guild.kick(user=member, reason="Неактивность")
            elif member_bd[5] > 25200:  # Если афк больше 400 часов трупачек
                await member.add_roles(dead)

            cursor.execute(f"""UPDATE dis_users SET time_afk = {member_bd[5] + 1} WHERE id_discord = {member.id}""")
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
    global conn
    global cursor
    global guild

    global who_im
    global dont_bot
    global plebey
    global civilian
    global nash_chel

    global no_name
    global chel
    global zymerok
    global lybitel
    global worker
    global zadrot

    global minor
    global kozyrok
    global churchill
    global intellegence
    global stalin

    global hoi
    global mow

    global senator
    global admin

    global dead

    global tech_channels
    global main_roles
    global trust_roles
    global vip_roles

    guild = client.get_guild(940667074093645856)  # Объект сервера

    who_im = guild.get_role(951918170527105105)
    dont_bot = guild.get_role(965019198382293032)
    plebey = guild.get_role(964948265722331216)
    civilian = guild.get_role(958026325434699806)
    nash_chel = guild.get_role(948647134234832957)

    no_name = guild.get_role(953756100946165820)
    chel = guild.get_role(964977305569067119)
    zymerok = guild.get_role(951917201412218980)
    lybitel = guild.get_role(954064661416923177)
    worker = guild.get_role(954064840845066270)
    zadrot = guild.get_role(951917649879793774)

    minor = guild.get_role(954067342608990239)
    kozyrok = guild.get_role(962370381690327081)
    churchill = guild.get_role(962062942050856960)
    intellegence = guild.get_role(962063644861010001)
    stalin = guild.get_role(958444218383224853)

    senator = guild.get_role(962065215950835793)
    admin = guild.get_role(945344360973742090)

    hoi = guild.get_role(953762306628653146)
    mow = guild.get_role(953763442303594616)

    dead = guild.get_role(953758013058060338)  # Роль труп

    tech_channels = []
    tech_channels.append(guild.get_channel(948644785118404618))  # hello
    tech_channels.append(guild.get_channel(955833582830637056))  # blockpost
    tech_channels.append(guild.get_channel(948658541206573106))  # roles
    tech_channels.append(guild.get_channel(948646836258865152))  # info
    tech_channels.append(guild.get_channel(949293533028835408))  # news
    tech_channels.append(guild.get_channel(949296173506777140))  # update

    main_roles = [no_name, chel, zymerok, lybitel, worker, zadrot]
    trust_roles = [dont_bot, plebey, civilian]
    vip_roles = [minor, kozyrok, churchill, intellegence, stalin]


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
            time_after_leaving INTEGER)""")
            # for role in member.roles:
            #
            #     cursor.execute(f"""INSERT INTO dis_users
            #                               VALUES ('{member.id}', '1', '0',
            #                               '0', '0', '0', '0', '0', '0')""")
        conn.commit()
    else:
        conn = sqlite3.connect("./mydatabase.db")  # Соединение с бд
        cursor = conn.cursor()

    # cursor.execute(
    #     f"""UPDATE dis_users SET warnings = 0 WHERE id_discord = 869217405862305822""")  # Обнуление предупреждений
    # conn.commit()

    # cursor.execute(f"""SELECT * FROM dis_users WHERE admin = 1""")
    # for i in cursor.fetchall():
    #     admins.append(i[0])
    print("ready")
    await timer_min()  # Обновление каждую минуту время в войсе и афк


@client.event
async def on_member_remove(member):
    if member.bot:  # Проверка на сообщение от пользователя
        return
    try:
        cursor.execute(f"""UPDATE dis_users SET time_after_leaving = 1 WHERE id_discord = {member.id}""")
        conn.commit()
    except:
        pass


@client.event
async def on_member_join(member):  # Когда человек заходит на сервер
    if member.bot:  # Проверка на сообщение от пользователя
        return
    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {member.id} """)
    if cursor.fetchone() is None:  # Если человек не найден в бд
        await member.add_roles(who_im)  # Добавление новичку роли Кто я?
        cursor.execute(f"""INSERT INTO dis_users
                              VALUES ('{member.id}', '0', '0',
                              '0', '0', '0', '0')""")  # нулевая роль это доверительная кто я
        conn.commit()  # Сохранение изменений в бд
        await member.send(f"Welcome {member.name}")  # Бот пишет в лс

    else:  # Если человек найден в бд
        cursor.execute(f"""UPDATE dis_users SET time_after_leaving 
        = 0 WHERE id_discord = {member.id}""")  # Обнуление времени после ухода
        cursor.execute(f"""UPDATE dis_users SET num_mess
                = 0 WHERE id_discord = {member.id}""")
        cursor.execute(f"""UPDATE dis_users SET time_on_voice
                        = 0 WHERE id_discord = {member.id}""")
        conn.commit()
        member_bd2 = cursor.fetchone()
        # print(member_bd2[1])
        if member_bd2[1] == 1:  # Проверка из базы данных на роль
            await member.add_roles(minor)
        if member_bd2[1] == 2:  # Проверка из базы данных на роль
            await member.add_roles(kozyrok)
        if member_bd2[1] == 3:  # Проверка из базы данных на роль
            await member.add_roles(churchill)
        if member_bd2[1] == 4:  # Проверка из базы данных на роль
            await member.add_roles(intellegence)
        if member_bd2[1] == 5:  # Проверка из базы данных на роль
            await member.add_roles(stalin)

        await member.send(f"С возвращением {member.name}, роли были восстановлены"
                          f" но доверие ты потерял")  # Бот пишет в лс


@client.event
async def on_raw_reaction_add(reaction):
    if reaction.message_id == 966372745032110091 and str(reaction.emoji) == "✅" and who_im in reaction.member.roles:
        await reaction.member.remove_roles(who_im)

    if reaction.message_id == 966694516906131486 and str(reaction.emoji) == "✅":  # Минор
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}""")
        member_reaction = cursor.fetchone()
        if minor in reaction.member.roles:
            await reaction.member.send("Роль уже куплена")
        if member_reaction[3] > 15000:
            await reaction.member.send("Вы купили роль @Минор")
            await reaction.member.add_roles(minor)
            cursor.execute(f"""UPDATE dis_users SET role 
                    = 1 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                = {member_reaction[3] - 15000} WHERE id_discord = {member_reaction[0]}""")
            conn.commit()
            if member_reaction[3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
             = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
        else:
            await reaction.member.send("Недостаточно средств")
    if reaction.message_id == 966694517833105418 and str(reaction.emoji) == "✅":  # Острый Козырёк
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}""")
        member_reaction = cursor.fetchone()
        if kozyrok in reaction.member.roles:
            await reaction.member.send("Роль уже куплена")
        if member_reaction[3] > 18000:
            await reaction.member.send("Вы купили роль @Острый Козырёк")
            await reaction.member.add_roles(kozyrok)
            cursor.execute(f"""UPDATE dis_users SET role 
                                = 2 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                            = {member_reaction[3] - 18000} WHERE id_discord = {member_reaction[0]}""")
            conn.commit()
            if member_reaction[3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
                         = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
        else:
            await reaction.member.send("Недостаточно средств")
    if reaction.message_id == 966694519384997928 and str(reaction.emoji) == "✅":  # Эх... Черчилль III, да...
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}""")
        member_reaction = cursor.fetchone()
        if churchill in reaction.member.roles:
            await reaction.member.send("Роль уже куплена")
        if member_reaction[3] > 18000:
            await reaction.member.send("Вы купили роль @Эх... Черчилль III, да...")
            await reaction.member.add_roles(churchill)
            cursor.execute(f"""UPDATE dis_users SET role 
                                = 3 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                            = {member_reaction[3] - 18000} WHERE id_discord = {member_reaction[0]}""")
            conn.commit()
            if member_reaction[3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
                         = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
        else:
            await reaction.member.send("Недостаточно средств")
    if reaction.message_id == 966694520567762974 and str(reaction.emoji) == "✅":  # Интеллигенция
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}""")
        member_reaction = cursor.fetchone()
        if intellegence in reaction.member.roles:
            await reaction.member.send("Роль уже куплена")
        if member_reaction[3] > 24000:
            await reaction.member.send("Вы купили роль @Интеллигенция")
            await reaction.member.add_roles(intellegence)
            cursor.execute(f"""UPDATE dis_users SET role 
                                = 4 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                            = {member_reaction[3] - 24000} WHERE id_discord = {member_reaction[0]}""")
            conn.commit()
            if member_reaction[3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
                         = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
        else:
            await reaction.member.send("Недостаточно средств")
    if reaction.message_id == 966694536468385832 and str(reaction.emoji) == "✅":  # Шиза Сталина
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}""")
        member_reaction = cursor.fetchone()
        if stalin in reaction.member.roles:
            await reaction.member.send("Роль уже куплена")
        if member_reaction[3] > 36000:
            await reaction.member.send("Вы купили роль @Шиза Сталина")
            await reaction.member.add_roles(stalin)
            cursor.execute(f"""UPDATE dis_users SET role 
                                = 5 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                            = {member_reaction[3] - 36000} WHERE id_discord = {member_reaction[0]}""")
            conn.commit()
            if member_reaction[3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
                         = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
        else:
            await reaction.member.send("Недостаточно средств")

    if reaction.message_id == 966694538104168449 and str(reaction.emoji) == "✅":  # HOI
        if not hoi in reaction.member.roles:
            await reaction.member.add_roles(hoi)
    if reaction.message_id == 966694539509260318 and str(reaction.emoji) == "✅":  # MOW
        if not mow in reaction.member.roles:
            await reaction.member.add_roles(mow)

    if reaction.message_id == 966746342800113676 and str(reaction.emoji) == "✅":
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.member_id}""")
        balance = cursor.fetchone()
        await reaction.member.send(f"Часов:{balance[3] // 60}\nЧисло сообщений:{balance[2]}")

@client.event
async def on_message(message):
    if message.author.bot:  # Проверка на сообщение от пользователя
        return
    if message.author.id in admins:
        return
    if str(message.channel.type) != "private" and message.channel not in tech_channels:  # Проверка не на лс и не тех
        member_messenger(message.author.id)  # Подсчет сообщений
        if len(str(message.content).split("https://discord.")) > 1:  # Если в сообщении ссылка то предупреждение
            await antispam(message.author.id)
            await message.delete()
        if len(str(message.content)) > 400:  # Если больше 400 сим удаление
            await message.channel.send(f"Слишком длинное сообщение, {message.author.name}")
            await message.delete()
        else:
            if not flag:
                await timer_messages(1)  # Если меньше 400 символов за 2 секунд ограничение - 2 сообщений

    # elif message.channel.id == 944209923645001728 or str(message.channel.type) == "private":  # Канал для комманд боту или лс
    #     await client.process_commands(message)


# @client.event
# async def on_raw_reaction_add(reaction):
#     if reaction.channel_id == 949728092253999195 and not reaction.member.bot:
#         print(reaction.emoji)
#         print(reaction.emoji.is_unicode_emoji())
#         print(reaction.emoji.id)



"""

-----COMMANDS-----

"""

'''
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




@client.command()
async def get_info_voice(ctx, arg):  # Команда get_info_voice Выводит время в голосовых чатах
    global cursor
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")

        user = guild.get_member(int(arg))
        num = cursor.fetchone()

        if num[3] > 60:
            await ctx.send(f"{user.name} сидел в голосовом чате {num[3] // 60} ч. {num[3] % 60} м.")
        else:
            await ctx.send(f"{user.name} сидел в голосовом чате {num[3]} м.")
    except:
        await ctx.send("Произошла ошибка")


@client.command()
async def get_info_messages(ctx, arg):  # Команда get_info_messages Выводит число сообщений за все время
    global cursor
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        user = guild.get_member(int(arg))
        num = cursor.fetchone()
        await ctx.send(f"{user.name} написал {num[2]} сообщ.")

    except:
        await ctx.send("Произошла ошибка")


# @client.command()
# async def get_info_warnings(ctx, arg):  # Команда get_info_warnings Выводит число предупреждений
#     global cursor
#     try:
#         cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
#         user = guild.get_member(int(arg))
#         num = cursor.fetchone()
#         await ctx.send(f"{user.name} получил {num[4]} предупр.")
#     except:
#         await ctx.send("Произошла ошибка")


# @client.command()
# async def button(ctx):
#     await ctx.send(
#         "Hello, World!",
#         components = [
#             Button(label = "1", custom_id = "button1"),
#             Button(label="2!", custom_id="button2"),
#
#         ],
#     )
#
#     while True:
#         msg = await client.wait_for("button_click")
#         if msg.custom_id == "button1":
#             await msg.send(content = 'Нажата кнопка 1 и ты получаешь нихуя')
#
#         if msg.custom_id == "button2":
#             await msg.send(content = 'Нажата кнопка 2 и ты получаешь приз',
#                               components=[Button(label = "Приз", custom_id = "button3")])
#         if msg.custom_id == "button3":
#             await msg.send(content=':flag_ua: ')
#
# @client.command()
# async def select(ctx):
#     await ctx.send(
#         "Hello, World!",
#         components = [
#             Select(
#                 placeholder = "Select something!",
#                 options = [
#                     SelectOption(label = "A", value = "A"),
#                     SelectOption(label = "B", value = "B")
#                 ]
#             )
#         ]
#     )
#
#     interaction = await client.wait_for("select_option")
#     await interaction.send(content = f"{interaction.values[0]} selected!")
'''
""" 


-----RUN-----

"""

if __name__ == '__main__':
    client.run(token)
