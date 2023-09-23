import json
import math
import requests


class YobitInfo:
    __URL_INFO = 'https://yobit.net/api/3/info'
    __URL_TICKER = 'https://yobit.net/api/3/ticker/'
    __MAIN_COIN = 'usdt'

    list_pair = []
    def get_pairs(self, name_coin=__MAIN_COIN):
        # btc_usdt сколько стоит btc в usdt
        res = requests.get(self.__URL_INFO)  # получаем данные info
        res_obj = json.loads(res.text)  # переводим полученный текст в объект с данными
        pairs = [pair for pair in res_obj['pairs'] if pair.startswith(name_coin + '_')]
        return pairs

    def get_price_pair(self, pair):
        try:
            ticker_res = requests.get(self.__URL_TICKER + pair)
            ticker_res_obj = json.loads(ticker_res.text)  # переводим полученный текст в объект с данными

            price_buy = '%0.8f' % ticker_res_obj[pair]['buy']
            price_sell = '%0.8f' % ticker_res_obj[pair]['sell']
            return {pair: {
                        'buy': price_buy,
                        'sell': price_sell
                    }}
        except KeyError as e:
            return {pair: {
                        'buy': 0,
                        'sell': 0
                    }}


    def get_price_all_pairs(self, name_coin=__MAIN_COIN):
        pairs = self.get_pairs(name_coin)
        self.list_pair.clear()
        for i in range(0, int(math.ceil(len(pairs) / 50))):
            part_pairs = pairs[i * 50:(i + 1) * 50]
            pairs_str = '-'.join(pairs[i * 50:(i + 1) * 50])
            ticker_res = requests.get(self.__URL_TICKER + pairs_str)
            ticker_res_obj = json.loads(ticker_res.text)
            price_all_pairs = []
            for pair in part_pairs:
                price_buy = '%0.8f' % ticker_res_obj[pair]['buy']
                price_sell = '%0.8f' % ticker_res_obj[pair]['sell']
                price_all_pairs.append({pair: {
                    'buy': price_buy,
                    'sell': price_sell
                }})
                self.list_pair.append(pair)

        return price_all_pairs

    def get_list_pair(self):
        return self.list_pair

