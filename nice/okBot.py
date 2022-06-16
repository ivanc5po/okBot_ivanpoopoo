import json

import okx.Account_api as Account
import okx.Funding_api as Funding
import okx.Market_api as Market
import okx.Public_api as Public
import okx.Trade_api as Trade
import okx.status_api as Status
import okx.subAccount_api as SubAccount
import okx.TradingData_api as TradingData
import okx.Broker_api as Broker
import okx.Convert_api as Convert
import time
import os

start_time = time.time()

os.system("clear")

st = 0
flag = '0'

api_key = "XXXXXXXXX"
secret_key = "XXXXXXXXX"
passphrase = "XXXXXXXXX"
url = "XXXXXXXXXXXX"

tradingDataAPI = TradingData.TradingDataAPI(api_key, secret_key, passphrase, False, flag)
accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
convertAPI = Convert.ConvertAPI(api_key, secret_key, passphrase, False, flag)
marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, True, flag)
publicAPI = Public.PublicAPI(api_key, secret_key, passphrase, False, flag)
tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

m = 15
from PIL import Image
import numpy as np
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
option = Options()
option.add_argument("--headless")
option.add_argument("--window-size=500,500")
wd = webdriver.Firefox(options=option)
wd.get(url)

re = 0
bs = 0
bs2 = 0
st = 0
text = ""
mode = 0
buy_var = 0
sell_var = 0
mp = 0
time.sleep(3)

spread = 0.005

while True:
        try:
                coin = str(wd.title).split()[0].replace("USDT", "")+"-USDT-SWAP"
                price = float(str(wd.title).split()[1])
                total = float(str(fundingAPI.get_asset_valuation(ccy = 'USDT')).split(", ")[4].split("'")[3])-218263.75*int(flag)
                os.system("clear")
                print(text)
                print(price)
                wd.save_screenshot("screenshot.png")
                image = Image.open("screenshot.png")
                img = np.array(image)
                max_X = 0
                for i in img:
                        for r in range(len(i)):
                                j = i[r]
                                if 46 >= j[0] and 42 <= j[0] and 32 >= j[1] and 28 <= j[1] and 41 >= j[2] and 38 <= j[2] and r > max_X:
                                        max_X = r
                                        bs = 1
                                if 27 >= j[0] and 24 <= j[0] and 41 >= j[1] and 38 <= j[1] and 41 >= j[2] and 38 <= j[2] and r > max_X:
                                        max_X = r
                                        bs = 2
                if st == 0:
                        text += coin + "\n"
                        bs2 = bs
                        st = 1

                if not bs2 == bs:
                        if bs == 1:
                                sell_var += 1
                                buy_var = 0
                        elif bs == 2:
                                buy_var += 1
                                sell_var = 0

                if sell_var == 3:
                        r1 = tradeAPI.close_positions(coin, 'cross', posSide="long")
                        accountAPI.set_leverage(instId=coin, lever=str(m), mgnMode='cross')
                        result = tradeAPI.place_order(instId=coin, tdMode='cross', side='sell', ordType='market', sz=str(int(total*2)), posSide="short")
                        if "'code': '0'" in str(result):
                                text += "做空 "+str(price) + "\n"
                                bs2 = bs
                                sell_var = 0
                                mode = 1
                                mp = price
                if buy_var == 3:
                        r1 = tradeAPI.close_positions(coin, 'cross', posSide="short")
                        accountAPI.set_leverage(instId=coin, lever=str(m), mgnMode='cross')
                        result = tradeAPI.place_order(instId=coin, tdMode='cross', side='buy', ordType='market', sz=str(int(total*2)), posSide="long")
                        if "'code': '0'" in str(result):
                                text += "做多 "+str(price) + "\n"
                                bs2 = bs
                                buy_var = 0
                                mode = 2
                                mp = price

                re += 1
                if re == 30:
                    wd.refresh()
                    re = 0

                time.sleep(1)
        except:
                time.sleep(1)
                q = 0
