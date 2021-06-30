import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import nltk 
nltk.download('punkt')

from nltk import word_tokenize,sent_tokenize

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np 
import tflearn
import tensorflow as tf
import random
import json
import pickle
import os
from tho import tho
from nofap import nofap
from facepplib import FacePP
import time

if os.path.isfile("data.pickle"):
    os.remove("data.pickle")

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)



net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)


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

class MyClient(discord.Client):

    def __init__(self):
        super().__init__()
        self.start_face_detect = time.time()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        #if message.channel.name=="test-con-bot-cua-tung":
        if str(message.author.id) == '403040446118363138':
            return

        satoshi_channel = {"spam-bot", "ark", "spam-human"}
        if message.channel.name in satoshi_channel:
            if 'satoshi' in message.content:
                milosid = '<@776381590602514443>'
                await message.channel.send(milosid)

        if message.channel.name=="spam-bot":# or message.channel.name=="ark":

            ark = False
            if message.channel.name=="ark":
                ark = True

            if message.content.startswith('?help') and not ark:
                help = ''
                soi_string =            '> **!soi @mention-member-1, @mention-member-2: show avatars**\n'
                price_string =          '> **!price coin-1, coin-2**: check price of coins\n'
                price_tlln_string =     '> **!price tlln**: check price of tlln coin list\n'
                price_shitcoin_string = '> **!price shitcoin**: check price of some fucking shitcoin\n'
                rate_string =           '> **!rate number coin-1 = ? coin-2**: check coin rate (Exp: !rate 10 neo = ? gas)\n'
                select_string =         '> **!select xxx, yyy, zzz**: select randomly\n'
                soiguong_string =       '> **!xoa**: xoa đầu ếch\n'
                xoadau_string =         '> **!soi gương**: trả về ảnh soi gương\n'
                tho_string =            '> **!tho**: trả về 1 đoạn thơ\n'
                help = soi_string + price_string + price_tlln_string + price_shitcoin_string + rate_string \
                         + select_string + soiguong_string + xoadau_string + tho_string
                await message.channel.send(help)
                return

            if message.content.startswith('!tho'):
                response = random.choice(tho)
                await message.channel.send(response)
                return

            if message.content.startswith('!face'):

                current_time = time.time()
                delta_time = current_time - self.start_face_detect

                if delta_time >= 60:
                    self.start_face_detect = time.time()
                else:
                    remain_time = 60 - delta_time
                    response = '> Tính năng này khả dụng trong ' + str(remain_time) + '(s) nữa'
                    await message.channel.send(response)
                    return

                for user in message.mentions:
                    userAvatar = user.avatar_url

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

            if message.content.startswith('!mk') and not ark:
                content = message.content[3:].strip()
                if content in coin_sp_names:
                    coin = content
                else:
                    if content in coin_sp_symbols:
                        coin = coin_dict[content]
                    else:
                        return
                res = cg.get_coin_market_chart_by_id(coin, 'usd', 1)
                print(res)

            if message.content == '!soi gương':
                response = 'https://media.discordapp.net/attachments/829403779513974824/859350808524488714/unknown.png'
                await message.channel.send(response)
                return

            if message.content.startswith('!xoa'):
                response = 'https://media.discordapp.net/attachments/829403779513974824/859350641344249886/ech.gif'
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
                    print(price_1)
                    print(price_2)
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
                coin = message.content[6:].strip()
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
                print(coin_lst_name)
                coin = ','.join(coin_lst_name)
                price = cg.get_price(ids=coin, vs_currencies='usd')
                print(price)
                string = ''
                for item in price:
                    string += '> ' + item + ' = ' + str(price[item]['usd']) + ' usd\n'
                await message.channel.send(string)
                return

            if message.author == self.user:
                return


            if (message.content[0] == ':') and (message.content[-1] == ':'):
                return

            inp = message.content
            result = model.predict([bag_of_words(inp, words)])[0]
            result_index = np.argmax(result)
            tag = labels[result_index]
            print(result[result_index])
            if result[result_index] > 0.925:
                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']
            
                bot_response=random.choice(responses)
                await message.channel.send('> ' + bot_response.format(message))


api_key_face = os.getenv("FACE_KEY")
api_secret_key_face = os.getenv("FACE_SECRET_KEY")
global facepp
facepp = FacePP(api_key=api_key_face, api_secret=api_secret_key_face)

token = os.getenv("DISCORD_TOKEN")
client = MyClient()
client.run(token)

