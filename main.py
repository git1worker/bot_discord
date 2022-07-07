import discord, sqlite3, time, os, asyncio, datetime, subprocess
from discord.ext import commands, tasks

# from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

intents = discord.Intents.all()
intents.members = True
intents.bans = True

client = commands.Bot(command_prefix="$", intents=intents)

flag = False

list_warnings = []
# authors_messages = []
messages = {}

# my_secret = os.environ['Token']
admins = []
links_warn = []

global log_var
log_var = False
global log_var2, diff
log_var2 = False
global log_timer
# global log_var
# log_var = False
# from flask import Flask
# from threading import Thread
#
# app = Flask('')
#
#
# @app.route('/')
# def home():
#     return "Монитор активен."
#
#
# def run():
#     app.run(host='0.0.0.0', port=8080)
#
#
# def keep_alive():
#     t = Thread(target=run)
#     t.start()
#
#
# keep_alive()

"""

-----START-----

"""


async def check_main_roles(member_bd, member):  # Проверка на выдачу ролей
    f1 = int(member_bd[3])
    f2 = int(member_bd[2])
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
    elif f1 > 59 or f2 > 150:
        # print(5)
        if zymerok not in m_r:
            for role in main_roles:
                if role in m_r:
                    await member.remove_roles(role)
            await member.add_roles(zymerok)
    else:
        if no_name not in m_r:
            if who_im not in m_r:
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
            await exceptions.send(f"{datetime.datetime.now()} - warning_for_spam_1 - {user.name}")
        elif num == 2:
            await user.send("Ты живёшь последний понедельник, понял?")
            await exceptions.send(f"{datetime.datetime.now()} - warning_for_spam_2 - {user.name} - "
                                  f"Он живет последний понедельник")
        else:
            await guild.ban(user)
            await exceptions.send(f"{datetime.datetime.now()} - ban_for_spam - {user.name}")
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
            f"""UPDATE dis_users SET num_mess = {int(num[2]) + int(v)} WHERE id_discord = {k}"""
        )
        conn.commit()
    # print(time.time()-t)
    flag = False
    messages = {}


async def check(channel):
    while True:
        await asyncio.sleep(5)
        if len(channel.members) == 0:
            await channel.delete()
            break


"""

------------------------TIMER

"""

