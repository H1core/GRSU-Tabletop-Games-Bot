import telebot
from telebot import types
from telebot import telebot
import json
import os
from datetime import date

class User():
    def __init__(self,telegram_id = 0 , username = "" , name = "" , surname = ""):
        self.telegram_id = telegram_id
        self.username = username
        self.name = name
        self.surname = surname
    def __iter__(self):
        return iter((self.telegram_id,self.username,self.name,self.surname))
    def to_json(self):
        return self.__dict__
    def from_json(dct):
        return User(
            dct["telegram_id"],
            dct["username"],
            dct["name"],
            dct["surname"]
            )
class Post():
    def __init__(self , date_relise = date.today().strftime("%d/%m/%Y") , text = "" , is_team = False , team_list = [] , team_members = [] , member_list = [] , id = 0 , photo_id = ""):
        self.date_relise = date_relise
        self.text = text
        self.is_team = is_team
        self.team_list = team_list
        self.team_members = team_members
        self.member_list = member_list
        self.id = id
        self.photo_id = photo_id
    def to_json(self):
        return self.__dict__
    def from_json(dct):
        return Post(
            dct["date_relise"],
            dct["text"],
            dct["is_team"],
            dct["team_list"],
            dct["team_members"],
            dct["member_list"],
            dct["id"],
            dct["photo_id"]
            )

def check_symbols(word):
    word = word.lower()
    for i in word:
        if((i>='a' and i <='z')or(i>='а' and i<='я')):
            continue
        else:
           return False
    return True

lines = [] 
with open('bot_text.txt', encoding="utf8") as text:
   lines = text.readlines()



users = []
posts = []
try:
    with open('post_data_file.json' , 'r' , encoding="utf8") as read_file:
        data = read_file.read()
        posts = json.loads(data, object_hook=Post.from_json)
except:print("The post data is empty")
with open('users_data_file.json' , "r" , encoding ="utf8") as read_file:
    data = read_file.read()
    users = json.loads(data , object_hook=User.from_json)
admins = [
    491446220,
    899836650
]

welcome_text = '''\
Добро пожаловать, я тестовый бот 🌸.
Я здесь для организации настольных и интеллектуальных игр от университета ГРГУ им. Янки Купалы 📅
'''
register_text = '''\
Новым пользователям необходимо зарегистрироваться 👤
'''
regisration_text2 = '''\
Чтобы провести регистрацию напишите своё имя и фамилию.
Для ввода доступны только русские и латинские символы❗️
'''
successful_registrataion = '''\
Вы успешно зарегистрировались✅✅✅
Eсли захотите поменять имя или фамилию, то повторите эту комманду, но с желаемыми данными
'''

register_button = [[types.InlineKeyboardButton("Регистрация 📊",callback_data = "register")]]

