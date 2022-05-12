import discord, sqlite3, time, os, asyncio
from discord.ext import commands

# from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

intents = discord.Intents.all()
intents.members = True
intents.bans = True

client = commands.Bot(command_prefix="$", intents=intents)

flag = False

list_warnings = []
# authors_messages = []
messages = {}

my_secret = os.environ['Token']
admins = []
links_warn = []
from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Монитор активен."


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

"""

-----START-----

"""


async def check_main_roles(member_bd, member):  # Проверка на выдачу ролей
    f1 = int(member_bd[3])
    f2 = member_bd[2]
    m_r = member.roles
    # if no_name in m_r:
    #     print("noname")
    # t = time.time()
    if f1 > 9000 or f2 > 3500:
        # print(1)
        if zadrot not in m_r:
            for role in main_roles:
                if role in m_r:
                    await member.remove_roles(role)
            await member.add_roles(zadrot)
    elif f1 > 3300 or f2 > 1500:
        # print(2)
        if worker not in m_r:
            for role in main_roles:
                if role in m_r:
                    await member.remove_roles(role)
            await member.add_roles(worker)
    elif f1 > 1500 or f2 > 550:
        # print(3)
        if lybitel not in m_r:
            for role in main_roles:
                if role in m_r:
                    await member.remove_roles(role)
            await member.add_roles(lybitel)
    elif f1 > 600 or f2 > 350:
        # print(4)
        if chel not in m_r:
            for role in main_roles:
                if role in m_r:
                    await member.remove_roles(role)
            await member.add_roles(chel)
    elif f1 > 60 or f2 > 150:
        # print(5)
        if zymerok not in m_r:
            for role in main_roles:
                if role in m_r:
                    await member.remove_roles(role)
            await member.add_roles(zymerok)
    else:
        if (no_name or who_im) not in m_r:
            for role in main_roles:
                if role in m_r:
                    await member.remove_roles(role)
            await member.add_roles(no_name)
    # print("Третья часть: ", time.time() - t)


def member_messenger(id):  # Подсчет сообщений
    global messages
    if id in messages:
        messages[id] = messages[id] + 1
    else:
        messages[id] = 1
    
    # print(messages)


async def antispam(k):  # Вызов предупреждения по спаму
    try:
        if k in admins:
            return
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
        num = cursor.fetchone()
        num = int(num[4]) + 1
        cursor.execute(
            f"""UPDATE dis_users SET warnings = {num} WHERE id_discord = {k}""")
        conn.commit()
        user = client.get_user(k)
        print(num)
        if num == 1:
            await user.send(
                "Здравствуй. Дружок, может тебе отдохнуть? Пальчики не устали?")
        elif num == 2:
            await user.send("Ты живёшь последний понедельник, понял?")
        else:
            await guild.ban(user)
    except:
      print("ERROR Antispam")

