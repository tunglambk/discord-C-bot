import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# import nltk 
# nltk.download('punkt')

# from nltk import word_tokenize,sent_tokenize

# from nltk.stem.lancaster import LancasterStemmer
# stemmer = LancasterStemmer()

# import numpy as np 
# import tflearn
# import tensorflow as tf
import random
#import json
#import pickle
import os
from tho import tho
from nofap import nofap
from truyencuoi import truyencuoi
from facepplib import FacePP
import time
import requests
from tinydb import TinyDB, Query

# if os.path.isfile("data.pickle"):
#     os.remove("data.pickle")

# with open("intents.json") as file:
#     data = json.load(file)

# try:
#     with open("data.pickle","rb") as f:
#         words, labels, training, output = pickle.load(f)

# except:
#     words = []
#     labels = []
#     docs_x = []
#     docs_y = []
#     for intent in data["intents"]:
#         for pattern in intent["patterns"]:
#             wrds = nltk.word_tokenize(pattern)
#             words.extend(wrds)
#             docs_x.append(wrds)
#             docs_y.append(intent["tag"])
            
#         if intent["tag"] not in labels:
#             labels.append(intent["tag"])


#     words = [stemmer.stem(w.lower()) for w in words if w != "?"]
#     words = sorted(list(set(words)))
#     labels = sorted(labels)

#     training = []
#     output = []
#     out_empty = [0 for _ in range(len(labels))]

#     for x, doc in enumerate(docs_x):
#         bag = []

#         wrds = [stemmer.stem(w.lower()) for w in doc]

#         for w in words:
#             if w in wrds:
#                bag.append(1)
#             else:
#               bag.append(0)
    
#         output_row = out_empty[:]
#         output_row[labels.index(docs_y[x])] = 1
        
#         training.append(bag)
#         output.append(output_row)

#     training = np.array(training)
#     output = np.array(output)
    
#     with open("data.pickle","wb") as f:
#         pickle.dump((words, labels, training, output), f)



# net = tflearn.input_data(shape=[None, len(training[0])])
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
# net = tflearn.regression(net)

# model = tflearn.DNN(net)
# model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
# model.save("model.tflearn")

# try:
#     model.load("model.tflearn")
# except:
#     model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
#     model.save("model.tflearn")


# def bag_of_words(s, words):
#     bag = [0 for _ in range(len(words))]

#     s_words = nltk.word_tokenize(s)
#     s_words = [stemmer.stem(word.lower()) for word in s_words]

#     for se in s_words:
#         for i, w in enumerate(words):
#             if w == se:
#                 bag[i] = 1
    
#     return np.array(bag)


import discord
import random
from pycoingecko import CoinGeckoAPI
import os

cg = CoinGeckoAPI()
coin_sp_lst = cg.get_coins_list()
coin_sp_names = []
coin_sp_symbols = []

for item in coin_sp_lst:
    coin_sp_names.append(item['id'])
    coin_sp_symbols.append(item['symbol'])

coin_dict = {coin_sp_symbols[i]: coin_sp_names[i] for i in range(len(coin_sp_symbols))}

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def talk(api_url, content):
    api_url = requests.get(api_url.format(content))
    load_api = api_url.json()
    sim_api = load_api['success']

    if not sim_api:
        response = "> Dồi sao?"
    elif str(sim_api) == "":
        response = "> Nhạt"
    else:
        response = '> ' + f"{sim_api}"
    return response