keyboard_butoon_for_post = [["Событие с командами👥"] , ["Событие без команд👤"]]
post_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True , one_time_keyboard= True)
post_reply_markup.keyboard = keyboard_butoon_for_post
reply_markup = types.InlineKeyboardMarkup(register_button)
bot = telebot.TeleBot("******", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN


def get_message_inline_keyboard(CurrentPost = Post()):
    post_id = CurrentPost.id
    join_team_reply_markup = types.InlineKeyboardMarkup()
    for i,team in enumerate(CurrentPost.team_list):
        join_team_reply_markup.add(
            types.InlineKeyboardButton(
            str(team),
            callback_data="teamlist%"+str(post_id)+"%"+str(i)
            ),
            types.InlineKeyboardButton(
                
                "👤" +str(len(CurrentPost.team_members[i])),
                callback_data="teamlist%"+str(post_id)+"%"+str(i)
            )
        )
    return join_team_reply_markup


posts_inline_keyboards = {}
for post in posts:
    join_team_reply_markup = get_message_inline_keyboard(post)
    posts_inline_keyboards[post.id] = join_team_reply_markup






def search_free_id():
    lst = []
    for j in posts:
        lst.append(j.id)
    i = 1
    while(True):
        if(i not in lst):
            break
        i+=1
    return i

def get_user_name(user_id):
    for user in users:
        if(user.telegram_id == user_id):
            return (user.name , user.surname)

join_command_text = "Присоединиться к команде"
create_command_text = "Создать команду"
member_text = "Участвовать"


def make_post(post , chat_id):
    if(post.is_team == True):
        join_reply_markup = types.InlineKeyboardMarkup()
        join_reply_markup.add(
            types.InlineKeyboardButton(
                join_command_text,
                callback_data="join_" + str(post.id)
                ),
            types.InlineKeyboardButton(
                create_command_text,
                callback_data="create_" + str(post.id)
                ),
        )
        if(post.photo_id == "-1"):
            bot.send_message(chat_id , text = post.text , reply_markup = join_reply_markup)
        else:
            try:
                bot.send_photo(chat_id , photo = post.photo_id , reply_markup = join_reply_markup , caption = post.text)
            except:
                pass

    else:
        join_reply_markup = types.InlineKeyboardMarkup()
        join_reply_markup.add(
            types.InlineKeyboardButton(
                    member_text,
                    callback_data="wjoin_"+str(post.id)
                )
            )
        if(post.photo_id =="-1"):
            bot.send_message(chat_id , text = post.text , reply_markup = join_reply_markup)
        else:
            bot.send_photo(chat_id , photo = post.photo_id , reply_markup = join_reply_markup , caption = post.text)
def delete_post(post_id):
    for post in posts:
        if(post.id == post_id):
            posts.remove(post)
            serialize_post_data()
            return True
    return False
@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, welcome_text)
    if(message.chat.type == 'private'):
        ID = int(message.from_user.id)
        flag = False
        for user in users:
            if ID in user:
                flag = True
                break
        
        bot.send_message(message.chat.id,register_text , reply_markup = reply_markup)

        if(flag == False):
            users.append(User(ID,message.from_user.first_name , "empty" , "empty"))
            serialize_user_data()

#Админский блок

text_make_post = '''Сделать пост/объявление 📌✅🔈'''
text_delete_post = '''Удалить пост/объявление ❌'''
text_get_users = '''Получить список участников 👥'''

def check_for_admin(id):
    return (id in admins)
def get_admins_reply_buttons():
    keyboard_button = [[text_make_post]]
    admin_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard = True)
    admin_reply_markup.keyboard = [[text_make_post],[text_delete_post],[text_get_users]]
    return admin_reply_markup
@bot.message_handler(commands = ['admin'])
def check_for_admincommand(message):
    if(check_for_admin(int(message.from_user.id)) == True):
        

        message = bot.send_message(message.chat.id,"Вы успешно вошли в режим администратора" , reply_markup = get_admins_reply_buttons())
        bot.register_next_step_handler(message, admin_commands)
    else: 
        bot.reply_to(message,"У вас нет доступа к этой команде")

def admin_commands(message):
    if(message.text == text_make_post):    
        msg = bot.send_message(message.chat.id, "Выберите тип объявления/поста:" , reply_markup = post_reply_markup)
        bot.register_next_step_handler(msg , making_post_2)
    elif(message.text == text_delete_post):
        bot.send_message(message.chat.id, "Список всех постов, которые можно удалить:" , reply_markup = create_buttons_post_list())

def create_buttons_post_list():
    reply_buttons = types.InlineKeyboardMarkup()
    for post in posts:
        reply_buttons.add(
            types.InlineKeyboardButton(
                "Пост с номером ID:" + str(post.id),
                callback_data= "admnPostList" + str(post.id)
                )
            )
    return reply_buttons