async def timer_messages(num_messages_in_2_sec):
    global flag
    global messages
    global list_warnings
    flag = True

    await asyncio.sleep(10)
    # t = time.time()
    for k, v in messages.items():
        user = guild.get_member(k)
        if v > num_messages_in_2_sec:  # Количество сообщений за 2 секунды # Антиспам!
            await antispam(k)  # Вызов предупреждения по спаму
        if dead in user.roles:
            await user.remove_roles(dead)
        # print("v", v)

        cursor.execute(
            f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {k}"""
        )  # Обнуление счетчика афк
        conn.commit()
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
        num = cursor.fetchone()
        cursor.execute(
            f"""UPDATE dis_users SET num_mess = {num[2] + v} WHERE id_discord = {k}"""
        )
        conn.commit()
    # print(time.time()-t)
    flag = False
    messages = {}


"""

-----TIMER-----

"""


async def timer_halfmin():  # Таймер на каждую минуту
    # global authors_messages
    while True:
        try:
            t1 = time.time()
            result = time.gmtime(t1)
            if result.tm_hour == 20 and result.tm_min == 1 and result.tm_sec > 49:
                with open("night.png", "rb") as image:
                    avatar = image.read()
                await client.user.edit(avatar=avatar, username="Vovan sleepy")
            if result.tm_hour == 4 and result.tm_min == 1 and result.tm_sec > 49:
                with open("day.jpeg", "rb") as image:
                    avatar = image.read()
                await client.user.edit(avatar=avatar, username="Vovan")
            members = guild.members
            for member in members:
                # t2 = time.time()
                # print(member.name)
                if member.bot:
                    continue
                cursor.execute(
                    f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
                member_bd = cursor.fetchone()
                if member.id not in admins:
                    if admin in member.roles:
                        admins.append(member.id)  
                    elif organizer in member.roles:
                        admins.append(member.id)
                    elif moder in member.roles:
                        admins.append(member.id)
                
                # print(member.name)
                # print(member_bd[5])
                cursor.execute(
                    f"""UPDATE dis_users SET time_afk = {member_bd[5] + 0.166} WHERE id_discord = {member.id}"""
                )
                conn.commit()
                try:
                    # print(member.name)
                    # print(member.voice)
                    if member.voice is not None and member.voice.channel != pivo and member.voice.self_mute == False:  # Если участник в войсе и не в пивнушке
                        cursor.execute(  # Счет времени в войсе
                            f"""UPDATE dis_users SET time_on_voice = {member_bd[3] + 0.166} WHERE id_discord = {member.id}"""
                        )
                        conn.commit()
                        cursor.execute(
                            f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {member.id}"""
                        )  # Обнуление счетчика афк
                        conn.commit()
                except:
                    pass
                # print("Первая часть: ", time.time())
                if nash_chel in member.roles:
                    for role in trust_roles:
                        if role in member.roles:
                            await member.remove_roles(role)
                elif member_bd[3] > 4200 and nash_chel not in member.roles:
                    if civilian not in member.roles:
                        for role in trust_roles:
                            if role in member.roles:
                                await member.remove_roles(role)
                        await member.add_roles(civilian)
                elif (member_bd[3] > 600
                      or member_bd[2] > 350) and (civilian or nash_chel) not in member.roles:
                    if plebey not in member.roles:
                        for role in trust_roles:
                            if role in member.roles:
                                await member.remove_roles(role)
                        await member.add_roles(plebey)
                elif (member_bd[3] > 0
                      or member_bd[2] > 20) and (civilian
                                                 or plebey or nash_chel) not in member.roles:
                    if dont_bot not in member.roles:
                        await member.add_roles(dont_bot)
                # print("Вторая часть: ", time.time() - t2)
                await check_main_roles(member_bd, member)
    
                if dead in member.roles and member_bd[
                        5] < 24000:  # Удаление роли трупа если число афк меньше недели
                    member.remove_roles(dead)
    
                if member_bd[
                        5] > 25440 and member.id not in admins:  # Если афк больше 424 часов кик
                    try:
                        
                        await member.send(f'''Ещё не запылился?
        Ты был **Исключён** из сервера " :banana: **Men of Cum - Redux** :milk:" за **Не активность** на **Сервере!**
        Если ты захочешь **Вернуться** к нам на **Сервер**, то советую поторопиться ...
        Все твои **Роли** скоро **Исчезнут**, да да...
        *У тебя Неделя, Дружок* :innocent:
        
        :arrow_right: {await general.create_invite(max_uses = 1)} :arrow_left:'''
                                          )  # !!!!!
                    except:
                        pass
                    await guild.kick(user=member)
                elif member_bd[5] > 24000:  # Если афк больше 420 часов трупачек
                    await member.add_roles(dead)
    
                
                # print("Обход участников:", time.time()-t2)
            cursor.execute(
                f"""SELECT * FROM dis_users WHERE time_after_leaving > 0 """
            )  # Обновление покинувших сервер
            users = cursor.fetchall()
            for i in users:
                if i[6] > 10080:  # Если время ухода с сервера больше недели удаление из базы данных
                    cursor.execute(
                        f"""DELETE FROM dis_users WHERE id_discord = {i[0]}""")
                else:
                    cursor.execute(
                        f"""UPDATE dis_users SET time_after_leaving = {i[6] + 0.166} WHERE id_discord = {i[0]}"""
                    )
            conn.commit()
            diff = time.time() - t1
            print(diff)
            await asyncio.sleep(10 - diff)
        except:
          print("ERROR")

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
    global organizer
    global moder

    global dead

    global pivo
    global tech_channels
    global general
    global main_roles
    global trust_roles
    global vip_roles

    global agreement
    global minor_mess
    global kozyrok_mess
    global churchill_mess
    global intellegence_mess
    global stalin_mess
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
    organizer = guild.get_role(945344360973742090)
    admin = guild.get_role(972535623128862770)
    moder = guild.get_role(972533459790753792)
  
    hoi = guild.get_role(953762306628653146)
    mow = guild.get_role(953763442303594616)

    dead = guild.get_role(953758013058060338)  # Роль труп

    pivo = guild.get_channel(948653240512286760)
    tech_channels = []
    tech_channels.append(guild.get_channel(948644785118404618))  # hello
    tech_channels.append(guild.get_channel(955833582830637056))  # blockpost
    tech_channels.append(guild.get_channel(948658541206573106))  # roles
    tech_channels.append(guild.get_channel(948646836258865152))  # info
    tech_channels.append(guild.get_channel(949293533028835408))  # news
    tech_channels.append(guild.get_channel(949296173506777140))  # update
    tech_channels.append(guild.get_channel(967711624108597318))  # shop
    general = guild.get_channel(962035426644885565)
    main_roles = [no_name, chel, zymerok, lybitel, worker, zadrot]
    trust_roles = [dont_bot, plebey, civilian]
    vip_roles = [minor, kozyrok, churchill, intellegence, stalin]

    agreement = await guild.get_channel(948646836258865152).fetch_message(970952344122581012)
    minor_mess = await guild.get_channel(967711624108597318).fetch_message(968957147503296584)
    kozyrok_mess = await guild.get_channel(967711624108597318).fetch_message(968957358640341022)
    churchill_mess = await guild.get_channel(967711624108597318).fetch_message(968957518715973762)
    intellegence_mess = await guild.get_channel(967711624108597318).fetch_message(968957651822182410)
    stalin_mess = await guild.get_channel(967711624108597318).fetch_message(968957729458765914)
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
        conn.commit()
        for member in guild.members:
            if not member.bot:
                cursor.execute(f"""INSERT INTO dis_users
                                              VALUES ('{member.id}', '0', '0',
                                              '0', '0', '0', '0')""")
                conn.commit()
    else:
        conn = sqlite3.connect("./mydatabase.db")  # Соединение с бд
        cursor = conn.cursor()
        for member in guild.members:
            if not member.bot:
                try:
                    cursor.execute(f"""INSERT INTO dis_users
                                              VALUES ('{member.id}', '0', '0',
                                              '0', '0', '0', '0')""")
                    conn.commit()
                except:
                    pass
                cursor.execute(
                    f"""UPDATE dis_users SET warnings = 0 WHERE id_discord = {member.id}"""
                )
                conn.commit()
    # cursor.execute(
    #     f"""UPDATE dis_users SET warnings = 0 WHERE id_discord = 869217405862305822""")  # Обнуление предупреждений
    # conn.commit()

    # cursor.execute(f"""SELECT * FROM dis_users WHERE admin = 1""")
    # for i in cursor.fetchall():
    #     admins.append(i[0])

    print("ready")
    await timer_halfmin()  # Обновление каждую минуту время в войсе и афк