class Timer(commands.Cog):
    def __init__(self):
        
        self.main_loop.start()

    def stop_timer(self):
        self.main_loop.cancel()

    def change_time(self, sec):
        self.main_loop.change_interval(seconds=sec)

    @tasks.loop(seconds=10.0)
    async def main_loop(self):
        global log_var, log_var2, diff
        try:
            
            # await exceptions.send(log_var)
            if log_var:
                # await exceptions.send("123")
                try:
                    os.remove("./log_timer.txt")
                except:
                    pass
                await exceptions.send("Opened")
                log_var2 = True
                log_timer = open("./log_timer.txt", "+a")
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
                t2 = time.time()
                t3 = time.time()
                # print(member.name)

                # try:
                if member.bot:
                    continue
                cursor.execute(
                        f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
                member_bd = cursor.fetchone()
                # print(member_bd)
                try:
                    if member_bd[8] is not None:
                        if datetime.datetime.now() > datetime.datetime.strptime(member_bd[8], "%d/%m/%Y, %H:%M:%S"):
                            struct_time = datetime.datetime.now()
                            struct_time += datetime.timedelta(weeks=1) + datetime.timedelta(hours=3)
                            struct_time = struct_time.strftime('%d/%m/%Y, %H:%M:%S')
                            cursor.execute(
                                f"""UPDATE dis_users SET next_notice = '{struct_time}' WHERE id_discord = {member.id}""")
                            conn.commit()
                            all_str = ""
                            for i in working_hands.members:
                                if i.id == 597161042367348736:
                                    continue
                                if moder in i.roles:
                                    continue
                                if organizer in i.roles:
                                    continue
                                if i.bot:
                                    continue
                                if admin in i.roles:
                                    continue
                                all_str += i.mention
                            await working_hands.send(f"""❗ ***Уведомление*** ❗

{member.name} **Не Проявлял** на сервере **Активность** около **1 Недели!**
*Ваша обязанность: В течение этого дня поиграть с {member.name}*
||{all_str}||""")
                except Exception as exc:
                    with open("./log_file.txt", "a+") as f:
                        f.write(
                            f"\n {datetime.datetime.now()} - Ошибка Таймер участников уведомление - {member.name} - {exc}\n")
                        await exceptions.send(
                            f"{datetime.datetime.now()} - Ошибка Таймер участников уведомление - {member.name} - {exc}")
                if member_bd[1] == 0 and member_bd[5] > 4320:
                    await guild.kick(user=member)
                if admin in member.roles:
                    if member.id not in admins:
                        admins.append(member.id)
                elif organizer in member.roles:
                    if member.id not in admins:
                        admins.append(member.id)
                elif moder in member.roles:
                    if member.id not in admins:
                        admins.append(member.id)
                elif senator in member.roles:
                    if member.id not in admins:
                        admins.append(member.id)
                # print(member.name)
                # print(member_bd[5])
                if log_var2:
                    log_timer.write(f"{member.name} - Первая часть: {time.time() - t2} - Роли: {member.roles}\n")
                t2 = time.time()
                cursor.execute(
                    f"""UPDATE dis_users SET time_afk = {member_bd[5] + 0.166} WHERE id_discord = {member.id}""")
                conn.commit()
                if log_var2:
                    log_timer.write(f"{member.name} - Вторая часть(Обновление в бд афк): {time.time() - t2}\n")
                t2 = time.time()
                try:
                    # print(member.name)
                    # print(member.voice)
                    if member.voice is not None and member.voice.channel != pivo and member.voice.self_mute == False:  # Если участник в войсе и не в пивнушке
                        cursor.execute(  # Счет времени в войсе
                            f"""UPDATE dis_users SET time_on_voice = {member_bd[3] + 0.166} WHERE id_discord = {member.id}"""
                        )
                        struct_time = datetime.datetime.now()
                        struct_time += datetime.timedelta(weeks=1) + datetime.timedelta(hours=3)
                        struct_time = struct_time.strftime('%d/%m/%Y, %H:%M:%S')
                        cursor.execute(
                            f"""UPDATE dis_users SET next_notice = '{struct_time}' WHERE id_discord = {member.id}""")
                        cursor.execute(
                            f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {member.id}"""
                        )  # Обнуление счетчика афк
                        conn.commit()
                except Exception as exc:
                    with open("./log_file.txt", "a+") as f:
                        f.write(
                            f"\n {datetime.datetime.now()} - Ошибка Таймер участников проверка войса - {member.name} - {exc}\n")
                        await exceptions.send(
                            f"{datetime.datetime.now()} - Ошибка Таймер участников проверка войса - {member.name} - {exc}")
                if log_var2:
                    log_timer.write(f"{member.name} - Третья часть(Проверка на войс и сброс афк): {time.time()-t2} - {member.voice}\n")
                t2 = time.time()
                m_roles = member.roles
                if nash_chel in m_roles:
                    for role in trust_roles:
                        if role in m_roles:
                            await member.remove_roles(role)
                elif member_bd[3] > 4200:
                    for role in [dont_bot, plebey]:
                        if role in m_roles:
                            await member.remove_roles(role)
                    if civilian not in m_roles:
                        await member.add_roles(civilian)
                elif (member_bd[3] > 600
                        or int(member_bd[2]) > 350) and civilian not in m_roles:
                    if dont_bot in m_roles:
                        await member.remove_roles(dont_bot)
                    if plebey not in m_roles:
                        await member.add_roles(plebey)
                elif (member_bd[3] > 0
                        or int(member_bd[2]) > 20) and civilian not in m_roles:
                    if plebey not in m_roles:
                        if dont_bot not in m_roles:
                            await member.add_roles(dont_bot)
                await check_main_roles(member_bd, member)
                if dead in m_roles and member_bd[
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

        :arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:''')  # !!!!!
                    except Exception as exc:
                        with open("./log_file.txt", "a+") as f:
                            f.write(f"\n {datetime.datetime.now()} - Ошибка Таймер участников афк кик - {member.name} - {exc}\n")
                            await exceptions.send(f"{datetime.datetime.now()} - Ошибка Таймер участников афк кик - {member.name} - {exc}")
                    finally:
                        await exceptions.send(
                            f"{datetime.datetime.now()} - Кик участника за афк - {member.name}")
                        await guild.kick(user=member)
                elif member_bd[5] > 24000:  # Если афк больше 420 часов трупачек
                    await member.add_roles(dead)
                if log_var2:
                    log_timer.write(
                        f"{member.name} - Четвертая часть(Провека ролей): {time.time() - t2}\n")
                if log_var2:
                    log_timer.write(
                        f"{member.name} - Всего: {time.time() - t3}\n")
                # except Exception as exc:
                #     with open("./log_file.txt", "a+") as f:
                #         f.write(f"\n {datetime.datetime.now()} - Ошибка Таймер участников - {member.name} - {exc}\n")
                #     await exceptions.send(f"{datetime.datetime.now()} - Ошибка Таймер участников - {member.name} - {exc}")
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
                        f"""UPDATE dis_users SET time_after_leaving = {i[6] + 0.166} WHERE id_discord = {i[0]}""")

            conn.commit()
            diff = time.time() - t1
            print(diff)
            if log_var2:
                log_timer.write(
                    f"\n\n{datetime.datetime.now()} - Задержка таймера: {diff}\n")
                log_timer.close()
                log_var2 = False
                log_var = False
            

            if diff > 10:
                await exceptions.send(f"{datetime.datetime.now()} - Время обработки превышено - {diff}")
        except Exception as exc:
            with open("./log_file.txt", "a+") as f:
                f.write(f"\n {datetime.datetime.now()} - Ошибка Таймер - {exc}\n")
            await exceptions.send(f"{datetime.datetime.now()} - Ошибка Таймер - {exc}")
            subprocess.run(["systemctl", "restart", "runscript.service"])
      

"""

------------------------EVENTS

"""


@client.event
async def on_ready():
    

    global conn, cursor, guild, timer

    global who_im, dont_bot, plebey, civilian, nash_chel

    global no_name, zadrot, worker, lybitel, zymerok, chel

    global minor, kozyrok, churchill, intellegence, stalin

    global hoi, mow

    global senator, admin, organizer, moder

    global dead

    global hands

    global pivo, tech_channels, general, working_hands, main_roles, trust_roles, vip_roles, exceptions

    global agreement, minor_mess, kozyrok_mess, churchill_mess, intellegence_mess, stalin_mess, balance, time_voice, hands_mess

    global gaming_zone

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

    hands = guild.get_role(965007953671356416)

    pivo = guild.get_channel(948653240512286760)
    tech_channels = []
    tech_channels.append(guild.get_channel(948644785118404618))  # hello
    tech_channels.append(guild.get_channel(955833582830637056))  # blockpost
    tech_channels.append(guild.get_channel(948658541206573106))  # roles
    tech_channels.append(guild.get_channel(948646836258865152))  # info
    tech_channels.append(guild.get_channel(949293533028835408))  # news
    tech_channels.append(guild.get_channel(949296173506777140))  # update
    tech_channels.append(guild.get_channel(967711624108597318))  # shop
    general = guild.get_channel(981970134384119819)
    working_hands = guild.get_channel(980684109301051414)
    main_roles = [no_name, chel, zymerok, lybitel, worker, zadrot]
    trust_roles = [dont_bot, plebey, civilian]
    vip_roles = [minor, kozyrok, churchill, intellegence, stalin]
    exceptions = guild.get_channel(981978051762061362)

    agreement = await guild.get_channel(948646836258865152).fetch_message(970952344122581012)
    minor_mess = await guild.get_channel(967711624108597318).fetch_message(968957147503296584)
    kozyrok_mess = await guild.get_channel(967711624108597318).fetch_message(968957358640341022)
    churchill_mess = await guild.get_channel(967711624108597318).fetch_message(968957518715973762)
    intellegence_mess = await guild.get_channel(967711624108597318).fetch_message(968957651822182410)
    stalin_mess = await guild.get_channel(967711624108597318).fetch_message(968957729458765914)
    balance = await guild.get_channel(974356084502433863).fetch_message(974987029043609660)
    time_voice = await guild.get_channel(974356084502433863).fetch_message(974989390755532800)
    hands_mess = await guild.get_channel(967711624108597318).fetch_message(977482928365899816)

    gaming_zone = guild.get_channel(940667074638921771)

    

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
                                              '0', '0', '0', '0', {time.time()})""")
                conn.commit()
    else:
        conn = sqlite3.connect("./mydatabase.db")  # Соединение с бд
        cursor = conn.cursor()
        for member in guild.members:
            if not member.bot:
                try:
                    struct_time = datetime.datetime.now()
                    struct_time += datetime.timedelta(hours=3)
                    struct_time = struct_time.strftime('%d/%m/%Y, %H:%M:%S')
                    cursor.execute(f"""INSERT INTO dis_users
                                  VALUES ('{member.id}', '0', '0',
                                  '0', '0', '0', '0', '{struct_time}', '{struct_time}'""")
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
    t1 = time.time()
    result = time.gmtime(t1)
    try:
        await guild.get_channel(983112905098666074).send(f"Перезапуск: {result.tm_mday}.{result.tm_mon}.{result.tm_year}")
    except:
        pass
    print("ready")
    timer = Timer()  # Обновление каждую минуту время в войсе и афк


@client.event
async def on_raw_reaction_remove(reaction):
    try:
        user = guild.get_member(reaction.user_id)
        if reaction.message_id == 970951993252278344 and str(
                reaction.emoji) == "<:HeartsofIronIV:953363622501969960>":  # HOI
            if hoi in user.roles:
                await user.remove_roles(hoi)
        if reaction.message_id == 970951993252278344 and str(
                reaction.emoji) == "<:MenofWar:953352918218711070>":  # MO
            if mow in user.roles:
                await user.remove_roles(mow)
    except Exception as exc:
        with open("./log_file.txt", "a+") as f:
            f.write(f"\n {datetime.datetime.now()} - Ошибка Удаление реакции - {reaction.user_id} - {exc}\n")
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка Удаление реакции - {reaction.user_id} - {exc}")


@client.event
async def on_member_remove(member):
    if member.bot:  # Проверка на сообщение от пользователя
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
        await exceptions.send(f"{datetime.datetime.now()} - Участника больше нет на сервере - {member.name} - id: {member.id}")
    except Exception as exc:
        with open("./log_file.txt", "a+") as f:
            f.write(f"\n {datetime.datetime.now()} - Ошибка выход человека с сервера - {member.id} - {exc}\n")
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка выход человека с сервера - {member.id} - {exc}")


@client.event
async def on_member_ban(guild, user):
    try:
        if user.id in admins:
            return
        cursor.execute(f"""DELETE FROM dis_users WHERE id_discord = {user.id}""")
        conn.commit()
    except Exception as exc:
        with open("./log_file.txt", "a+") as f:
            f.write(f"\n {datetime.datetime.now()} - На бан - {user.id} -На бан - {user.id} - {exc}")


@client.event
async def on_member_join(member):  # Когда человек заходит на сервер
    try:
        if member.bot:  # Проверка на сообщение от пользователя
            return
        struct_time = datetime.datetime.now()
        days = struct_time - member.created_at
        struct_time += datetime.timedelta(hours=3)
        struct_time2 = struct_time + datetime.timedelta(weeks=1)
        struct_time2 = struct_time2.strftime('%d/%m/%Y, %H:%M:%S')
        struct_time = struct_time.strftime('%d/%m/%Y, %H:%M:%S')
        # print(struct_time)
        cursor.execute(
            f"""SELECT * FROM dis_users WHERE id_discord = {member.id} """)
        if int(days.days) < 60:
            await guild.kick(member)
        elif cursor.fetchone() is None:  # Если человек не найден в бд
            try:
                await member.add_roles(who_im)  # Добавление новичку роли Кто я?
                cursor.execute(f"""INSERT INTO dis_users
                                      VALUES ('{member.id}', '0', '0',
                                      '0', '0', '0', '0', '{struct_time}', '{struct_time2}')"""
                               )  # нулевая роль это доверительная кто я
                conn.commit()
                # await exceptions.send(f"{datetime.datetime.now()} - Заход на сервер - {member.name} - Аккаунт создан: {member.created_at}")
                # print("insert")
            except Exception as exc:
                with open("./log_file.txt", "a+") as f:
                    f.write(f"\n {datetime.datetime.now()} - Ошибка заход новичка на сервер - {member.name} - {exc}\n")
                await exceptions.send(
                    f"{datetime.datetime.now()} - Ошибка заход новичка на сервер - {member.name} - {exc}")

        else:  # Если человек найден в бд
            try:
                cursor.execute(f"""UPDATE dis_users SET time_after_leaving 
                = 0, time_afk = 0 WHERE id_discord = {member.id}""")  # Обнуление времени после ухода
                # cursor.execute(f"""UPDATE dis_users SET num_mess
                #         = 0 WHERE id_discord = {member.id}""")
                # cursor.execute(f"""UPDATE dis_users SET time_on_voice
                #                 = 61 WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(
                    f"""SELECT * FROM dis_users WHERE id_discord = {member.id} """)
                member_bd2 = cursor.fetchone()
                if int(member_bd2[3]) > 4200 and (dont_bot and plebey
                                             and nash_chel) not in member.roles:
                    for role in trust_roles:
                        if role in member.roles:
                            await member.remove_roles(role)
                    await member.add_roles(civilian)
                elif int(member_bd2[3]) > 600 or int(member_bd2[2]) > 350 and (
                        dont_bot and civilian and nash_chel) not in member.roles:
                    for role in trust_roles:
                        if role in member.roles:
                            await member.remove_roles(role)
                    await member.add_roles(plebey)
                elif (int(member_bd2[3]) >= 0

                                                  and nash_chel) not in member.roles:
                    await member.add_roles(dont_bot)
                # print("Вторая часть: ", time.time() - t2)
                await check_main_roles(member_bd2, member)
                # print(member_bd2[1]
                if member_bd2[1] == 2:  # Проверка из базы данных на роль
                    await member.add_roles(minor)
                elif member_bd2[1] == 3:  # Проверка из базы данных на роль
                    await member.add_roles(kozyrok)
                elif member_bd2[1] == 4:  # Проверка из базы данных на роль
                    await member.add_roles(churchill)
                elif member_bd2[1] == 5:  # Проверка из базы данных на роль
                    await member.add_roles(intellegence)
                elif member_bd2[1] == 6:  # Проверка из базы данных на роль
                    await member.add_roles(stalin)
                await member.send('''О, всё таки вернулся) :kissing_heart:
Значит не зря тебе напомнил.
**Все** твои **Роли Восстановлены** в полном составе.
И это, **Больше** чтобы такого **Не Было**.
*Это был последний раз, Дружок*''')  # Бот пишет в лс  !!!!!!!
            except Exception as exc:
                with open("./log_file.txt", "a+") as f:
                    f.write(f"\n {datetime.datetime.now()} - Ошибка заход бывшего участника на сервер - {member.name} - {exc}\n")
                await exceptions.send(
                    f"{datetime.datetime.now()} - Ошибка заход новичка на сервер - {member.name} - {exc}")
    except Exception as exc:
        with open("./log_file.txt", "a+") as f:
            f.write(f"\n {datetime.datetime.now()} - Ошибка заход человека на сервер - {member.name} - {exc}\n")
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка заход человека на сервер - {member.name} - {exc}")


