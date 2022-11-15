import discord, sqlite3, time, os, asyncio, datetime, subprocess, openpyxl
import parse_mosreg as ps
from discord.ext import commands, tasks


# from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

intents = discord.Intents.all()
intents.members = True
intents.bans = True
global client, exceptions_members, list_boost
client = commands.Bot(command_prefix="$", intents=intents)

flag = False

list_warnings = []
messages = {}

admins = []
links_warn = []
exceptions_members = []
list_boost = {}


log_var = False

log_var2 = False
global log_timer
global send_text_on_click_react_button, send_text_small_money, delete_vip_roles, congr, buying_vip
global check_buy_vip


class Timer(commands.Cog):
    def __init__(self):
        
        self.main_loop.start()

    def stop_timer(self):
        self.main_loop.cancel()

    def change_time(self, sec):
        self.main_loop.change_interval(seconds=sec)

    @tasks.loop(seconds=10.0)
    async def main_loop(self):
        global log_var2, diff, log_var, list_boost
        # try:
        """Если нужно сделать логи таймера"""
        member_error = "none"
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

        """Проверка аватарки"""
        t1 = time.time()
        result = time.gmtime(t1)
        if result.tm_hour == 19 and result.tm_min == 30 and result.tm_sec > 49:
            with open("night.png", "rb") as image:
                avatar = image.read()
            await client.user.edit(avatar=avatar, username="Stalin")
            with open("night_guild.jpg", "rb") as image:
                avatar = image.read()
            await guild.edit(icon=avatar)
        elif result.tm_hour == 4 and result.tm_min == 1 and result.tm_sec > 49:
            with open("day.png", "rb") as image:
                avatar = image.read()
            await client.user.edit(avatar=avatar, username="Vovan")
            with open("day_guild.jpeg", "rb") as image:
                avatar = image.read()
            await guild.edit(icon=avatar)
        
        members = guild.members

        """Обход всех участников"""
        for member in members:
            """Логи"""
            member_error = f"{member.name} - {member.id}"
            t2 = time.time()
            t3 = time.time()
            # print(member.id)
            # try:
            if member.bot:
                continue
            cursor.execute(
                    f"""SELECT * FROM dis_users WHERE id_discord = {member.id}""")
            member_bd = cursor.fetchone()
            try:
                temp_list = member_bd[1].split(',')
            except Exception as exc:
                await exceptions.send(
                        f"{datetime.datetime.now()} - Ошибка - {member.name} {member.id}- {exc}")
                continue
            # print(member_bd)
            struct_time = datetime.datetime.now()
            struct_time += datetime.timedelta(hours=3)
            """Достижение ЛЮТЫЙ"""
            if hoi in member.roles and mow in member.roles and thunder in member.roles and \
                    stellaris in member.roles and mine in member.roles and zomb in member.roles:
                if lutiy_ not in member.roles:
                    if '11' not in temp_list:
                        temp_list.append('11')
                    await member.add_roles(lutiy_)
                    await member.send("Поздравляю ты получил достижение ЛЮТЫЙ и 5 Social Credit")
                    cursor.execute(
                        f"""UPDATE dis_users SET credits = {int(member_bd[10]) + 5} WHERE id_discord = {member.id}""")
                    cursor.execute(
                        f"""UPDATE dis_users SET role = '{",".join(temp_list)}' WHERE id_discord = {member.id}""")
                    conn.commit()
            try:
                """Проверка дня рождения"""
                if member_bd[8] is not None:
                    if struct_time.day == datetime.datetime.strptime(member_bd[8], "%d/%m").day:
                        if struct_time.month == datetime.datetime.strptime(member_bd[8], "%d/%m").month:
                            if birthday_role not in member.roles:
                                await member.add_roles(birthday_role)
                                try:
                                    await member.send(f"Поздравляем **{member.display_name}** с днем рождения!!!")
                                except:
                                    pass
                                try:
                                    struct_time = datetime.datetime.now()
                                    struct_time += datetime.timedelta(days=1)
                                    str_time = struct_time.strftime('%d/%m/%Y, %H:%M:%S')
                                    await member.add_roles(X2)
                                    list_boost[member.id] = struct_time
                                    cursor.execute(f"""UPDATE dis_users SET time_end_boost 
                                                                    = '{str_time}' WHERE id_discord = {member.id}""")
                                    conn.commit()
                                except:
                                    pass

                    else:
                        if birthday_role in member.roles:
                            await member.remove_roles(birthday_role)
            except Exception as exc:
                await exceptions.send(
                        f"{datetime.datetime.now()} - Ошибка Роль День рождения - {member.name} - {exc}")

            """Проверка если новичок на сервере без соглашения больше 72 часов 
            и добавления в список админов"""
            # if '11' not in temp_list:
            #     temp_list.append('11')
            if '0' in temp_list and member_bd[5] > 4320:
                await guild.kick(user=member)

            """Добавление админов в список"""
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

            """Логи"""
            if log_var2:
                log_timer.write(f"{member.name} - Первая часть: {time.time() - t2} - Роли: {member.roles}\n")
            t2 = time.time()

            """Счетчик афк"""
            cursor.execute(
                f"""UPDATE dis_users SET time_afk = {member_bd[5] + 0.166} WHERE id_discord = {member.id}""")
            conn.commit()

            """Логи"""
            if log_var2:
                log_timer.write(f"{member.name} - Вторая часть(Обновление в бд афк): {time.time() - t2}\n")
            t2 = time.time()

            try:
                """Проверка войс чата"""
                # print(member.name)
                # print(member.voice)
                if member.voice is not None and member.voice.channel != pivo and member.voice.self_mute == False:  # Если участник в войсе и не в пивнушке
                    if who_im in member.roles:
                        await member.remove_roles(who_im)
                        if '0' in temp_list:
                            temp_list.remove('0')
                        if no_name not in member.roles:
                            await member.add_roles(no_name)
                            if '1' not in temp_list:
                                temp_list.append('1')
                            cursor.execute(
                                    f"""UPDATE dis_users SET role = '{",".join(temp_list)}' WHERE id_discord = {member.id}""")
                            conn.commit()
                    """Достижение войс"""
                    if member_bd[3] > 6000 and voice_100_ not in member.roles:
                        if '5' not in temp_list:
                            temp_list.append('5')
                        await member.send("Поздравляю ты получил достижение На Связи и 3 Social Credit")
                        await member.add_roles(voice_100_)
                        cursor.execute(
                            f"""UPDATE dis_users SET role = '{",".join(temp_list)}' WHERE id_discord = {member.id}""")
                        cursor.execute(
                            f"""UPDATE dis_users SET credits = {member_bd[10] + 3} WHERE id_discord = {member.id}""")
                        conn.commit()

                    if X2 in member.roles:
                        cursor.execute(  # Счет времени в войсе Х2
                        f"""UPDATE dis_users SET time_on_voice = {member_bd[3] + 0.332} WHERE id_discord = {member.id}"""
                    )
                        cursor.execute(  # Счет кредитов Х2
                            f"""UPDATE dis_users SET credits = {member_bd[10] + 0.00111} WHERE id_discord = {member.id}"""
                        )
                        conn.commit()
                    elif X4 in member.roles:
                        cursor.execute(  # Счет времени в войсе Х4
                        f"""UPDATE dis_users SET time_on_voice = {member_bd[3] + 0.664} WHERE id_discord = {member.id}"""
                    )
                        cursor.execute(  # Счет кредитов Х4
                            f"""UPDATE dis_users SET credits = {member_bd[10] + 0.00222} WHERE id_discord = {member.id}"""
                        )
                        conn.commit()
                    else:
                        cursor.execute(  # Счет времени в войсе
                            f"""UPDATE dis_users SET time_on_voice = {member_bd[3] + 0.166} WHERE id_discord = {member.id}"""
                        )
                        cursor.execute(  # Счет кредитов
                            f"""UPDATE dis_users SET credits = {member_bd[10] + 0.000555} WHERE id_discord = {member.id}"""
                        )
                        conn.commit()
                    cursor.execute(
                        f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {member.id}"""
                    )  # Обнуление счетчика афк
                    conn.commit()
                elif member.voice is not None and member.voice.channel == pivo:
                    if member_bd[9] is None:
                        cursor.execute(  # Счет времени в afk войсе
                            f"""UPDATE dis_users SET time_afk_voice = 0 WHERE id_discord = {member.id}""")
                        conn.commit()
                    """Достижение афк"""
                    if member_bd[9] > 1440 and afk_master_ not in member.roles:
                        if '9' not in temp_list:
                            temp_list.append('9')
                        await member.send("Поздравляю ты получил достижение Афк Мастер и 3 Social Credit")
                        await member.add_roles(afk_master_)
                        cursor.execute(
                            f"""UPDATE dis_users SET role = '{",".join(temp_list)}' WHERE id_discord = {member.id}""")
                        cursor.execute(
                            f"""UPDATE dis_users SET credits = {member_bd[10] + 3} WHERE id_discord = {member.id}""")
                        conn.commit()
                    cursor.execute(  # Счет времени в afk войсе
                            f"""UPDATE dis_users SET time_afk_voice = {member_bd[9] + 0.166} WHERE id_discord = {member.id}"""
                        )
                    conn.commit()
            except Exception as exc:

                await exceptions.send(
                        f"{datetime.datetime.now()} - Ошибка Таймер участников проверка войса - {member.name} - {exc}")

            """Логи"""
            if log_var2:
                log_timer.write(f"{member.name} - Третья часть(Проверка на войс и сброс афк): {time.time()-t2} - {member.voice}\n")
            t2 = time.time()

            """Проверка всех ролей"""
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
                await member.remove_roles(dead)
            if member_bd[
                5] > 129600 and member.id not in admins:  # Если афк больше 424 часов кик
                try:
                    await member.send(f'''Ещё не запылился?
Ты был **Исключён** из сервера " :banana: **Men of Cum - Redux** :milk:" за **Не активность** на **Сервере!**
Если ты захочешь **Вернуться** к нам на **Сервер**, то советую поторопиться ...
Все твои **Роли** скоро **Исчезнут**, да да...
*У тебя Неделя, Дружок* :innocent:

    :arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:''')  # !!!!!
                except Exception as exc:

                    await exceptions.send(f"{datetime.datetime.now()} - Ошибка Таймер участников афк кик - {member.name} - {exc}")
                finally:
                    await exceptions.send(
                        f"{datetime.datetime.now()} - Кик участника за афк - {member.name}")
                    await guild.kick(user=member)
            elif member_bd[5] > 128160:  # Если афк больше 420 часов трупачек
                await member.add_roles(dead)

            """Логи"""
            if log_var2:
                log_timer.write(
                    f"{member.name} - Четвертая часть(Провека ролей): {time.time() - t2}\n")
            if log_var2:
                log_timer.write(
                    f"{member.name} - Всего: {time.time() - t3}\n")
            conn.commit()

        """Проверка бустов"""
        try:
            # print(list_boost)
            for k in list_boost:
                if datetime.datetime.now() > list_boost[k]:
                    print(123)
                    user = guild.get_member(k)
                    try:
                        await user.remove_roles(X2)
                    except:
                        print("err")
                    try:
                        await user.remove_roles(X4)
                    except:
                        print("err2")
                    cursor.execute(f"""UPDATE dis_users SET time_end_boost = '0' WHERE id_discord = {k}""")
                    conn.commit()
                    del list_boost[k]
        except Exception as exc:
            print(exc)

        diff = time.time() - t1
        print(diff)
        if log_var2:
            log_timer.write(
                f"\n\n{datetime.datetime.now()} - Задержка таймера: {diff}\n")
            log_timer.close()
            log_var2 = False
            log_var = False
        if diff > 15:
            await exceptions.send(f"{datetime.datetime.now()} - Время обработки превышено - {diff}")
        # except Exception as exc:
        #     print(121)
        #     await exceptions.send(f"{datetime.datetime.now()} - Ошибка Таймер - {exc}\n{member_error}")
        #     subprocess.run(["systemctl", "restart", "runscript.service"])


@client.event
async def on_ready():

    global conn, cursor, guild, timer, list_boost

    global who_im, dont_bot, plebey, civilian, nash_chel

    global no_name, zadrot, worker, lybitel, zymerok, chel

    global intellegence, stalin

    global hoi, mow, thunder, stellaris, mine, zomb

    global senator, admin, organizer, moder

    global dead

    global hands, birthday_role, X2, X4

    global role_666_, voice_100_, ping_, get_warning_, buy_vip_, afk_master_, shizik_, lutiy_

    global pivo, tech_channels, general, working_hands, main_roles, trust_roles, choice_roles, vip_roles, exceptions

    global balance, time_voice, hands_mess

    global gaming_zone, console


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

    intellegence = guild.get_role(962063644861010001)
    stalin = guild.get_role(958444218383224853)

    senator = guild.get_role(962065215950835793)
    organizer = guild.get_role(945344360973742090)
    admin = guild.get_role(972535623128862770)
    moder = guild.get_role(972533459790753792)

    """Роли"""
    hoi = guild.get_role(953762306628653146)
    mow = guild.get_role(953763442303594616)
    thunder = guild.get_role(998529734520610856)
    stellaris = guild.get_role(1001516316303310888)
    mine = guild.get_role(998530465742987265)
    zomb = guild.get_role(1002990478129631263)

    dead = guild.get_role(953758013058060338)  # Роль труп

    hands = guild.get_role(965007953671356416)
    birthday_role = guild.get_role(1007381174240432218)
    X2 = guild.get_role(1015909775692808212)
    X4 = guild.get_role(1015910232892915792)

    """Достижения"""
    role_666_ = guild.get_role(1009536699078033518)
    voice_100_ = guild.get_role(1009536850488197231)
    ping_ = guild.get_role(1009537583954542622)
    get_warning_ = guild.get_role(1009537203141099692)
    buy_vip_ = guild.get_role(1009537668939518033)
    afk_master_ = guild.get_role(1009538166820196382)
    shizik_ = guild.get_role(1009538819743305821)
    lutiy_ = guild.get_role(1009538481057452042)

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
    console = guild.get_channel(983112905098666074)

    main_roles = [no_name, chel, zymerok, lybitel, worker, zadrot]
    trust_roles = [dont_bot, plebey, civilian]
    vip_roles = [intellegence, stalin]
    choice_roles = [hoi, mow, thunder, stellaris, mine, zomb]
    exceptions = guild.get_channel(981978051762061362)

    gaming_zone = guild.get_channel(940667074638921771)

    # agreement = await guild.get_channel(1007651685931429928).fetch_message(1020990889629339710)
    # intellegence_mess = await guild.get_channel(967711624108597318).fetch_message(1015625607658356827)
    # stalin_mess = await guild.get_channel(967711624108597318).fetch_message(1015625903293878343)
    balance = await guild.get_channel(1009223762769621124).fetch_message(1010874327773741199)
    time_voice = await guild.get_channel(1009224041493692436).fetch_message(1013415312915447909)
    # hands_mess = await guild.get_channel(967711624108597318).fetch_message(977482928365899816)

        # print("else")
    conn = sqlite3.connect("./mydatabase.db")  # Соединение с бд
    cursor = conn.cursor()
    ggg = []
    for member in guild.members:
        try:
            cursor.execute(
            f"""SELECT * FROM dis_users WHERE id_discord = '{member.id}'""")
            bd = cursor.fetchone()
            ggg.append(bd[0])

            if bd[6] != 0:
                str_time = datetime.datetime.strptime(bd[6], '%d/%m/%Y, %H:%M:%S')
                list_boost[member.id] = str_time
        except:
            pass
    cursor.execute(
        f"""SELECT * FROM dis_users""")
    bd = cursor.fetchall()
    for i in bd[0]:
        if i not in ggg:
            cursor.execute(f"""DELETE FROM dis_users WHERE id_discord = '{i}'""")
            conn.commit()
    t1 = time.time()
    result = time.gmtime(t1)
    
    try:
        for i in range(19, 24):
            if result.tm_hour == i:
                with open("night.png", "rb") as image:
                    avatar = image.read()
                await client.user.edit(avatar=avatar, username="Stalin")
                with open("night_guild.jpg", "rb") as image:
                    avatar = image.read()
                await guild.edit(icon=avatar)
        for i in range(0, 4):
            if result.tm_hour == i:
                with open("night.png", "rb") as image:
                    avatar = image.read()
                await client.user.edit(avatar=avatar, username="Stalin")
                with open("night_guild.jpg", "rb") as image:
                    avatar = image.read()
                await guild.edit(icon=avatar)
        for i in range(4, 19):
            if result.tm_hour == i:
                with open("day.png", "rb") as image:
                    avatar = image.read()
                await client.user.edit(avatar=avatar, username="Vovan")
                with open("day_guild.jpeg", "rb") as image:
                    avatar = image.read()
                await guild.edit(icon=avatar)

    except:
        pass
    try:
        await console.send(f"Перезапуск: {result.tm_mday}.{result.tm_mon}.{result.tm_year}")
    except:
        pass
    print("ready")
    timer = Timer()  # Обновление каждую минуту время в войсе и афк


# @client.event
# async def on_raw_reaction_remove(reaction):
#


@client.event
async def on_member_remove(member):
    if member.bot:  # Проверка на сообщение от пользователя
        return
    try:
        if who_im in member.roles:
            cursor.execute(
                f"""DELETE FROM dis_users WHERE id_discord = {member.id}""")
            conn.commit()
        await exceptions.send(f"{datetime.datetime.now()} - Участника больше нет на сервере - {member.name} - id: {member.id}")
    except Exception as exc:
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка выход человека с сервера - {member.id} - {exc}")


@client.event
async def on_member_ban(guild, user):
    try:
        if user.id in admins:
            return
        cursor.execute(f"""DELETE FROM dis_users WHERE id_discord = {user.id}""")
        conn.commit()
    except Exception as exc:
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка бан человека - {user.id} - {exc}")


@client.event
async def on_member_join(member):  # Когда человек заходит на сервер

    if member.bot:  # Проверка на сообщение от пользователя
        return
    struct_time = datetime.datetime.now(datetime.timezone.utc)
    days = struct_time - member.created_at
    struct_time += datetime.timedelta(hours=3)
    # struct_time2 = struct_time + datetime.timedelta(weeks=1)
    # struct_time2 = struct_time2.strftime('%d/%m/%Y, %H:%M:%S')
    struct_time = struct_time.strftime('%d/%m/%Y, %H:%M:%S')
    # print(days)
    cursor.execute(
        f"""SELECT * FROM dis_users WHERE id_discord = {member.id} """)

    if int(days.days) < 60:
        if member.id not in exceptions_members:
            await exceptions.send(f"{datetime.datetime.now()} - Твинк пытался зайти на сервер, но был наказан - {member.id}")
            await guild.kick(member)

    if cursor.fetchone() is None:  # Если человек не найден в бд
        try:
            t = guild.get_role(1009536415928942712)
            tt = guild.get_role(962055146781679657)
            await member.add_roles(t, who_im, no_name, tt)
            # Добавление новичку роли Кто я?
            cursor.execute(f"""INSERT INTO dis_users
                                  VALUES ('{member.id}', '0', '0',
                                  '0', '0', '0', '0', '{struct_time}', NULL, '0', '0', '0')"""
                           )  # нулевая роль это доверительная кто я
            conn.commit()
            # await exceptions.send(f"{datetime.datetime.now()} - Заход на сервер - {member.name} - Аккаунт создан: {member.created_at}")
            # print("insert")
            # await exceptions.send(
            #     f"{datetime.datetime.now()} - Кто я? - {member.name}")
        except Exception as exc:
             await exceptions.send(
                f"{datetime.datetime.now()} - Ошибка заход новичка на сервер - {member.name} - {exc}")

    else:  # Если человек найден в бд
        try:
            cursor.execute(f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {member.id}""")  # Обнуление времени после ухода
            # cursor.execute(f"""UPDATE dis_users SET num_mess
            #         = 0 WHERE id_discord = {member.id}""")
            # cursor.execute(f"""UPDATE dis_users SET time_on_voice
            #                 = 61 WHERE id_discord = {member.id}""")
            conn.commit()
            cursor.execute(
                f"""SELECT * FROM dis_users WHERE id_discord = {member.id} """)
            member_bd2 = cursor.fetchone()
            t = guild.get_role(1009536415928942712)
            tt = guild.get_role(962055146781679657)
            await member.add_roles(t, tt)
            print(member_bd2)
            if int(member_bd2[3]) > 4200 and dont_bot not in member.roles and plebey not in member.roles \
                                         and nash_chel not in member.roles:
                for role in trust_roles:
                    if role in member.roles:
                        await member.remove_roles(role)
                await member.add_roles(civilian)
            elif int(member_bd2[3]) > 600 or int(member_bd2[2]) > 350 and \
                    dont_bot not in member.roles and civilian not in member.roles and nash_chel not in member.roles:
                for role in trust_roles:
                    if role in member.roles:
                        await member.remove_roles(role)
                await member.add_roles(plebey)
            elif (int(member_bd2[3]) >= 0 and nash_chel) not in member.roles:
                await member.add_roles(dont_bot)
            # print("Вторая часть: ", time.time() - t2)
            await check_main_roles(member_bd2, member)
            # print(member_bd2[1]
            # if member_bd2[1] == 2:  # Проверка из базы данных на роль
            #     await member.add_roles(minor)
            # elif member_bd2[1] == 3:  # Проверка из базы данных на роль
            #     await member.add_roles(kozyrok)
            # elif member_bd2[1] == 4:  # Проверка из базы данных на роль
            #     await member.add_roles(churchill)
            """Восстановление достижений"""

            temp_list = member_bd2[1].split(",")
            print(temp_list)
            if '2' in temp_list:  # Проверка из базы данных на роль
                await member.add_roles(intellegence)
            elif '3' in temp_list:  # Проверка из базы данных на роль
                await member.add_roles(stalin)
            if '4' in temp_list:
                await member.add_roles(role_666_)
            if '5' in temp_list:
                await member.add_roles(voice_100_)
            if '6' in temp_list:
                await member.add_roles(ping_)
            if '7' in temp_list:
                await member.add_roles(get_warning_)
            if '8' in temp_list:
                await member.add_roles(buy_vip_)
            if '9' in temp_list:
                await member.add_roles(afk_master_)
            if '10' in temp_list:
                await member.add_roles(shizik_)
            if '11' in temp_list:
                await member.add_roles(lutiy_)

            await member.send('''О, всё таки вернулся) :kissing_heart:
Значит не зря тебе напомнил.
**Все** твои **Роли и Достижения Восстановлены** в полном составе.
И это, **Больше** чтобы такого **Не Было**.
*Это был последний раз, Дружок*''')  # Бот пишет в лс  !!!!!!!
        except Exception as exc:
            await exceptions.send(
                f"{datetime.datetime.now()} - Ошибка заход новичка на сервер - {member.name} - {exc}")
    # except Exception as exc:
    #     await exceptions.send(f"{datetime.datetime.now()} - Ошибка заход человека на сервер - {member.name} - {exc}")