@client.event
async def on_raw_reaction_remove(reaction):
    user = guild.get_member(reaction.user_id)
    if reaction.message_id == 968960778403196968 and str(
            reaction.emoji) == "<:HeartsofIronIV:953363622501969960>":  # HOI
        if hoi in user.roles:
            await user.remove_roles(hoi)
    if reaction.message_id == 968960778403196968 and str(
            reaction.emoji) == "<:MenofWar:953352918218711070>":  # MO
        if mow in user.roles:
            await user.remove_roles(mow)


@client.event
async def on_member_remove(member):
    if member.bot:  # Проверка на сообщение от пользователя
        return
    if member.id in admins:
        return
    if who_im in member.roles:
        cursor.execute(
            f"""DELETE FROM dis_users WHERE id_discord = {member.id}""")
        conn.commit()
    try:
        cursor.execute(
            f"""UPDATE dis_users SET time_after_leaving = 1 WHERE id_discord = {member.id}"""
        )
        conn.commit()
    except:
        pass


@client.event
async def on_member_ban(guild, user):
    if user.id in admins:
        return
    cursor.execute(f"""DELETE FROM dis_users WHERE id_discord = {user.id}""")
    conn.commit()


@client.event
async def on_member_join(member):  # Когда человек заходит на сервер
    if member.bot:  # Проверка на сообщение от пользователя
        return
    cursor.execute(
        f"""SELECT * FROM dis_users WHERE id_discord = {member.id} """)
    if cursor.fetchone() is None:  # Если человек не найден в бд
        await member.add_roles(who_im)  # Добавление новичку роли Кто я?
        cursor.execute(f"""INSERT INTO dis_users
                              VALUES ('{member.id}', '0', '0',
                              '0', '0', '0', '0')"""
                       )  # нулевая роль это доверительная кто я
        conn.commit()  # Сохранение изменений в бд
        

    else:  # Если человек найден в бд
        cursor.execute(f"""UPDATE dis_users SET time_after_leaving 
        = 0 WHERE id_discord = {member.id}""")  # Обнуление времени после ухода
        # cursor.execute(f"""UPDATE dis_users SET num_mess
        #         = 0 WHERE id_discord = {member.id}""")
        # cursor.execute(f"""UPDATE dis_users SET time_on_voice
        #                 = 61 WHERE id_discord = {member.id}""")
        conn.commit()
        cursor.execute(
            f"""SELECT * FROM dis_users WHERE id_discord = {member.id} """)
        member_bd2 = cursor.fetchone()
        if member_bd2[3] > 4200 and (dont_bot and plebey
                                     and nash_chel) not in member.roles:
            for role in trust_roles:
                if role in member.roles:
                    await member.remove_roles(role)
            await member.add_roles(civilian)
        elif member_bd2[3] > 600 or member_bd2[2] > 350 and (
                dont_bot and civilian and nash_chel) not in member.roles:
            for role in trust_roles:
                if role in member.roles:
                    await member.remove_roles(role)
            await member.add_roles(plebey)
        elif (member_bd2[3] >= 0
              or member_bd2[2] > 20) and (civilian and plebey
                                          and nash_chel) not in member.roles:
            await member.add_roles(dont_bot)
        # print("Вторая часть: ", time.time() - t2)
        await check_main_roles(member_bd2, member)
        # print(member_bd2[1]
        if member_bd2[1] == 1:  # Проверка из базы данных на роль
            await member.add_roles(minor)
        elif member_bd2[1] == 2:  # Проверка из базы данных на роль
            await member.add_roles(kozyrok)
        elif member_bd2[1] == 3:  # Проверка из базы данных на роль
            await member.add_roles(churchill)
        elif member_bd2[1] == 4:  # Проверка из базы данных на роль
            await member.add_roles(intellegence)
        elif member_bd2[1] == 5:  # Проверка из базы данных на роль
            await member.add_roles(stalin)
        await member.send('''О, всё таки вернулся) :kissing_heart:
Значит не зря тебе напомнил.
**Все** твои **Роли Восстановлены** в полном составе.
И это, **Больше** чтобы такого **Не Было**.
*Это был последний раз, Дружок*''')  # Бот пишет в лс  !!!!!!!