@bot.callback_query_handler(func =lambda call: call.data.startswith("admn"))
def admin_buttons_pressed(call):
    user_id = int(call.message.chat.id)
    if(call.data.startswith("admnPostList")):
        post_id = int(call.data[12:])
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(
            types.InlineKeyboardButton
            (
                "Удалить пост",
                callback_data = "admnDelPost"+str(post_id)
            )
        ).add(
            types.InlineKeyboardButton(
                "Отмена",
                callback_data= "admnCancel"
                )
        )
        bot.edit_message_text(chat_id = user_id , message_id = call.message.id , text =get_post(post_id).text , reply_markup = reply_markup)
    elif(call.data.startswith("admnDelPost")):
        post_id = int(call.data[11:])
        if(delete_post(post_id)):
            bot.send_message(call.message.chat.id , "Объявление было успешно удалено")
        else:
            bot.send_message(call.message.chat.id , "Объявление уже не существует")
    elif(call.data.startswith("admnCancel")):
       bot.edit_message_text(chat_id = user_id , message_id = call.message.id, text = "Список всех постов, которые можно удалить:" , reply_markup = create_buttons_post_list())



def making_post_2(message):
    
    
    command = False
    if(message.text == "Событие без команд👤"):
        command = False
    elif(message.text == "Событие с командами👥"):
        command = True
    else:
        msg = bot.reply_to(message, "Выбран неверный тип , создание поста отменяется")
        return
    msg = bot.send_message(message.chat.id , "Напишите текст объявления:")
    bot.register_next_step_handler(msg , making_post_2_3 , command)
    
    '''  try:
        text = message.text
        send_message_all_users(text)
    except: print("ERROR")
    '''
def making_post_2_3(message, command = False):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True , one_time_keyboard= True)
    reply_markup.keyboard = [["Добавить фотографию📷"],["Не добавлять фотографию"]]
    msg = bot.send_message(message.chat.id, "Выберите опцию для фотографии:" , reply_markup = reply_markup)
    bot.register_next_step_handler(msg, making_post_2_4,message.text , command)
def making_post_2_4(message, post_text, command = False):
    if(message.text == "Добавить фотографию📷"):
        msg = bot.send_message(message.chat.id,"Отправьте фотографию:")
        bot.register_next_step_handler(msg, making_post_2_5,post_text, command)
    elif(message.text == "Не добавлять фотографию"):
        making_post_3(message,post_text,"-1",command)
    else:
        pass
def making_post_2_5(message,post_text,command):
    if(message.photo):
       bot.send_message(message.chat.id,  "Фото было успешно добавлено")
       making_post_3(message,post_text, message.photo[1].file_id , command)
    else:
        pass
def making_post_3(message , post_text , file_id , command = False ):
    msg = bot.send_message(message.chat.id, "Напишите идентификационный номер оъявления ID:")
    bot.register_next_step_handler(msg, making_post_4 , command , post_text , file_id)
def making_post_4(message, command , text , file_id):
    
    if(len(list(filter(lambda o: o>='0' and o<='9',message.text))) == len(message.text)):
        new_post = Post(date.today().strftime("%d/%m/%Y") , text , command , [] , [] , [], int(message.text) , file_id)
        posts.append(new_post)
        send_message_all_users(posts[-1])
        serialize_post_data()
    else:
        msg = bot.send_message(message.chat.id , "Идентификационный номер должен содержать только цифры и длинной не более 12 символов, введите его ещё раз:")
        bot.register_next_step_handler(msg,making_post_4,command , text)
def send_message_all_users(post):
    for user in users:
        make_post(post , user.telegram_id)

def get_message(message):
    s = message.text.split()
    if(len(s)!=2):
        bot.reply_to(message,"Неверный ввод ❌❌❌" + "\n" + "Ввести нужно два слова: имя и фамилию❗️")
    else:
        name , surname = s[0] , s[1]
        f1, f2 = check_symbols(name) ,check_symbols(surname)
        if(f1 and f2) == False: 
            bot.reply_to(message,"Неверный ввод❌❌❌" + "\n" + regisration_text2)
        else:
            for user in users:
                if(user.telegram_id == message.from_user.id):
                    user.name = name
                    user.surname = surname
                    break
            serialize_user_data()
            bot.reply_to(message,successful_registrataion)
            for i in posts:
                make_post(i,message.from_user.id)