class MyClient(discord.Client):

    def __init__(self):
        super().__init__()
        self.start_face_detect = time.time() - 30
        self.enable_bot = True
        self.enable_casau = False
        self.enable_satoshi = False
        self.enable_soap = True

        self.ga_swith = False
        self.db_top_ga = TinyDB('db_top_ga.json')
        self.db_top_rain = TinyDB('db_top_rain.json')
        self.db_top_rich_ga = TinyDB('db_top_rich_ga.json')
        self.db_top_rich_rain = TinyDB('db_top_rich_rain.json')
        self.db_total = TinyDB('db_total.json')
        self.query = Query()

        all_db_top_ga = self.db_top_ga.all()
        all_db_top_rain = self.db_top_rain.all()
        all_db_top_rich_ga = self.db_top_rich_ga.all()
        all_db_top_rich_rain = self.db_top_rich_rain.all()
        all_db_total = self.db_total.all()

        self.top_ga =  list()
        self.top_rain = list()
        self.top_rich_rain = list()
        self.top_rich_ga = list()

        if len(all_db_top_ga) > 0:
            for item in all_db_top_ga:
                self.top_ga.append([item['amount'], item['id'], item['name']])

        if len(all_db_top_rain) > 0:
            for item in all_db_top_rain:
                self.top_rain.append([item['amount'],  item['id'], item['name']])

        if len(all_db_top_rich_rain) > 0:
            for item in all_db_top_rich_rain:
                self.top_rich_rain.append([item['amount'],  item['id'], item['name']])

        if len(all_db_top_rich_ga) > 0:
            for item in all_db_top_rich_ga:
                self.top_rich_ga.append([item['amount'],  item['id'], item['name']])

        if len(all_db_total) == 0 :
            self.total_ga = 0
            self.total_rain = 0
            self.total_fee = 0
            self.db_total.insert({'name': 'total_ga', 'amount': 0})
            self.db_total.insert({'name': 'total_fee', 'amount': 0})
            self.db_total.insert({'name': 'total_rain', 'amount': 0})
        else:
            temp = self.db_total.search(self.query.name == 'total_ga')
            self.total_ga = temp[0]['amount']
            temp = self.db_total.search(self.query.name == 'total_rain')
            self.total_rain = temp[0]['amount']
            temp = self.db_total.search(self.query.name == 'total_fee')
            self.total_fee = temp[0]['amount']

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message_edit(self, before, after):

        if not isinstance(after.channel, discord.DMChannel):

            if after.guild.id == 769800684056215572 and str(after.author.id) == "546463922287411230":

                embeds = after.embeds
                for embed in embeds:
                    embed = embed.to_dict()
                    if 'The Giveaway of' in embed['title'] and 'has ended' in embed['title']:
                        description = embed['description']
                        description = description.split('**')
                        amount = round(float(description[3]), 2)

                        rich_person = embed['author']['name']

                        if 'all of you were too slow' in embed['fields'][0]['value']:
                            return

                        lucky_ids = embed['fields'][0]['value'].split(' ')
                        for i, item in enumerate(lucky_ids):
                            lucky_ids[i] = int(item[2:-1])
                        for id in lucky_ids:
                            is_new_user = True
                            profile = await self.fetch_user_profile(id)
                            display_name = profile.user.display_name

                            for i, item in enumerate(self.top_ga):
                                if id == item[1]:
                                    self.top_ga[i][0] += amount
                                    self.top_ga[i][2] = display_name
                                    self.db_top_ga.update({'amount': self.top_ga[i][0], 'name': display_name}, self.query.id == id)
                                    is_new_user = False
                                    break
                            if is_new_user:
                                new_user = [amount, id, display_name]
                                self.top_ga.append(new_user)
                                self.db_top_ga.insert({'name': display_name, 'amount': amount, 'id': id})

                        is_new_rich_person = True
                        for i, item in enumerate(self.top_rich_ga):
                            if rich_person == item[1]:
                                is_new_rich_person = False
                                self.top_rich_ga[i][0] += amount * len(lucky_ids)
                                self.db_top_rich_ga.update({'amount': self.top_rich_ga[i][0]}, self.query.name == rich_person)
                                break
                        if is_new_rich_person:
                            new_user = [amount * len(lucky_ids), rich_person]
                            self.top_rich_ga.append(new_user)
                            self.db_top_rich_ga.insert({'name': rich_person, 'amount': amount * len(lucky_ids)})

                        self.total_ga += amount * len(lucky_ids)
                        self.total_fee += 0.01 * len(lucky_ids)
                        self.db_total.update({'amount': self.total_ga}, self.query.name == 'total_ga')
                        self.db_total.update({'amount': self.total_fee}, self.query.name == 'total_fee')

                return



    async def on_message(self, message):

        if not isinstance(message.channel, discord.DMChannel):

            if message.guild.id==769800684056215572  and str(message.author.id) == "546463922287411230":

                if self.ga_swith:
                    await message.add_reaction("💰")

                embeds = message.embeds # return list of embeds
                for embed in embeds:
                    embed = embed.to_dict()
                    if 'made it rain' in embed['title']:
                        description = embed['description']
                        description = description.split('**')
                        amount = round(float(description[3]), 2)

                        title = embed['title']
                        title = title.split('**')
                        rich_person = title[1]

                        lucky_ids = embed['fields'][0]['value'].split(' ')
                        for i, item in enumerate(lucky_ids):
                            lucky_ids[i] = int(item[2:-1])

                        for id in lucky_ids:
                            is_new_user = True
                            profile = await self.fetch_user_profile(id)
                            display_name = profile.user.display_name

                            for i, item in enumerate(self.top_rain):
                                if id == item[1]:
                                    self.top_rain[i][0] += amount
                                    self.top_rain[i][2] = display_name
                                    is_new_user = False
                                    self.db_top_rain.update({'amount': self.top_rain[i][0], 'name': display_name}, self.query.id == id)
                                    break
                            if is_new_user:
                                new_user = [amount, id, display_name]
                                self.top_rain.append(new_user)
                                self.db_top_rain.insert({'name': display_name, 'amount': amount, 'id': id})

                        is_new_rich_person = True
                        for i, item in enumerate(self.top_rich_rain):
                            if rich_person == item[1]:
                                is_new_rich_person = False
                                self.top_rich_rain[i][0] += amount * len(lucky_ids)
                                self.db_top_rich_rain.update({'amount': self.top_rich_rain[i][0]}, self.query.name == rich_person)
                                break
                        if is_new_rich_person:
                            new_user = [amount * len(lucky_ids), rich_person]
                            self.top_rich_rain.append(new_user)
                            self.db_top_rich_rain.insert({'name': rich_person, 'amount': amount * len(lucky_ids)})

                        self.total_rain += amount * len(lucky_ids)
                        self.total_fee += 0.01 * len(lucky_ids)
                        self.db_total.update({'amount': self.total_rain}, self.query.name == 'total_rain')
                        self.db_total.update({'amount': self.total_fee}, self.query.name == 'total_fee')
                return

            if message.guild.id==359221465842843648  and str(message.author.id) == "546463922287411230":
                await message.add_reaction("💰")
                return

            if str(message.channel.id) == "859030316524896267":
                if message.content.startswith('!bot'):
                    self.enable_bot = not self.enable_bot
                    if self.enable_bot:
                        response = '> Mở Bot'
                    else:
                        response = '> Tắt Bot'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!ga'):
                    self.ga_swith = not self.ga_swith
                    if self.ga_swith:
                        response = '> Mở tự nhặt GA'
                    else:
                        response = '> Tắt tự nhặt GA'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!casaudoi'):
                    self.enable_casau = not self.enable_casau
                    if self.enable_casau:
                        response = '> Bắt đầu thả cá sấu vào chat của dơi trong box ARK'
                    else:
                        response = '> Ngừng thả cá sấu vào chat của dơi trong box ARK'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!satoshimitoshi'):
                    self.enable_satoshi = not self.enable_satoshi
                    if self.enable_satoshi:
                        response = '> Bắt đầu thả emo vào chat của Mitoshi trong box ARK'
                    else:
                        response = '> Ngừng thả emo vào chat của Mitoshi trong box ARK'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!soap'):
                    self.enable_soap = not self.enable_soap
                    if self.enable_satoshi:
                        response = '> Bắt đầu thả emo soap vào chat có liên quan tới swap trong box ARK'
                    else:
                        response = '> Ngừng thả emo soap vào chat có liên quan tới swap trong box ARK'
                    await message.channel.send(response)
                    return


            if not self.enable_bot:
                return

            satoshi_channel = {814159783677526036, 829403779513974824, 776366209804926981}
            if message.channel.id in satoshi_channel:
                if 'satoshi' in message.content:
                    milosid = '<@776381590602514443>'
                    await message.channel.send(milosid)

            spam_channel = {829403779513974824, 814159783677526036, 859030316524896267, 813452767099355136}
            if message.channel.id in spam_channel:

                if message.content == '!total':
                    response = ''
                    response = response + '> Tổng lượng mưa: {:0.2f} ark\n'.format(self.total_rain)
                    response = response + '> Tổng lượng ark giveaway cứu đói: {:0.2f} ark\n'.format(self.total_ga)
                    response = response + '> Tổng phí đã cúng cho bot và mạng: {:0.2f} ark\n'.format(self.total_fee)
                    await message.channel.send(response)

                    return

                if message.content == '!topall':
                    self.top_rain.sort(reverse = True)
                    self.top_ga.sort(reverse = True)
                    self.top_rich_rain.sort(reverse = True)
                    self.top_rich_ga.sort(reverse = True)

                    response = '> Ông trùm hứng mưa:\n'
                    max_len = min(5, len(self.top_rain))
                    for i in range(max_len):
                        response = response + '> ' + str(i+1) + '. **' + self.top_rain[i][1] + '** - {:0.2f}'.format(self.top_rain[i][0]) + ' ark' + '\n'

                    response = response + '> \n'

                    response = response + '> Vua tay nhanh hơn não:\n'
                    max_len = min(5, len(self.top_ga))
                    for i in range(max_len):
                        response = response + '> ' + str(i+1) + '. **' + self.top_ga[i][1] + '** - {:0.2f}'.format(self.top_ga[i][0]) + ' ark' + '\n'

                    response = response + '> \n'

                    response = response + '> Hô phong hoán vũ:\n'
                    max_len = min(5, len(self.top_rich_rain))
                    for i in range(max_len):
                        response = response + '> ' + str(i+1) + '. **' + self.top_rich_rain[i][1] + '** - {:0.2f}'.format(self.top_rich_rain[i][0]) + ' ark' + '\n'

                    response = response + '> \n'

                    response = response + '> Thần tài đến thần tài đến hãy giang tay đón mời:\n'
                    max_len = min(5, len(self.top_rich_ga))
                    for i in range(max_len):
                        response = response + '> ' + str(i+1) + '. **' + self.top_rich_ga[i][1] + '** - {:0.2f}'.format(self.top_rich_ga[i][0]) + ' ark' + '\n'

                    await message.channel.send(response)
                    return

                if message.content == '!toprain':
                    self.top_rain.sort(reverse = True)
                    response = '> Ông trùm hứng mưa:\n'
                    max_len = min(5, len(self.top_rain))
                    for i in range(max_len):
                        response = response + '> ' + str(i+1) + '. **' + self.top_rain[i][1] + '** - {:0.2f}'.format(self.top_rain[i][0]) + ' ark' + '\n'
                    await message.channel.send(response)
                    return

                if message.content == '!topga':
                    self.top_ga.sort(reverse = True)
                    response = '> Vua tay nhanh hơn não:\n'
                    max_len = min(5, len(self.top_ga))
                    for i in range(max_len):
                        response = response + '> ' + str(i+1) + '. **' + self.top_ga[i][1] + '** - {:0.2f}'.format(self.top_ga[i][0]) + ' ark' + '\n'
                    await message.channel.send(response)
                    return

                if message.content == '!richrain':
                    self.top_rich_rain.sort(reverse = True)
                    response = '> Hô phong hoán vũ:\n'
                    max_len = min(5, len(self.top_rich_rain))
                    for i in range(max_len):
                        response = response + '> ' + str(i+1) + '. **' + self.top_rich_rain[i][1] + '** - {:0.2f}'.format(self.top_rich_rain[i][0]) + ' ark' + '\n'
                    await message.channel.send(response)
                    return


                if message.content == '!richga':
                    self.top_rich_ga.sort(reverse = True)
                    response = '> Thần tài đến thần tài đến hãy giang tay đón mời:\n'
                    max_len = min(5, len(self.top_rich_ga))
                    for i in range(max_len):
                        response = response + '> ' + str(i+1) + '. **' + self.top_rich_ga[i][1] + '** - {:0.2f}'.format(self.top_rich_ga[i][0]) + ' ark' + '\n'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!bocphot'):
                    for user in message.mentions:
                        id = user.id
                        print(id)
                        response = '> Đấu tố  **{}**\n'.format(user.display_name)
                        not_found = True
                        for item in self.top_ga:
                            if id == item[1]:
                                response += '> Giveaway đã lụm: **{:0.2f}** ark\n'.format(item[0])
                                not_found = False
                                break
                        if not_found:
                            response += '> Giveaway đã lụm: **0** ark\n'

                        not_found = True
                        for item in self.top_rain:
                            if id == item[1]:
                                response += '> Mưa đã hứng: **{:0.2f}** ark\n'.format(item[0])
                                not_found = False
                                break
                        if not_found:
                            response += '> Mưa đã hứng: **0** ark\n\n'
                        await message.channel.send(response)
                        return

                if message.content.startswith('!shisa'):
                    response = 'https://media.discordapp.net/attachments/859030316524896267/861580019696271360/image0.gif?width=1184&height=666'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!gaquay'):
                    response = 'https://images-ext-1.discordapp.net/external/ua0bSN8loX0fQVEJCRr_6ijzgJ3sNL7pEGUfYP0rpgk/https/media.discordapp.net/attachments/810900401347231764/868373100520173628/ga-disco2.gif'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!gaduday'):
                    response = 'https://images-ext-2.discordapp.net/external/uqy5_Jeezo5g0RpxAFhGXr8AC1MTYHI3nlY-kIBId6c/https/media.discordapp.net/attachments/829403779513974824/868427177165750272/du-day.gif'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!milosquay'):
                    response = 'https://media.discordapp.net/attachments/829403779513974824/868816750601469972/vanvui.gif'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!sex') or message.content.startswith('!sẽ'):
                    response = 'https://media.discordapp.net/attachments/859030316524896267/860911102082285608/unknown.png?width=1213&height=666'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!caumua'):
                    response = '> Ey, Bee’s sedie! Ey, elfgy! Ex ite? Zay Kay! Ail endemal , cure are est. Thee jew! Vie. Dubé Jew! Axe wife jeet.\n'
                    await message.channel.send(response)
                    response = '<a:rain:866595451968290826> <a:rain:866595451968290826> <a:rain:866595451968290826>'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!mottomua'):
                    response = '> Đảng Rain có Ngài đời đời ấm no.\n> Alarom talilgo vuvinai!'
                    await message.channel.send(response)
                    return


            if str(message.author.id) == '420943647647989785' and self.enable_casau and message.channel.id==829403779513974824:
                await message.add_reaction(":casau:815685082710409237")

            if str(message.author.id) == '776381590602514443' and self.enable_satoshi and message.channel.id==829403779513974824:
                await message.add_reaction("a:tenor_2:861069706371137537")
                await message.add_reaction(":Satoshi_Nakamoto:861071505802919936")

            if self.enable_soap and message.channel.id==829403779513974824:
                soap_keywords = ['soap', 'swap', 'xì quáp', 'xà bông', 'xà phòng']
                for keyword in soap_keywords:
                    if keyword in message.content:
                        await message.add_reaction(":PES3_Soap:783754543346221116")
                        await message.add_reaction("🧼")
                        return


            if str(message.author.id) == '403040446118363138':

                if "vừa tăng 5.00% trên sàn Binance" in message.content:
                    await message.add_reaction(":stonk:815120736980959244")
                    await message.add_reaction(":camap:805149996936462336")
                    await message.add_reaction(":rocket:815121319774519316")
                    await message.add_reaction("a:aPES_HappyClap:622096721408950295")
                elif "vừa giảm 5.00% trên sàn Binance" in message.content:
                    await message.add_reaction(":PES_NotStonks:800129909439725608")
                    await message.add_reaction(":beartrap:846853630933991505")
                    await message.add_reaction(":pray:814925096439119913")
                    await message.add_reaction("a:aPES_SadDance:849698896031776768")
                return

            if message.channel.id==814159783677526036:# or message.channel.name=="ark":

                ark = False
                if message.channel.id==829403779513974824:
                    ark = True

                if message.content.startswith('?help') and not ark:
                    help = ''

                    crypto_intro =          '> **CRYPTO**\n> \n'
                    price_string =          '> `!p coin-1, coin-2`: check price of coins\n'
                    price_tlln_string =     '> `!p tlln`: check price of tlln coin list\n'
                    rate_string =           '> `!rate number coin-1 = ? coin-2`: check coin rate (Exp: !rate 10 neo = ? gas)\n'
                    price_shitcoin_string = '> `!p shitcoin`: check price of some fucking shitcoin\n'

                    space = '> \n'

                    funny_intro =           '> **FUNNY**\n> \n'
                    talk_string =           '> `!talk abcxyz`: talk to me\n'
                    soi_string =            '> `!soi @mention-member-1, @mention-member-2`: show avatars\n'
                    face_string =           '> `!face @mention-member`: avatar face detection\n'
                    select_string =         '> `!select xxx, yyy, zzz`: select randomly\n'
                    tho_string =            '> `!tho`: trả về 1 đoạn thơ\n'
                    truyencuoi_string =     '> `!truyencuoi`: trả về 1 truyện cười\n'
                    fap_string =            '> `!fap` hoặc `!nofap`: show ảnh no fap\n'
                    se_string =             '> `!sex` or `!sẽ`: Xem sẽ (theo yêu cầu của dream)\n'
                    gaquay_string =         '> `!gaquay`: Gif gà quẩy party\n'
                    gaduday_string =        '> `!gaduday`: Gif gà đu dây\n'
                    milosquay_string =      '> `!milosquay`: Gif Milos quẩy party\n'
                    top_ga_string =         '> `!topga`: Xem top members nhận GA\n'
                    top_rain_string =       '> `!toprain`: Xem top members nhân rain\n'
                    top_rich_ga_string =    '> `!richga`: Xem top mạnh thường quân GA\n'
                    top_rich_rain_string =  '> `!richrain`: Xem top mạnh thường quân tạo rain\n'
                    top_all_string =        '> `!topall`: Xem tất cả top GA và rain\n'
                    bocphot_string =        '> `!bocphot @mention-member-1`: Soi GA và mưa đã nhận\n'
                    caumua_string =         '> `!caumua`: Thần chú cầu mưa\n'
                    mottomua_string =       '> `!mottomua`: Châm ngôn Đảng Mưa\n'
                    note_string =           '> Chức năng !face và !talk chỉ là funny nhé các feng'


                    help = crypto_intro + price_string + price_tlln_string + rate_string + price_shitcoin_string \
                            + space + funny_intro + talk_string + soi_string + face_string + select_string + tho_string + truyencuoi_string + fap_string \
                            + se_string + gaquay_string + gaduday_string + milosquay_string \
                            + space + top_ga_string + top_rain_string + top_rich_ga_string + top_rich_rain_string + top_all_string + caumua_string \
                            + bocphot_string + mottomua_string + space + note_string

                    await message.channel.send(help)
                    return

                if message.content.startswith('!tho'):
                    response = random.choice(tho)
                    await message.channel.send(response)
                    return

                if message.content.startswith('!truyencuoi'):
                    response = random.choice(truyencuoi)
                    message = await message.channel.send(response)
                    for emoji in (':vcl:837406003011649576', 'a:thisthis:837401903952429127', 'a:aPES4_HahaSex:726511347457720320'):
                        await message.add_reaction(emoji)
                    return

                if message.content.startswith('!face'):

                    current_time = time.time()
                    delta_time = current_time - self.start_face_detect

                    if delta_time >= 30:
                        self.start_face_detect = time.time()
                    else:
                        remain_time = 30 - delta_time
                        response = '> Tính năng này khả dụng trong ' + str(remain_time) + '(s) nữa'
                        await message.channel.send(response)
                        return

                    for user in message.mentions:
                        userAvatar = str(user.avatar_url)
                        userAvatar = userAvatar.replace('.webp', '.png').replace('.gif', '.png')

                        image = facepp.image.get(image_url=userAvatar,return_attributes=['gender', 'age', 'emotion', 'skinstatus', 'beauty'])

                        if image.face_num > 0:
                            age = '> Age: ' + str(image.faces[0].age['value']) + '\n'
                            gender = '> Gender: ' + str(image.faces[0].gender['value']) + '\n'
                            beauty_male = '> Beauty male score: ' + str(image.faces[0].beauty['male_score']) + '\n'
                            beauty_female = '> Beauty female score: ' + str(image.faces[0].beauty['female_score']) + '\n'
                            conclusion = '> This is just funny detection'
                            response = age + gender + beauty_male + beauty_female + conclusion
                        else:
                            response = '> Không tìm thấy khuôn mặt nào trong ảnh'

                        await message.channel.send(response)
                        return
                    return

                if message.content.startswith('!nofap') or message.content.startswith('!fap'):
                    response = random.choice(nofap)
                    await message.channel.send(response)
                    return

                if message.content.startswith('!soi'):
                    for user in message.mentions:
                        userAvatar = user.avatar_url
                        await message.channel.send(userAvatar)
                        return

                if message.content.startswith('!rate') and not ark:
                    content = message.content[5:].strip()
                    content_lst = content.split(' ')
                    if (content_lst[2] != '=') or (content_lst[3] != '?'):
                        return
                    if isfloat(content_lst[0]):
                        num_1 = float(content_lst[0])
                        if content_lst[1] in coin_sp_names:
                            price_1 = cg.get_price(ids=content_lst[1], vs_currencies='usd')
                        else:
                            if content_lst[1] in coin_sp_symbols:
                                coin = coin_dict[content_lst[1]]
                                price_1 = cg.get_price(ids=coin, vs_currencies='usd')
                            else:
                                return

                        if content_lst[4] in coin_sp_names:
                            price_2 = cg.get_price(ids=content_lst[4], vs_currencies='usd')
                        else:
                            if content_lst[4] in coin_sp_symbols:
                                coin = coin_dict[content_lst[4]]
                                price_2 = cg.get_price(ids=coin, vs_currencies='usd')
                            else:
                                return
                        price_1 =  float(list(price_1.values())[0]['usd'])
                        price_2 =  float(list(price_2.values())[0]['usd'])
                        rate = round(price_1/price_2 * num_1, 3)

                        string = str(num_1) + " " + content_lst[1] + ' = ' + str(rate) + ' ' + content_lst[4]
                        await message.channel.send('> '+string)
                        return


                if message.content.startswith('!select'):
                    content = message.content[5:]
                    lst = content.split(',')
                    response = random.choice(lst)
                    await message.channel.send('> '+response)
                    return

                if message.content.startswith('!price') and not ark:
                    response = '> Chuyển qua dùng !p, không dùng !price nữa nha feng'
                    await message.channel.send(response)
                    return

                if message.content.startswith('!p') and not ark:
                    coin = message.content[2:].strip()
                    if 'tlln' in coin:
                        coin = 'neo,gas,firo,dash,zen,ark'
                    elif 'shitcoin' in coin:
                        coin = 'doge,shib,cummies,xrp'
                    else:
                        coin = coin.replace(' ','')
                    coin_lst = coin.split(',')
                    coin_lst_name = []
                    for item in coin_lst:
                        if item not in coin_sp_names:
                            if item in coin_sp_symbols:
                                coin_lst_name.append(coin_dict[item])
                        if item in coin_sp_names:
                            coin_lst_name.append(coin_dict[item])
                    coin = ','.join(coin_lst_name)
                    price = cg.get_price(ids=coin, vs_currencies='usd')
                    string = ''
                    for item in price:
                        string += '> ' + item + ' = ' + str(price[item]['usd']) + ' usd\n'
                    await message.channel.send(string)
                    return

                if message.content.startswith('!talk') and not ark:
                    content = message.content[5:].strip()

                    response = talk('https://simsumi.herokuapp.com/api?text={}&lang=vi', content)

                    if 'Limit 50 queries' in response:
                        response = talk('https://api.simsimi.net/v1/?text={}&lang=vi_VN', content)

                    await message.channel.send(response)
                    return


                if message.author == self.user:
                    return


                if (message.content[0] == ':') and (message.content[-1] == ':'):
                    return

                if str(message.author.id) == '403040446118363138':

                    return


                # inp = message.content
                # result = model.predict([bag_of_words(inp, words)])[0]
                # result_index = np.argmax(result)
                # tag = labels[result_index]
                # print(result[result_index])
                # if result[result_index] > 0.925:
                #     for tg in data["intents"]:
                #         if tg['tag'] == tag:
                #             responses = tg['responses']

                #     bot_response=random.choice(responses)
                #     await message.channel.send('> ' + bot_response.format(message))


api_key_face = os.getenv("FACE_KEY")
api_secret_key_face = os.getenv("FACE_SECRET_KEY")
global facepp
facepp = FacePP(api_key=api_key_face, api_secret=api_secret_key_face)

token = os.getenv("DISCORD_TOKEN")
client = MyClient()
client.run(token)