@client.event
async def on_raw_reaction_add(reaction):
    # chann = guild.get_channel(948658541206573106)
    # message = reaction.message_id
    # message = await chann.fetch_message(message)
    # await message.add_reaction(reaction.emoji)
    
    if reaction.message_id == 970952344122581012:
        if str(reaction.emoji) == "✅":
            await agreement.remove_reaction("✅", reaction.member)
            if who_im in reaction.member.roles:
                await reaction.member.add_roles(no_name)
                await reaction.member.remove_roles(who_im)
        elif str(reaction.emoji) == "❌":
            await agreement.remove_reaction("❌", reaction.member)
            if who_im in reaction.member.roles:
              try:
                  await reaction.member.kick()
              except:
                  pass

    elif reaction.message_id == 968957147503296584 and str(
            reaction.emoji) == "💵":  # Минор
        await minor_mess.remove_reaction("💵", reaction.member)
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
        )
        member_reaction = cursor.fetchone()
        if minor in reaction.member.roles:
            await reaction.member.send(
                '''Ты не устал **Жмакать **на **Кнопочку**?
Заебал, прекращай.''')  # !!!!!!!
        elif member_reaction[3] > 15000:
            for role in vip_roles:
                await reaction.member.remove_roles(role)
            await reaction.member.send(
                f''':shopping_bags: **Поздравляю Тебя с Покупкой!** :shopping_bags:
Была куплена Роль - "{minor.name}"
Данная роль имеется у {len(minor.members)} чел.
:sparkling_heart: **Вы** всегда будите **Нашим** желанным **Покупателем!** :cupid:'''
            )  # !!!!!
            await reaction.member.add_roles(minor)
            cursor.execute(f"""UPDATE dis_users SET role 
                    = 1 WHERE id_discord = {member_reaction[0]}""")
            conn.commit()
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                = {member_reaction[3] - 15000} WHERE id_discord = {member_reaction[0]}"""
                           )
            conn.commit()
            cursor.execute(
                f"""UPDATE dis_users SET num_mess = 0 WHERE id_discord = {member_reaction[0]}"""
            )
            conn.commit()
            if member_reaction[
                    3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
             = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
            await check_main_roles(member_reaction, reaction.member)
        else:
            """{member_bd"""
            await reaction.member.send(f'''**У Вас Не Достаточно Средств!**
Ваш Баланс : {int(member_reaction[3]/60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age = 1800,max_uses = 1)} :arrow_left:

:gift_heart: **Приятной Вам Игры!** :cupid:''')  # !!!!!!!
    elif reaction.message_id == 968957358640341022 and str(
            reaction.emoji) == "💵":  # Острый Козырёк
        await kozyrok_mess.remove_reaction("💵", reaction.member)
        cursor.execute(
            f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
        )
        member_reaction = cursor.fetchone()
        if kozyrok in reaction.member.roles:
            await reaction.member.send(
                '''Ты не устал **Жмакать **на **Кнопочку**?
Заебал, прекращай.''')
        elif member_reaction[3] > 18000:
            for role in vip_roles:
                await reaction.member.remove_roles(role)
            await reaction.member.send(
                f''':shopping_bags: **Поздравляю Тебя с Покупкой!** :shopping_bags:
Была куплена Роль - "{kozyrok.name}"
Данная роль имеется у {len(kozyrok.members)} чел.
:sparkling_heart: **Вы** всегда будите **Нашим** желанным **Покупателем!** :cupid:'''
            )
            await reaction.member.add_roles(kozyrok)
            cursor.execute(f"""UPDATE dis_users SET role 
                                = 2 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                            = {member_reaction[3] - 18000} WHERE id_discord = {member_reaction[0]}"""
                           )
            conn.commit()
            cursor.execute(
                f"""UPDATE dis_users SET num_mess = 0 WHERE id_discord = {member_reaction[0]}"""
            )
            conn.commit()
            if member_reaction[
                    3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
                         = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
            await check_main_roles(member_reaction, reaction.member)
        else:
            await reaction.member.send(f'''**У Вас Не Достаточно Средств!**
Ваш Баланс : {int(member_reaction[3]/60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age = 1800,max_uses = 1)} :arrow_left:

:gift_heart: **Приятной Вам Игры!** :cupid:''')
    elif reaction.message_id == 968957518715973762 and str(
            reaction.emoji) == "💵":  # Эх... Черчилль III, да...
        await churchill_mess.remove_reaction("💵", reaction.member)
        cursor.execute(
            f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
        )
        member_reaction = cursor.fetchone()
        if churchill in reaction.member.roles:
            await reaction.member.send(
                '''Ты не устал **Жмакать **на **Кнопочку**?
Заебал, прекращай.''')
        elif member_reaction[3] > 18000:
            for role in vip_roles:
                await reaction.member.remove_roles(role)
            await reaction.member.send(
                f''':shopping_bags: **Поздравляю Тебя с Покупкой!** :shopping_bags:
Была куплена Роль - "{churchill.name}"
Данная роль имеется у {len(churchill.members)} чел.
:sparkling_heart: **Вы** всегда будите **Нашим** желанным **Покупателем!** :cupid:'''
            )
            await reaction.member.add_roles(churchill)
            cursor.execute(f"""UPDATE dis_users SET role 
                                = 3 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                            = {member_reaction[3] - 18000} WHERE id_discord = {member_reaction[0]}"""
                           )
            conn.commit()
            cursor.execute(
                f"""UPDATE dis_users SET num_mess = 0 WHERE id_discord = {member_reaction[0]}"""
            )
            conn.commit()
            if member_reaction[
                    3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
                         = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
            await check_main_roles(member_reaction, reaction.member)
        else:
            await reaction.member.send(f'''**У Вас Не Достаточно Средств!**
Ваш Баланс : {int(member_reaction[3]/60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age = 1800,max_uses = 1)} :arrow_left:

:gift_heart: **Приятной Вам Игры!** :cupid:''')
    elif reaction.message_id == 968957651822182410 and str(
            reaction.emoji) == "💵":  # Интеллигенция
        await intellegence_mess.remove_reaction("💵", reaction.member)
        cursor.execute(
            f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
        )
        member_reaction = cursor.fetchone()
        if intellegence in reaction.member.roles:
            await reaction.member.send(
                '''Ты не устал **Жмакать **на **Кнопочку**?
Заебал, прекращай.''')
        elif member_reaction[3] > 24000:
            for role in vip_roles:
                await reaction.member.remove_roles(role)
            await reaction.member.send(
                f''':shopping_bags: **Поздравляю Тебя с Покупкой!** :shopping_bags:
Была куплена Роль - "{intellegence.name}"
Данная роль имеется у {len(intellegence.members)} чел.
:sparkling_heart: **Вы** всегда будите **Нашим** желанным **Покупателем!** :cupid:'''
            )
            await reaction.member.add_roles(intellegence)
            cursor.execute(f"""UPDATE dis_users SET role 
                                = 4 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                            = {member_reaction[3] - 24000} WHERE id_discord = {member_reaction[0]}"""
                           )
            conn.commit()
            cursor.execute(
                f"""UPDATE dis_users SET num_mess = 0 WHERE id_discord = {member_reaction[0]}"""
            )
            conn.commit()
            if member_reaction[
                    3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
                         = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
            await check_main_roles(member_reaction, reaction.member)
        else:
            await reaction.member.send(f'''**У Вас Не Достаточно Средств!**
Ваш Баланс : {int(member_reaction[3]/60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age = 1800,max_uses = 1)} :arrow_left:

:gift_heart: **Приятной Вам Игры!** :cupid:''')
    elif reaction.message_id == 968957729458765914 and str(
            reaction.emoji) == "💵":  # Шиза Сталина
        await stalin_mess.remove_reaction("💵", reaction.member)
        cursor.execute(
            f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
        )
        member_reaction = cursor.fetchone()
        if stalin in reaction.member.roles:
            await reaction.member.send(
                '''Ты не устал **Жмакать **на **Кнопочку**?
Заебал, прекращай.''')
        elif member_reaction[3] > 36000:
            for role in vip_roles:
                await reaction.member.remove_roles(role)
            await reaction.member.send(
                f''':shopping_bags: **Поздравляю Тебя с Покупкой!** :shopping_bags:
Была куплена Роль - "{stalin.name}"
Данная роль имеется у {len(stalin.members)} чел.
:sparkling_heart: **Вы** всегда будите **Нашим** желанным **Покупателем!** :cupid:'''
            )
            await reaction.member.add_roles(stalin)
            cursor.execute(f"""UPDATE dis_users SET role 
                                = 5 WHERE id_discord = {member_reaction[0]}""")
            cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                            = {member_reaction[3] - 36000} WHERE id_discord = {member_reaction[0]}"""
                           )
            conn.commit()
            cursor.execute(
                f"""UPDATE dis_users SET num_mess = 0 WHERE id_discord = {member_reaction[0]}"""
            )
            conn.commit()
            if member_reaction[
                    3] < 61:  # Если у человека осталось меньше часа, устанавливается час
                cursor.execute(f"""UPDATE dis_users SET time_on_voice
                         = 61 WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
            await check_main_roles(member_reaction, reaction.member)
        else:
            await reaction.member.send(f'''**У Вас Не Достаточно Средств!**
Ваш Баланс : {int(member_reaction[3]/60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age = 1800,max_uses = 1)} :arrow_left:

:gift_heart: **Приятной Вам Игры!** :cupid:''')

    elif reaction.message_id == 970951993252278344 and str(
            reaction.emoji) == "<:HeartsofIronIV:953363622501969960>":  # HOI
        if hoi not in reaction.member.roles:
            await reaction.member.add_roles(hoi)
    elif reaction.message_id == 970951993252278344 and str(
            reaction.emoji) == "<:MenofWar:953352918218711070>":  # MO
        if mow not in reaction.member.roles:
            await reaction.member.add_roles(mow)

    # if reaction.message_id == 966746342800113676 and str(reaction.emoji) == "✅":  # Баланс
    #     cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.member_id}""")
    #     balance = cursor.fetchone()
    #     await reaction.member.send(f"Часов:{balance[3] // 60}\nЧисло сообщений:{balance[2]}")  # !!!!!!


