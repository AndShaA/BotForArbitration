from src.yobit import YobitInfo
from heapq import nlargest
import copy


def get_names_coins(pair: str):
    two_name_coin = pair.split('_')
    return two_name_coin


class BotLogic:
    __BALANCE = 100
    __FEE = 0.99
    yobit = YobitInfo()

    def search_best_trade(self):
        list_trade = []
        dict_all_pair = {}
        dict_best_pair = {}

        all_pairs = self.yobit.get_price_all_pairs()
        list_pair = self.yobit.get_list_pair()
        list_pair = copy.copy(list_pair)
        iter_pair = 0
        for pairs in all_pairs:
            name_pair = list_pair[iter_pair]
            start_trade = (float(pairs[name_pair]['sell']) * self.__BALANCE) * self.__FEE

            iter_pair += 1
            second_name = get_names_coins(name_pair)

            second_all_pairs = self.yobit.get_price_all_pairs(second_name[1])
            second_list_pair = self.yobit.get_list_pair()
            second_iter_pair = 0
            for second_pairs in second_all_pairs:
                second_name_pair = second_list_pair[second_iter_pair]
                intermediate_trade = (float(second_pairs[second_name_pair]['sell']) * start_trade) * self.__FEE

                second_iter_pair += 1
                last_name_pair_list = get_names_coins(second_name_pair)
                last_name_pair = last_name_pair_list[1] + '_' + 'usdt'

                last_price = self.yobit.get_price_pair(last_name_pair)
                finish_trade = (float(last_price[last_name_pair]['sell']) * intermediate_trade - 100) * self.__FEE

                if finish_trade < 0:
                    continue
                list_trade.append(finish_trade)
                dict_all_pair[finish_trade] = name_pair + ' -> ' + second_name_pair + ' -> ' + last_name_pair

        list_best_trade = nlargest(5, list_trade)
        list_best_trade.sort()

        for price in list_best_trade:
            dict_best_pair[dict_all_pair[price]] = round(price, 2)

        return dict_best_pair
