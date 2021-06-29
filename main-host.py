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
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        if message.channel.name=="test-con-bot-cua-tung":
        #if message.channel.name=="ark":

            if message.content.startswith('?help'):
                help = ''
                price_string =          '*!price coin-1, coin-2*:             check price of coins\n'
                price_tlln_string =     '*!price tlln*:                       check price of tlln coin list\n'
                price_shitcoin_string = '*!price shitcoin*:                   check price of some fucking shitcoin\n'
                rate_string =           '*!rate number coin-1 = ? coin-2*:    check coin rate (Exp: !rate 10 neo = ? gas)\n'
                select_string =         '*!select xxx, yyy, zzz*:             select randomly\n'
                help = price_string + price_tlln_string + price_shitcoin_string + rate_string + select_string
                await message.channel.send(help)

            if message.content.startswith('!mk'):
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

            if message.content.startswith('!rate'):
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
                    await message.channel.send(string)
                    

            if message.content.startswith('!select'):
                content = message.content[5:]
                lst = content.split(',')
                response = random.choice(lst)
                await message.channel.send(response)

            if message.content.startswith('!price'):
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
                    string += item + ' = ' + str(price[item]['usd']) + ' usd\n'
                await message.channel.send(string)

            #if message.author == self.user:
            #    return

token = os.getenv("DISCORD_TOKEN")
client = MyClient()
client.run(token)