@client.event
async def on_message(message):
    
    if message.author.bot:  # Проверка на сообщение от пользователя
        return
    # if message.author.id in admins:
    #     return
    if message.channel.id == 967710989728497664:  # Канал для комманд боту
      await client.process_commands(message)
    if str(
            message.channel.type
    ) != "private" and message.channel not in tech_channels:  # Проверка не на лс и не тех
        # invite = await general.create_invite(max_age = 1800,max_uses = 1)
        # await message.channel.send(invite)
        member_messenger(message.author.id)  # Подсчет сообщений
        if len(str(message.content).split("discord.gg/")
               ) > 1:  # Если в сообщении ссылка то предупреждение
            if message.author.id in links_warn:
                links_warn.remove(message.author.id)
                await message.delete()
                await message.author.ban()
                await message.channel.send(
                    f"Слизь со стены - {message.author.name} отлетела в помоечку."
                )
            links_warn.append(message.author.id)
            await message.delete()
            await message.channel.send(
                f"О, животное - {message.author.name} в чате пытается рекламировать свою хуету."
            )
        if len(str(message.content)) > 500:  # Если больше 400 сим удаление
            await message.delete()
        else:
            if not flag:
                await timer_messages(5)
           
                

    


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
async def insert_time(ctx, arg, arg2):
    user = await guild.fetch_member(arg)
    cursor.execute(f"""UPDATE dis_users SET time_on_voice = {int(arg2)*60} WHERE id_discord = {arg}""")
    conn.commit()
    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
    bd = cursor.fetchone()
    
    await ctx.send(f"У участника {user.name} в базе данных {round(bd[3]/60)} ч.")

@client.command()
async def insert_mess(ctx, arg, arg2):
    user = await guild.fetch_member(arg)
    cursor.execute(f"""UPDATE dis_users SET num_mess = {int(arg2)} WHERE id_discord = {arg}""")
    conn.commit()
    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
    bd = cursor.fetchone()
    
    await ctx.send(f"У участника {user.name} в базе данных {bd[2]} сообщ.")

@client.command()
async def get_info(ctx, arg):
    user = await guild.fetch_member(arg)
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        bd = cursor.fetchone()
        await ctx.send(f"""Информация об участнике {user.name}:
ID:  {bd[0]}
Role:  {bd[1]}
Number_messages:  {bd[2]}
Time_on_voice:  {int(bd[3])} мин. = {int(bd[3])/60} ч.
Warnings:  {bd[4]}
Time_afk:  {int(bd[5])} мин. = {int(bd[5])/60} ч.
Time_after_leaving:  {int(bd[6])}""")
    except:
        await ctx.send("Произошла ошибка")
'''
@client.command()
async def help(ctx):  # Команда help_me Выводит доступные команды

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
#                            )

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
    client.run(my_secret)