@client.event
async def on_raw_reaction_add(reaction):
    try:
        # chann = guild.get_channel(967711624108597318)
        # message = reaction.message_id
        # message = await chann.fetch_message(message)
        # await message.add_reaction(reaction.emoji)
        if reaction.message_id == 977482928365899816:
            if str(reaction.emoji) == "💵":
                await hands_mess.remove_reaction("💵", reaction.member)
                cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
                               )
                member_reaction = cursor.fetchone()
                if hands in reaction.member.roles:
                    await reaction.member.send(
                        '''Ты не устал **Жмакать **на **Кнопочку**?
Заебал, прекращай.''')  # !!!!!!!
                elif member_reaction[3] > 420:
                    await reaction.member.send(
                        f''':shopping_bags: **Поздравляю Тебя с Покупкой!** :shopping_bags:
Была куплена Роль - "{hands.name}"
Данная роль имеется у **{len(hands.members)}** чел.
:sparkling_heart: **Вы** всегда будете **Нашим** желанным **Покупателем!** :cupid:'''
                    )  # !!!!!
                    await reaction.member.add_roles(hands)
                    cursor.execute(f"""UPDATE dis_users SET time_on_voice 
                                                = {member_reaction[3] - 420} WHERE id_discord = {member_reaction[0]}"""
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
Ваш Баланс : {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:

:gift_heart: **Приятной Вам Игры!** :cupid:''')
        # print(reaction.emoji)
        elif reaction.message_id == 974989390755532800:
            if str(reaction.emoji) == "1️⃣":
                await time_voice.remove_reaction("1️⃣", reaction.member)
                channel = await guild.create_voice_channel(name="1x1", user_limit=2, category=gaming_zone)
                try:
                    await reaction.member.move_to(channel)
                    await check(channel)
                except:
                    await reaction.member.send("Зайдите в любой голосовой канал")
                    await check(channel)

            if str(reaction.emoji) == "2️⃣":
                await time_voice.remove_reaction("2️⃣", reaction.member)
                channel = await guild.create_voice_channel(name="2x2", user_limit=4, category=gaming_zone)
                try:
                    await reaction.member.move_to(channel)
                    await check(channel)
                except:
                    await reaction.member.send("Зайдите в любой голосовой канал")
                    await check(channel)
            if str(reaction.emoji) == "3️⃣":
                await time_voice.remove_reaction("3️⃣", reaction.member)
                channel = await guild.create_voice_channel(name="3x3", user_limit=6, category=gaming_zone)
                try:
                    await reaction.member.move_to(channel)
                    await check(channel)
                except:
                    await reaction.member.send("Зайдите в любой голосовой канал")
                    await check(channel)
            if str(reaction.emoji) == "♾️":
                await time_voice.remove_reaction("♾️", reaction.member)
                channel = await guild.create_voice_channel(name="99x99", category=gaming_zone)
                try:
                    await reaction.member.move_to(channel)
                    await check(channel)
                except:
                    await reaction.member.send("Зайдите в любой голосовой канал")
                    await check(channel)

        elif reaction.message_id == 974987029043609660:
            if str(reaction.emoji) == "💰":
                cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
                               )
                member_reaction = cursor.fetchone()
                await balance.remove_reaction("💰", reaction.member)
                await reaction.member.send(
                    f'''Ваш Баланс : {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:''')

        elif reaction.message_id == 970952344122581012:
            if str(reaction.emoji) == "✅":
                await agreement.remove_reaction("✅", reaction.member)
                if who_im in reaction.member.roles:
                    await reaction.member.add_roles(no_name)
                    await reaction.member.remove_roles(who_im)
                    cursor.execute(f"""UPDATE dis_users SET role 
                                        = 1 WHERE id_discord = {reaction.user_id}""")
                    conn.commit()
            elif str(reaction.emoji) == "❌":
                await agreement.remove_reaction("❌", reaction.member)
                if who_im in reaction.member.roles:
                    try:
                        if reaction.member.id not in admins:
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
Данная роль имеется у **{len(minor.members)}** чел.
:sparkling_heart: **Вы** всегда будете **Нашим** желанным **Покупателем!** :cupid:'''
                )  # !!!!!
                await reaction.member.add_roles(minor)
                cursor.execute(f"""UPDATE dis_users SET role 
                        = 2 WHERE id_discord = {member_reaction[0]}""")
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
Ваш Баланс : {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:
    
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
Данная роль имеется у **{len(kozyrok.members)}** чел.
:sparkling_heart: **Вы** всегда будете **Нашим** желанным **Покупателем!** :cupid:'''
                )
                await reaction.member.add_roles(kozyrok)
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
Ваш Баланс : {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:
    
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
Данная роль имеется у **{len(churchill.members)}** чел.
:sparkling_heart: **Вы** всегда будете **Нашим** желанным **Покупателем!** :cupid:'''
                )
                await reaction.member.add_roles(churchill)
                cursor.execute(f"""UPDATE dis_users SET role 
                                    = 4 WHERE id_discord = {member_reaction[0]}""")
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
Ваш Баланс : {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:
    
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
Данная роль имеется у **{len(intellegence.members)}** чел.
:sparkling_heart: **Вы** всегда будете **Нашим** желанным **Покупателем!** :cupid:'''
                )
                await reaction.member.add_roles(intellegence)
                cursor.execute(f"""UPDATE dis_users SET role 
                                    = 5 WHERE id_discord = {member_reaction[0]}""")
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
Ваш Баланс : {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:
    
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
Данная роль имеется у **{len(stalin.members)}** чел.
:sparkling_heart: **Вы** всегда будете **Нашим** желанным **Покупателем!** :cupid:'''
                )
                await reaction.member.add_roles(stalin)
                cursor.execute(f"""UPDATE dis_users SET role 
                                    = 6 WHERE id_discord = {member_reaction[0]}""")
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
Ваш Баланс : {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:

:gift_heart: **Приятной Вам Игры!** :cupid:''')

        elif reaction.message_id == 970951993252278344 and str(
                reaction.emoji) == "<:HeartsofIronIV:953363622501969960>":  # HOI
            if hoi not in reaction.member.roles:
                await reaction.member.add_roles(hoi)
        elif reaction.message_id == 970951993252278344 and str(
                reaction.emoji) == "<:MenofWar:953352918218711070>":  # MO
            if mow not in reaction.member.roles:
                await reaction.member.add_roles(mow)
    except Exception as exc:
        with open("./log_file.txt", "a+") as f:
            f.write(f"\n {datetime.datetime.now()} - Ошибка Добавление реакции - {reaction.user_id} - {reaction.message_id} - {exc}\n")
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка Добавление реакции - {reaction.user_id} - {reaction.message_id} - {exc}")
    # if reaction.message_id == 966746342800113676 and str(reaction.emoji) == "✅":  # Баланс
    #     cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.member_id}""")
    #     balance = cursor.fetchone()
    #     await reaction.member.send(f"Часов:{balance[3] // 60}\nЧисло сообщений:{balance[2]}")  # !!!!!!


@client.event
async def on_message(message):
    try:
        if message.author.bot:  # Проверка на сообщение от пользователя
            return
        # if message.author.id in admins:
        #     return
        if message.channel.id == 983112905098666074:  # Канал для комманд боту

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
                        f"Слизь со стены - {message.author.name} отлетела в помоечку.")
                    await exceptions.send(
                        f"{datetime.datetime.now()} - ban_for_link - {message.author.name} - Отлетел в помойку")
                links_warn.append(message.author.id)
                await message.delete()
                await message.channel.send(
                    f"О, животное - {message.author.name} в чате пытается рекламировать свою хуету.")
                await exceptions.send(
                    f"{datetime.datetime.now()} - link - {message.author.name} - Животное рекламирует хуету")
            if len(str(message.content)) > 500 and message.channel.id != 967710989728497664:  # Если больше 400 сим удаление
                await message.delete()
            else:
                if not flag:
                    await timer_messages(5)
        elif message.author.id == 869217405862305822 or message.author.id == 597161042367348736:
            await client.process_commands(message)
    except Exception as exc:
        with open("./log_file.txt", "a+") as f:
            f.write(f"\n {datetime.datetime.now()} - Ошибка Сообщение - {message.author.id} - {message.content} - {exc}\n")
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка Сообщение - {message.author.id} - {message.content} - {exc}")
"""

----------------------COMMANDS

"""


@client.command()
async def update_time(ctx, arg, arg2):
    try:
        user = await guild.fetch_member(arg)
        cursor.execute(f"""UPDATE dis_users SET time_on_voice = {int(arg2) * 60} WHERE id_discord = {arg}""")
        conn.commit()
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        bd = cursor.fetchone()

        await ctx.send(f"У участника {user.name} в базе данных {round(bd[3] / 60)} ч.")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def add_to_time(ctx, arg, arg2):
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        bd = cursor.fetchone()
        user = await guild.fetch_member(arg)
        cursor.execute(f"""UPDATE dis_users SET time_on_voice = {(int(arg2) * 60) + bd[3]} WHERE id_discord = {arg}""")
        conn.commit()
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        bd = cursor.fetchone()
        await ctx.send(f"У участника {user.name} в базе данных {round(bd[3] / 60)} ч.")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def add_to_mess(ctx, arg, arg2):
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        bd = cursor.fetchone()
        user = await guild.fetch_member(arg)
        cursor.execute(f"""UPDATE dis_users SET time_on_voice = {int(arg2) + bd[2]} WHERE id_discord = {arg}""")
        conn.commit()
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        bd = cursor.fetchone()

        await ctx.send(f"У участника {user.name} в базе данных {bd[2]} ч.")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def update_mess(ctx, arg, arg2):
    try:
        user = await guild.fetch_member(arg)
        cursor.execute(f"""UPDATE dis_users SET num_mess = {int(arg2)} WHERE id_discord = {arg}""")
        conn.commit()
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        bd = cursor.fetchone()

        await ctx.send(f"У участника {user.name} в базе данных {bd[2]} сообщ.")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def get_info(ctx, arg):
    try:
        user = await guild.fetch_member(arg)
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {arg}""")
        bd = cursor.fetchone()
        await ctx.send(f"""Информация об участнике **{user.name}**:
ID:  {bd[0]}
ID Роли:  {bd[1]}
Число сообщений:  {bd[2]}
Время в войсе:  {int(bd[3])} мин. = {int(bd[3]) / 60} ч.
Предупреждений:  {bd[4]}
Время афк:  {int(bd[5])} мин. = {int(bd[5]) / 60} ч.
Время после выхода:  {int(bd[6])}
Время захода: {bd[7]}
Время создания аккаунта: {user.created_at}
Время след. уведомления: {bd[8]}""")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка - {exc}")
        with open("./log_file.txt", "a+") as f:
            f.write(f"\n {datetime.datetime.now()} - {exc}\n")


@client.command()
async def insert(ctx, arg):
    try:
        cursor.execute(f"""{arg}""")
        conn.commit()
        await ctx.send("Успешно")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def select(ctx, arg):
    try:
        cursor.execute(f"""{arg}""")
        bd = cursor.fetchall()
        await ctx.send(f"""{bd}""")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def mess(ctx, arg, arg2):
    try:
        user = await client.fetch_user(arg)
        await user.send(str(arg2))
        await ctx.send(f"Отправлено:\n\n{arg2} \n\n для пользователя {user.name}")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def check_channel(ctx, arg):
    try:
        channel = await client.fetch_channel(arg)
        await ctx.send("Успешно")
        await check(channel)
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def test(ctx):
    await ctx.send(datetime.datetime.now())
    # channel = guild.get_channel(948644785118404618)
    # async for message in channel.history(limit=300):
    #     try:
    #         cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {message.author.id}""")
    #         bd = cursor.fetchall()
    #         if bd is None:
    #             cursor.execute(f"""INSERT INTO dis_users VALUES ('{message.author.id}', '1', '0', '0', '0', '0', '0', '0')""")
    #             conn.commit()
    #
    #         struct_time = message.created_at
    #         struct_time += datetime.timedelta(hours=3)
    #         struct_time = struct_time.strftime('%d/%m/%Y, %H:%M:%S')
    #         cursor.execute(
    #             f"""UPDATE dis_users SET time_join = "{str(struct_time)}", role = 1 WHERE id_discord = {message.author.id}""")
    #         conn.commit()
    #     except:
    #         print(mess.author.name)
    # print("complete")


@client.command()
async def name(ctx, arg):
    try:
        user = await guild.fetch_member(arg)
        await ctx.send(user.name)
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def check_timer(ctx):
    try:
        await ctx.send(diff)
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command(pass_context=True)
async def give_log(ctx):
    global log_var
    try:
        log_var = True
        while True:
            if log_var == False:
                await ctx.send('Готово!', file=discord.File("log_timer.txt"))
                break
            await ctx.send(log_var)
            await asyncio.sleep(10)
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")

@client.command()
async def restart(ctx):
    subprocess.run(["systemctl", "restart", "runscript.service"])


if __name__ == '__main__':
    client.run("")