@client.event
async def on_raw_reaction_add(reaction):
    try:
        print(reaction.message_id)
        # print(str(reaction.emoji))
        # <:minecraftaccept:953387049950527488>
        # <:minecraftdeny:953387065347813536>
        # <:Communism:983102694854119464>
        # <:FortniteF_Key:953387191717998622>
        # 2️⃣ 6️⃣ ♾️

        # chann = guild.get_channel(983112905098666074)
        # message = reaction.message_id
        # message = await chann.fetch_message(message)
        # await message.add_reaction(reaction.emoji)
        if reaction.member.bot:  # Проверка на сообщение от пользователя
            return
        elif reaction.message_id == 1025685771878936626:
            mess = await guild.get_channel(1025685710293962772).fetch_message(reaction.message_id)
            await mess.remove_reaction("<:minecraftaccept:953387049950527488>", reaction.member)
            await console.send("Ожидай...")
            subprocess.run(["systemctl", "restart", "runscript.service"])
        #    Temp voice
        elif reaction.message_id == 1013415312915447909:

            if str(reaction.emoji) == "2️⃣":

                await time_voice.remove_reaction("2️⃣", reaction.member)
                channel = await guild.create_voice_channel(name="2x", user_limit=2, category=gaming_zone)
                await check_and_move(reaction, channel)
            if str(reaction.emoji) == "6️⃣":
                await time_voice.remove_reaction("6️⃣", reaction.member)
                channel = await guild.create_voice_channel(name="6x", user_limit=6, category=gaming_zone)
                await check_and_move(reaction, channel)
            if str(reaction.emoji) == "♾️":
                await time_voice.remove_reaction("♾️", reaction.member)
                channel = await guild.create_voice_channel(name="99x", category=gaming_zone)
                await check_and_move(reaction, channel)
        #    Школьный портал
        elif reaction.message_id == 1024723746617032815:
            text_chann = guild.get_channel(1024730756305653830)
            mess = await guild.get_channel(1024723619898720386).fetch_message(1024723746617032815)
            await mess.remove_reaction("<:minecraftaccept:953387049950527488>", reaction.member)
            async for message in text_chann.history(limit=200):
                await message.delete()
            # await guild.get_channel(1024730756305653830).send("Ожидай...")
            init = ps.Parsing()
            init.loggining()
            init.parse_hours()
            read_xl()
            with open("residue.txt", "r") as h:
                residue = h.read()
            await text_chann.send(residue)
        #    Школьный портал
        elif reaction.message_id == 1024731248733724702:
            text_chann = guild.get_channel(1024731099919818804)
            mess = await guild.get_channel(1024723619898720386).fetch_message(1024731248733724702)
            await mess.remove_reaction("<:minecraftaccept:953387049950527488>", reaction.member)
            async for message in text_chann.history(limit=200):
                await message.delete()
            init = ps.Parsing()
            init.loggining()
            init.parse_timetable()
            with open("timetable.txt", "r") as h:
                table = h.read()
            await text_chann.send(table)
        #    Баланс
        elif reaction.message_id == 1010874327773741199:

            if str(reaction.emoji) == "<:FortniteF_Key:953387191717998622>":
                cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
                                )
                member_reaction = cursor.fetchone()
                await balance.remove_reaction("<:FortniteF_Key:953387191717998622>", reaction.member)
                await reaction.member.send(
                    f'''Ваш Баланс : {int(member_reaction[10])} Social Credits и {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:''')

        #    """Roles, Shop"""

        elif reaction.channel_id == 1007651685931429928 or reaction.channel_id == 948658541206573106 or \
                reaction.channel_id == 967711624108597318 or reaction.channel_id == 1015877658812362762:
            # if reaction.message_id == 1020990889629339710:
            #     if str(reaction.emoji) == "<:minecraftaccept:953387049950527488>":
            #         await agreement.remove_reaction("<:minecraftaccept:953387049950527488>", reaction.member)
            #         if who_im in reaction.member.roles:
            #             await reaction.member.add_roles(no_name)
            #             await reaction.member.remove_roles(who_im)
            #             cursor.execute(f"""UPDATE dis_users SET role
            #                                 = '1' WHERE id_discord = {reaction.user_id}""")
            #             conn.commit()
            #     elif str(reaction.emoji) == "<:minecraftdeny:953387065347813536>":
            #         await agreement.remove_reaction("<:minecraftdeny:953387065347813536>", reaction.member)
            #         if who_im in reaction.member.roles:
            #             try:
            #                 if reaction.member.id not in admins:
            #                     await reaction.member.kick()
            #             except:
            #                 pass
            temp_chann = guild.get_channel(reaction.channel_id)
            temp_mess = await temp_chann.fetch_message(reaction.message_id)
            await temp_mess.remove_reaction("<:minecraftaccept:953387049950527488>", reaction.member)
            """Roles"""
            if reaction.message_id == 1020988233317896284 or reaction.message_id == 1015534668570959903:  # HOI
                if hoi not in reaction.member.roles:
                    await reaction.member.add_roles(hoi)
            elif reaction.message_id == 1020988543230808115 or reaction.message_id == 1015534981080170616:  # MO
                if mow not in reaction.member.roles:
                    await reaction.member.add_roles(mow)
            elif reaction.message_id == 1020988370962370580 or reaction.message_id == 1015534797440958495:
                if thunder not in reaction.member.roles:
                    await reaction.member.add_roles(thunder)
            elif reaction.message_id == 1020988438578741270 or reaction.message_id == 1015534870522507314:
                if stellaris not in reaction.member.roles:
                    await reaction.member.add_roles(stellaris)
            elif reaction.message_id == 1020988601791684669 or reaction.message_id == 1015535025095200768:
                if mine not in reaction.member.roles:
                    await reaction.member.add_roles(mine)
            elif reaction.message_id == 1020988702157180948 or reaction.message_id == 1015535104589844652:
                if zomb not in reaction.member.roles:
                    await reaction.member.add_roles(zomb)

            #    """VIP Roles"""
            # Интеллигенция
            elif reaction.message_id == 1015625607658356827 or reaction.message_id == 1015890393214238771:
                await check_buy_vip(reaction, intellegence)

            # Шиза Сталина
            elif reaction.message_id == 1015625903293878343 or reaction.message_id == 1015890837911109642:
                await check_buy_vip(reaction, stalin)

            #    """Бусты"""
            #  X2
            elif reaction.message_id == 1015893741577453568 or reaction.message_id == 1015871263178240051:
                if X2 in reaction.member.roles or X4 in reaction.member.roles:
                    await reaction.member.send('У вас уже действует буст')
                else:
                    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
                                   )
                    member_reaction = cursor.fetchone()
                    if int(member_reaction[10]) >= 6:
                        await reaction.member.send("Вы активировали буст Х2")
                        await add_boost(reaction.member, member_reaction, 2)
                    else:
                        await send_text_small_money(reaction, member_reaction)
            #  X4
            elif reaction.message_id == 1015871435144691752 or reaction.message_id == 1015893972775878717:
                if X2 in reaction.member.roles or X4 in reaction.member.roles:
                    await reaction.member.send('У вас уже действует буст')
                else:
                    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}"""
                                   )
                    member_reaction = cursor.fetchone()
                    if int(member_reaction[10]) >= 6:
                        await reaction.member.send("Вы активировали буст Х4")
                        await add_boost(reaction.member, member_reaction, 4)
                    else:
                        await send_text_small_money(reaction, member_reaction)

    except Exception as exc:
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка Добавление реакции - {reaction.user_id} - {reaction.message_id} - {exc}")


@client.event
async def on_message(message):
    try:
        if message.author.bot:  # Проверка на сообщение от пользователя
            return
        # if message.author.id in admins:
        #     return
        elif message.channel.id == 983112905098666074:  # Канал для комманд боту
            await client.process_commands(message)

        elif message.author.id == 597161042367348736:
            pass
        elif str(message.channel.type) == "private":
            user = guild.get_member(message.author.id)
            if shizik_ not in user.roles:
                cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {user.id}""")
                bd = cursor.fetchone()
                temp_list = bd[1].split(",")
                if '10' not in temp_list:
                    temp_list.append('10')
                await user.send("Поздравляю ты получил достижение Шизик и 5 Social Credit")
                await user.add_roles(shizik_)
                cursor.execute(
                    f"""UPDATE dis_users SET role = '{",".join(temp_list)}' WHERE id_discord = {user.id}""")
                cursor.execute(
                    f"""UPDATE dis_users SET credits = {bd[10] + 5} WHERE id_discord = {user.id}""")
                conn.commit()
        # :minecraftaccept:
        elif str(
                message.channel.type
        ) != "private" and message.channel not in tech_channels:  # Проверка не на лс и не тех
            # invite = await general.create_invite(max_age = 1800,max_uses = 1)
            # await message.channel.send(invite)
            member_messenger(message.author.id)  # Подсчет сообщений
            if len(str(message.content).split("discord.gg/")
                   ) > 1 and message.author.id not in admins:  # Если в сообщении ссылка то предупреждение
                if message.author.id in links_warn:
                    links_warn.remove(message.author.id)

                    await message.author.ban()
                    await message.channel.send(
                        f"Слизь со стены - {message.author.name} отлетела в помоечку.")
                    await exceptions.send(
                        f"{datetime.datetime.now()} - ban_for_link - {message.author.name} - Отлетел в помойку")
                links_warn.append(message.author.id)
                await message.delete()
                await message.channel.send(
                    f"О, животное - {message.author.name} в чате пытается рекламировать свою хуету.")
                if get_warning_ not in message.author.roles:
                    cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {message.author.id}""")
                    bd = cursor.fetchone()
                    temp_list = bd[1].split(",")
                    if '7' not in temp_list:
                        temp_list.append('7')
                    await message.author.send("Поздравляю ты получил достижение Плохиш и 3 Social Credit")
                    await message.author.add_roles(get_warning_)
                    cursor.execute(
                        f"""UPDATE dis_users SET role = '{",".join(temp_list)}' WHERE id_discord = {message.author.id}""")
                    cursor.execute(
                        f"""UPDATE dis_users SET credits = {bd[10] + 3} WHERE id_discord = {message.author.id}""")
                    conn.commit()
                await exceptions.send(
                    f"{datetime.datetime.now()} - link - {message.author.name} - Животное рекламирует хуету")
            elif len(str(message.content)) > 500 and message.author.id not in admins:  # Если больше 500 сим удаление
                await message.delete()
            elif (len(message.mentions) > 0 or len(message.role_mentions) > 0) and ping_ not in message.author.roles:
                cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {message.author.id}""")
                bd = cursor.fetchone()
                if bd[11] > 24:
                    temp_list = bd[1].split(",")
                    if '6' not in temp_list:
                        temp_list.append('6')
                    await message.author.send("Поздравляю ты получил достижение Связной и 3 Social Credit")
                    await message.author.add_roles(ping_)
                    cursor.execute(
                        f"""UPDATE dis_users SET credits = {bd[10] + 3} WHERE id_discord = {message.author.id}""")
                    cursor.execute(
                        f"""UPDATE dis_users SET role = {temp_list} WHERE id_discord = {message.author.id}""")
                    conn.commit()
                cursor.execute(
                    f"""UPDATE dis_users SET pings = {bd[11] + len(message.mentions) + len(message.role_mentions)} WHERE id_discord = {message.author.id}""")
                conn.commit()
            else:
                if not flag:
                    await timer_messages(5)
        elif message.author.id == 869217405862305822 or message.author.id == 597161042367348736:
            await client.process_commands(message)

    except Exception as exc:
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка Сообщение - {message.author.id} - {message.content} - {exc}")


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
async def exception_join(ctx, arg):
    try:
        user = await client.fetch_user(arg)
        await ctx.send(f"Участник {user.name} добавлен в исключения")
        exceptions_members.append(arg)
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
Время окончания буста:  {bd[6]}
Время захода: {bd[7]}
Время создания аккаунта: {user.created_at}
День рождения: {bd[8]}
Время в Пивнушке: {int(bd[9]) / 60} ч.
Число Social Credits: {bd[10]}""")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка - {exc}")
        

@client.command()
async def insert(ctx, arg):
    try:
        cursor.execute(f"""{arg}""")
        conn.commit()
        await ctx.send("Успешно")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


@client.command()
async def test(ctx):
    q = guild.get_role(962055146781679657)
    # w = guild.get_role(964985647305744446)
    # e = guild.get_role(958445794577514516)
    # r = guild.get_role(962055146781679657)
    # # t = guild.get_role(1009536415928942712)
    # y = guild.get_role(1015909584151523328)
    for member in guild.members:
        if q not in member.roles:
            await member.add_roles(q)
        # if w in member.roles:
        #     await member.remove_roles(w)
        # if e in member.roles:
        #     await member.remove_roles(e)
        # if r in member.roles:
        #     await member.remove_roles(r)
        # if y in member.roles:
        #     await member.remove_roles(y)
    await ctx.send("""OK""")
    pass


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
async def add_reaction(ctx, arg, arg2, arg3):
    try:
        # <:minecraftaccept:953387049950527488>
        #  реакция Канал сообщение
        # await ctx.send(f"1) {arg} 2) {arg2} 3) {arg3}")
        chann = await client.fetch_channel(arg2)
        message = await chann.fetch_message(arg3)
        await message.add_reaction(arg)
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")
    # await ctx.send(datetime.datetime.now())
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
    await ctx.send("Принял.")
    subprocess.run(["systemctl", "restart", "runscript.service"])


@client.command()
async def clear_all(ctx):

    for member in guild.members:
        if member.bot:
            continue
        try:
            if member.id not in admins:
                await member.kick()
                cursor.execute(f"""DELETE FROM dis_users WHERE id_discord = {member.id}""")
                conn.commit()
                await member.send(f'''Произошла чистка
    :arrow_right: {await general.create_invite(max_age=86400, max_uses=1)} :arrow_left:''')
            else:
                cursor.execute(f"""UPDATE dis_users SET role = '1' WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(f"""UPDATE dis_users SET num_mess = '1' WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(f"""UPDATE dis_users SET warnings = '0' WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(f"""UPDATE dis_users SET time_afk = '0' WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(f"""UPDATE dis_users SET time_end_boost = '0' WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(f"""UPDATE dis_users SET time_join = '08/09/2022, 00:00:00' WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(f"""UPDATE dis_users SET birthday = NULL WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(f"""UPDATE dis_users SET credits = '0' WHERE id_discord = {member.id}""")
                conn.commit()
                cursor.execute(f"""UPDATE dis_users SET pings = '0' WHERE id_discord = {member.id}""")
                conn.commit()
        except:
            pass

@client.command()
async def birthday(ctx, arg, arg2):
    try:
        struct_time = datetime.datetime.strptime(str(arg), "%d/%m")
        struct_time2 = struct_time.strftime('%d/%m')
        cursor.execute(
            f"""UPDATE dis_users SET birthday = "{struct_time2}" WHERE id_discord = {arg2}""")
        conn.commit()
        await ctx.send(f"Установлен день рождения у id - {arg2}, день - {struct_time.day} и месяц - {struct_time.month}")
    except Exception as exc:
        await ctx.send(f"Произошла ошибка {exc}")


async def send_text_small_money(reaction, member_reaction):
    await reaction.member.send(f'''**У Вас Не Достаточно Средств!**
Ваш Баланс : {int(member_reaction[10])} Social Credits и {int(member_reaction[3] / 60)} ч. и {int(member_reaction[2])} сообщ.
Чтобы их **Восполнить**, нужно **Зайти**...
:arrow_right: {await general.create_invite(max_age=1800, max_uses=1)} :arrow_left:

:gift_heart: **Приятной Вам Игры!** :cupid:''')


async def send_text_on_click_react_button(reaction):
    await reaction.member.send(
            '''Ты не устал **Жмакать **на **Кнопочку**?
Заебал, прекращай.''')


async def delete_vip_roles(reaction):
    for role in vip_roles:
            await reaction.member.remove_roles(role)


async def congr(reaction, role):
    await reaction.member.send(
                    f''':shopping_bags: **Поздравляю Тебя с Покупкой!** :shopping_bags:
Была куплена Роль - "{role.name}"
Данная роль имеется у **{len(role.members)}** чел.
:sparkling_heart: **Вы** всегда будете **Нашим** желанным **Покупателем!** :cupid:''')


async def add_boost(user, bd, num):
    global list_boost
    struct_time = datetime.datetime.now()
    struct_time += datetime.timedelta(days=1)
    str_time = struct_time.strftime('%d/%m/%Y, %H:%M:%S')
    list_boost[user.id] = struct_time

    if num == 2:
        await user.add_roles(X2)
        try:
            cursor.execute(f"""UPDATE dis_users SET time_end_boost 
                                = '{str_time}' WHERE id_discord = {user.id}""")
            print(str_time)
            cursor.execute(f"""UPDATE dis_users SET credits 
                                        = {int(bd[10]) - 6} WHERE id_discord = {user.id}""")
            conn.commit()
        except Exception as exc:
            print(exc)
    elif num == 4:
        await user.add_roles(X4)
        cursor.execute(f"""UPDATE dis_users SET time_end_boost 
                                        = '{struct_time}' WHERE id_discord = {user.id}""")
        cursor.execute(f"""UPDATE dis_users SET credits 
                                                = {int(bd[10]) - 10} WHERE id_discord = {user.id}""")
        conn.commit()


async def buying_vip(reaction, role, member_reaction, num):
    try:
        temp_list = member_reaction[1].split(",")
        """Добавление достижения"""
        if buy_vip_ not in reaction.member.roles:
            if '8' not in temp_list:
                await reaction.member.send("Поздравляю ты получил достижение Блатной и 5 Social Credit")
                temp_list.append('8')
                cursor.execute(f"""UPDATE dis_users SET role 
                            = '{','.join(temp_list)}' WHERE id_discord = {member_reaction[0]}""")
                conn.commit()
            await reaction.member.add_roles(buy_vip_)
        await delete_vip_roles(reaction)
        await congr(reaction, role)
        await reaction.member.add_roles(role)
        # if role == minor:
        #     id_role = 2
        # elif role == kozyrok:
        #     id_role = 3
        # elif role == churchill:
        #     id_role = 4
        if role == intellegence:
            try:
                temp_list.remove('3')
            except:
                pass
            temp_list.append('2')
        elif role == stalin:
            try:
                temp_list.remove('2')
            except:
                pass
            temp_list.append('3')

        cursor.execute(f"""UPDATE dis_users SET role 
                    = '{','.join(temp_list)}' WHERE id_discord = {member_reaction[0]}""")
        conn.commit()
        cursor.execute(f"""UPDATE dis_users SET credits 
                            = {member_reaction[10] - num} WHERE id_discord = {member_reaction[0]}""")
        conn.commit()
    except Exception as exc:
        print(exc)


async def check_buy_vip(reaction, role):
    try:
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {reaction.user_id}""")
        member_reaction = cursor.fetchone()

        if role in reaction.member.roles:
            await send_text_on_click_react_button(reaction)
        if birthday_role in reaction.member.roles:
            if role == intellegence and member_reaction[10] > 27.5:
                await buying_vip(reaction, role, member_reaction, 27.5)
            elif role == stalin and member_reaction[10] > 35:
                await buying_vip(reaction, role, member_reaction, 35)
            else:
                await send_text_small_money(reaction, member_reaction)
        # elif role == minor and member_reaction[3] > 15000:
        #     await minor_mess.remove_reaction("💵", reaction.member)
        #     await buying_vip(reaction, role, member_reaction)
        # elif role == kozyrok and member_reaction[3] > 18000:
        #     await kozyrok.remove_reaction("💵", reaction.member)
        #     await buying_vip(reaction, role, member_reaction)
        # elif role == churchill and member_reaction[3] > 18000:
        #     await churchill_mess.remove_reaction("💵", reaction.member)
        #     await buying_vip(reaction, role, member_reaction)

        else:
            if role == intellegence and member_reaction[10] > 55:
                print("buy")
                await buying_vip(reaction, role, member_reaction, 55)
            elif role == stalin and member_reaction[10] > 70:
                await buying_vip(reaction, role, member_reaction, 70)
            else:
                await send_text_small_money(reaction, member_reaction)
    except Exception as exc:
        print(exc)


async def check_main_roles(member_bd, member):  # Проверка на выдачу ролей
    try:
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
    except Exception as exc:
        print(exc)


def member_messenger(id):  # Подсчет сообщений
    global messages
    if id in messages:
        messages[id] = messages[id] + 1
    else:
        messages[id] = 1

    # print(messages)


async def antispam(k):  # Вызов предупреждения по спаму
    try:
        user = guild.get_member(k)
        if k in admins:
            return
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
        bd = cursor.fetchone()
        num = int(bd[4]) + 1
        cursor.execute(
            f"""UPDATE dis_users SET warnings = {num} WHERE id_discord = {k}""")
        conn.commit()
        # print(num)
        if get_warning_ not in user.roles:
            temp_list = bd[1].split(",")
            if '7' not in temp_list:
                temp_list.append('7')
            await user.send("Поздравляю ты получил достижение Плохиш и 5 Social Credit")
            await user.add_roles(get_warning_)
            cursor.execute(
                f"""UPDATE dis_users SET role = '{",".join(temp_list)}' WHERE id_discord = {user.id}""")
            cursor.execute(
                f"""UPDATE dis_users SET credits = {bd[10] + 5} WHERE id_discord = {user.id}""")
            conn.commit()

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
    except Exception as exc:
        user = guild.get_user(k)
        await exceptions.send(f"{datetime.datetime.now()} - Ошибка Антиспам - {user.name} - {exc}")


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
        cursor.execute(f"""SELECT * FROM dis_users WHERE id_discord = {k}""")
        num = cursor.fetchone()
        cursor.execute(
            f"""UPDATE dis_users SET time_afk = 0 WHERE id_discord = {k}"""
        )  # Обнуление счетчика афк
        cursor.execute(
            f"""UPDATE dis_users SET num_mess = {int(num[2]) + int(v)} WHERE id_discord = {k}"""
        )
        """Проверка на 666 сообщений"""
        if (int(num[2]) + int(v) > 665) and role_666_ not in user.roles:
            temp_list = num[1].split(",")
            if '4' not in temp_list:
                temp_list.append('4')
            await user.send("Поздравляю ты получил достижение Адский Строчила и 5 Social Credit")
            await user.add_roles(role_666_)
            cursor.execute(
                f"""UPDATE dis_users SET role = '{",".join(temp_list)}' WHERE id_discord = {user.id}""")
            cursor.execute(
                f"""UPDATE dis_users SET credits = {num[10] + 5} WHERE id_discord = {user.id}""")

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


async def check_and_move(reaction, channel):
    try:
        await reaction.member.move_to(channel)
        await check(channel)
    except:
        await reaction.member.send("Зайдите в любой голосовой канал")
        await check(channel)


def read_hours():
    try:
        with open("hours.txt", "r") as h:
            hours = h.read()
        return hours
    except Exception:
        init = ps.Parsing()
        init.loggining()
        init.parse_hours()
        with open("hours.txt", "r") as h:
            hours = h.read()
        return hours


def read_timetable():
    try:
        with open("timetable.txt", "r") as h:
            table = h.read()
        return table
    except Exception:
        init = ps.Parsing()
        init.loggining()
        init.parse_timetable()
        with open("timetable.txt", "r") as h:
            table = h.read()
        return table


def read_xl():
    try:
        os.remove("residue.txt")
    except Exception:
        pass
    hours = openpyxl.open("hours.xlsx", read_only=False, data_only=True)
    hours_list = hours.active
    residue = open("residue.txt","a")
    residue.write(f"\nЗа 1 семестр осталось:\n\n")
    all = 0
    for i in range(2, 17):

        subject_name = hours_list[f"A{i}"].value
        all_in_1 = hours_list[f"G{i}"].value
        passed_in_1 = hours_list[f"D{i}"].value
        subject_value = int(all_in_1) - int(passed_in_1)

        if int(subject_value) != 0:
            residue.write(f"{subject_name}:  {subject_value} ч. из {all_in_1}\n")
            all += subject_value

    residue.write(f"\nВсего осталось за 1 семестр {int(all)} ч.\n\n")

    residue.write(f"\nЗа 2 семестр осталось:\n\n")
    for i in range(2, 17):
        subject_name = hours_list[f"A{i}"].value
        all_in_2 = hours_list[f"H{i}"].value
        passed_in_2 = hours_list[f"E{i}"].value
        subject_value = int(all_in_2) - int(passed_in_2)

        if int(subject_value) != 0:
            residue.write(f"{subject_name}:  {subject_value} ч. из {all_in_2}\n")
            all += subject_value

    residue.write(f"\nВсего осталось за 2 семестр {int(all)} ч.\n\n")
    hours.close()
    residue.close()


if __name__ == '__main__':
    client.run("")