@bot.message_handler(commands = ['registration'])
def regisration(message):
    msg = bot.send_message(message.chat.id, regisration_text2)
    bot.register_next_step_handler(msg , get_message)


def add_user_to_team(user_id , post_id , team_id):
    for post in posts:
        if(post.id == post_id):
            if(user_id not in post.team_members[team_id]):
                post.team_members[team_id].append(user_id)
                post.member_list.append(user_id)
    serialize_post_data()

def change_user_team(user_id,post_id,team_id = -1):
    current_post = get_post(post_id)
    for i,member in enumerate(current_post.team_members):
        if(user_id in member):
            if(i == team_id):
                return False
            member.remove(user_id)
            posts_inline_keyboards[post_id].keyboard[i][1].text =  "👤" + str(len(member))
            break
    if(team_id == -1):
        return 
    current_post.team_members[team_id].append(user_id)
    posts_inline_keyboards[post_id].keyboard[team_id][1].text = "👤" +str(len(current_post.team_members[team_id]))
    serialize_post_data()
    return True
    
    #join_team_reply_markup.keyboard[1][0]
    #if(len(member) == 0): сделать патом)
   
def add_team(team_name , post_id , user_id , ):
    for post in posts:
        if(post.id == post_id):
            if(team_name not in post.team_list):
                post.team_list.append(team_name)
                post.team_members.append([user_id])
                post.member_list.append(user_id)

                lenght = len(post.team_list) - 1
                posts_inline_keyboards[post_id].add(
                     types.InlineKeyboardButton(
                        str(team_name),
                        callback_data="teamlist%"+str(post_id)+"%"+str(lenght)
                    ),
                    types.InlineKeyboardButton(
                    "👤" +str(1),
                    callback_data="teamlist%"+str(post_id)+"%"+str(lenght)
                    )
                )
                change_user_team(user_id, post_id)
                return True
            else:
                return False

def create_team(message , post_id):
    if(add_team(message.text, post_id , int(message.chat.id))):
        bot.reply_to(message , "Команда была успешно создана✅👥📌")
        serialize_post_data()
    else:
        msg = bot.reply_to(message, "Команда с таким название уже есть, введите другое название:")
        bot.register_next_step_handler(msg, create_team, post_id)
def get_post(post_id):
    for post in posts:
        if(post.id == int(post_id)):
            return post

@bot.callback_query_handler(func =lambda call: not call.data.startswith("admn"))
def callback_inline(call):
    user_id = int(call.message.chat.id)

    if(call.data == "register"):
        msg = bot.send_message(call.message.chat.id, regisration_text2)
        bot.register_next_step_handler(msg , get_message)

    elif(call.data.startswith("join_")):
        post_id = int(call.data[5:])
        
        if(post_id not in posts_inline_keyboards.keys()):
            join_team_reply_markup = get_message_inline_keyboard(get_post(post_id))
            posts_inline_keyboards[post_id] = join_team_reply_markup
        
        bot.reply_to(call.message, "Список зарегистрированных команд:" , reply_markup = posts_inline_keyboards[post_id])
    elif(call.data.startswith("back")):
        post_id = int(call.data[4:])
        try:
            bot.edit_message_text(chat_id = user_id,  message_id = call.message.id , text = "Список зарегистрированных команд:" , reply_markup = posts_inline_keyboards[post_id])
        except:
            pass
    elif(call.data.startswith("create_")):
        post_id = int(call.data[7:])
        CurrentPost = get_post(post_id)

        if(post_id not in posts_inline_keyboards.keys()):
            join_team_reply_markup = get_message_inline_keyboard(CurrentPost)
            posts_inline_keyboards[post_id] = join_team_reply_markup
        
        msg = bot.reply_to(call.message , "Напишите название команды:")
        bot.register_next_step_handler(msg , create_team , post_id)
    elif(call.data.startswith("wjoin_")):
        post_id = int(call.data[6:])
        try:
            CurrentPost = get_post(int(post_id))
            CurrentPost.member_list.append(user_id)
            bot.reply_to(call.message , "Вы успешно записаны✅")
            serialize_post_data()
        except:
            bot.reply_to(call.message, "Это объявление больше не существует")
    elif(call.data.startswith("add_to_team%")):
        post_id , team_id = call.data[12:].split("%")
        if(change_user_team(user_id , int(post_id) , int(team_id)) == False):
            return

        #Поменяй потом
        CurrentPost = get_post(int(post_id))
        message_text = "Список членов этой команды:" + '\n\n'
        for member in CurrentPost.team_members[int(team_id)]:
            message_text +="👤" + ' '.join(get_user_name(member)) + '\n\n'
        keyboard_reply_markup = types.InlineKeyboardMarkup()
        keyboard_reply_markup.add(
                types.InlineKeyboardButton(
                    "Присоединиться",
                    callback_data="add_to_team%"+post_id+"%"+team_id
                    )).add(
                types.InlineKeyboardButton(
                    "Назад",
                    callback_data="back"+post_id
                    )
        )
        #Вот это A
        #        |
        
        bot.edit_message_text(chat_id = user_id , message_id = call.message.id , text =message_text , reply_markup = keyboard_reply_markup)
    elif(call.data.startswith("teamlist%")):
        post_id , team_id = call.data[9:].split("%")
        CurrentPost = get_post(int(post_id))
        
        if(post_id not in posts_inline_keyboards.keys()):
            join_team_reply_markup = get_message_inline_keyboard(CurrentPost)
            posts_inline_keyboards[post_id] = join_team_reply_markup
        
        message_text = "Список членов этой команды:" + '\n\n'
        for member in CurrentPost.team_members[int(team_id)]:
            message_text +="👤" + ' '.join(get_user_name(member)) + '\n\n'
        
        keyboard_reply_markup = types.InlineKeyboardMarkup()
        keyboard_reply_markup.add(
                types.InlineKeyboardButton(
                    "Присоединиться к этой команде",
                    callback_data="add_to_team%"+post_id+"%"+team_id
                    )).add(
                types.InlineKeyboardButton(
                    "Назад",
                    callback_data="back"+post_id
                    )
        )
        try:
            bot.edit_message_text(chat_id = user_id,  message_id = call.message.id , text = message_text , reply_markup = keyboard_reply_markup)
        except:
            pass
    elif(call.data[0:12] == "add_to_team%"):
        post_id , team_id = call.data[12:].split("%")
        change_user_team(user_id, int(post_id) , int(team_id))
        bot.edit_message_reply_markup(chat_id = user_id,message_id = call.message.id, reply_markup = posts_inline_keyboards[int(post_id)] )
    
def serialize_post_data():
    with open('post_data_file.json' , 'w' , encoding="utf8") as write_file:
        json.dump(posts, write_file , default = lambda o : o.to_json() , indent = 4)
def serialize_user_data():
    with open('users_data_file.json' , 'w' , encoding="utf8") as write_file:
        json.dump(users, write_file , default = lambda o : o.to_json() , indent = 4)

@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = os.path.dirname(os.path.abspath(__file__))+message.photo[1].file_id
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Фото добавлено")
    print(message.photo[-1].file_id)
    bot.send_photo(chat_id = message.chat.id , photo = message.photo[-1].file_id, caption = "TESTSTSTSTS")

bot.infinity_polling()

"""
            ОБЯЗАТЕЛЬНЫЙ ПЛАН
Сделать ограничения на вводимое имя,фамилию
Сделать ограничения на вводимое название команды
Расставить везде try|except
Добавить команду delete_post
Добавить команду 
Автоматически удалять все команды, где ноль человек
"""