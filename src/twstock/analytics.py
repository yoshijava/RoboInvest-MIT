# -*- coding: utf-8 -*-

from statistics import stdev

class Analytics(object):

    def continuous(self, data):
        diff = [1 if data[-i] > data[-i - 1]
                else -1 for i in range(1, len(data))]
        cont = 0
        for v in diff:
            if v == diff[0]:
                cont += 1
            else:
                break
        return cont * diff[0]

    def moving_average(self, data, days):
        result = []
        data = data[:]
        for _ in range(len(data) - days + 1):
            result.append(round(sum(data[-days:]) / days, 2))
            data.pop()
        return result[::-1]

    def ma_bias_ratio(self, day1, day2):
        """Calculate moving average bias ratio"""
        data1 = self.moving_average(self.close, day1)
        data2 = self.moving_average(self.close, day2)
        result = [data1[-i] - data2[-i]
                  for i in range(1, min(len(data1), len(data2)) + 1)]

        return result[::-1]

    def ma_bias_ratio_pivot(self, data, sample_size=5, position=False):
        """Calculate pivot point"""
        sample = data[-sample_size:]

        if position is True:
            check_value = max(sample)
            pre_check_value = max(sample) > 0
        elif position is False:
            check_value = min(sample)
            pre_check_value = max(sample) < 0

        return ((sample_size - sample.index(check_value) < 4 and
                 sample.index(check_value) != sample_size - 1 and pre_check_value),
                sample_size - sample.index(check_value) - 1,
                check_value)


class WinnerRule(object):
    BEST_WHY_BUY = ['R1: [2] Vol[-1] > 3 * Vol[-1:-61]',
                    'R2: [2] Vol[-1] > 3 * Vol[-1:-31]',
                    'R3: [x/5] Pri[-1]/Pri[-2] >= x %',
                    'R4: [2] {5>10}MA && all MAs are up',
                    'R5: [2] {5>10>20}MA && all MAs are up',
                    'R6: [2] {5>10>20>60}MA && all MAs are up',
                    'R7: [2] {5/10/20}MA tangled(std<=1% Pri[-1]) & >=1% up',
                    'R8: [2] {5/10/20/60}MA tangled(std<=1% Pri[-1]) & >=1% up',
                    'R9: [2] Higher than upper shadow in last 20 days',
                    'R10: [2] lower shadow > 2 * kbarSize & is up',
                    'R11: ',
                    'R12: [2] RSI >= 80 for 2 days',
                    'R13: [2] price > 5MA for 3 days'
                    ]

    BEST_WHY_SELL = ['R1: [2] Vol[-1] > 3 * Vol[-1:-61]',
                     'R2: [2] Vol[-1] > 3 * Vol[-1:-31]',
                     'R3: [x/5] Pri[-2]/Pri[-1] >= x %',
                     'R4: [2] {5<10}MA && all MAs are down',
                     'R5: [2] {5<10<20}MA && all MAs are down',
                     'R6: [2] {5<10<20<60}MA && all MAs are down',
                     'R7: [2] {5/10/20}MA tangled(std<=1% Pri[-1]) & >=1% down',
                     'R8: [2] {5/10/20/60}MA tangled(std<=1% Pri[-1]) & >=1% down',
                     'R9: [2] Lower than lower shadow in last 20 days',
                     'R10: [2] upper shadow > 2 * kbarSize & is down)',
                     'R11: ',
                     'R12: [2] RSI <= 20 for 2 days',
                     'R13: [2] price < 5MA for 3 days'
                    ]


    def __init__(self, stock):
        self.stock = stock

    def bias_ratio(self, position=False):
        return self.stock.ma_bias_ratio_pivot(
            self.stock.ma_bias_ratio(1, 5),
            position=position)

    def plus_bias_ratio(self):
        return self.bias_ratio(True)

    def mins_bias_ratio(self):
        return self.bias_ratio(False)

    def winner_rule1(self):
        totalVolume = 0
        for idx in range(2, 61):
            totalVolume = totalVolume + self.stock.volume[-idx]

        avgVolume = totalVolume / 60
        # print("sid = ", self.stock.sid)
        # print("CurrPri = ", self.stock.close[-1])
        # print("CurrVol = ", self.stock.volume[-1])
        # print("30d avgVol = ", avgVolume)
        if self.stock.volume[-1] > avgVolume * 3:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule2(self):
        totalVolume = 0
        for idx in range(2, 31):
            totalVolume = totalVolume + self.stock.volume[-idx]

        avgVolume = totalVolume / 30
        # print("sid = ", self.stock.sid)
        # print("CurrPri = ", self.stock.close[-1])
        # print("CurrVol = ", self.stock.volume[-1])
        # print("30d avgVol = ", avgVolume)
        if self.stock.volume[-1] > avgVolume * 3:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule3(self):
        # print("sid", self.stock.sid)
        # print("TodayPri = ", self.stock.close[-1])
        # print("YesterdayPri = ", self.stock.close[-2])
        # print("Ratio = ", self.stock.close[-1] / self.stock.close[-2])
        score = (self.stock.close[-1] / self.stock.close[-2] - 1) * 100
        if score >= 1:
            return [True, score/5, 10/5]
        else:
            return [False, 0, 2]

    def winner_rule3_neg(self):
        score = (self.stock.close[-2] / self.stock.close[-1] - 1) * 100
        if score >= 1:
            return [True, score/5, 10/5]
        else:
            return [False, 0, 2]

    def winner_rule4(self):
        if (self.stock.moving_average(self.stock.close, 5)[-1] > self.stock.moving_average(self.stock.close, 10)[-1] and \
            self.stock.moving_average(self.stock.close, 5)[-1] / self.stock.moving_average(self.stock.close, 5)[-2] >= 1.01 and \
            self.stock.moving_average(self.stock.close, 10)[-1] / self.stock.moving_average(self.stock.close, 10)[-2] >= 1.01):
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule4_neg(self):
        if (self.stock.moving_average(self.stock.close, 5)[-1] < self.stock.moving_average(self.stock.close, 10)[-1] and
            self.stock.moving_average(self.stock.close, 5)[-2] / self.stock.moving_average(self.stock.close, 5)[-1] >= 1.01 and
                self.stock.moving_average(self.stock.close, 10)[-2] / self.stock.moving_average(self.stock.close, 10)[-1] >= 1.01):
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule5(self):
        if (self.winner_rule4()[0] == True and \
            self.stock.moving_average(self.stock.close, 10)[-1] > self.stock.moving_average(self.stock.close, 20)[-1] and \
            self.stock.moving_average(self.stock.close, 10)[-1] / self.stock.moving_average(self.stock.close, 10)[-2] >= 1.01 and \
            self.stock.moving_average(self.stock.close, 20)[-1] / self.stock.moving_average(self.stock.close, 20)[-2] >= 1.01):
            return [True, 2, 2]
        else:
            return [False, 0, 2]
    
    def winner_rule5_neg(self):
        if (self.winner_rule4_neg()[0] == True and \
            self.stock.moving_average(self.stock.close, 10)[-1] < self.stock.moving_average(self.stock.close, 20)[-1] and \
            self.stock.moving_average(self.stock.close, 10)[-2] / self.stock.moving_average(self.stock.close, 10)[-1] >= 1.01 and \
            self.stock.moving_average(self.stock.close, 20)[-2] / self.stock.moving_average(self.stock.close, 20)[-1] >= 1.01):
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule6(self):
        if (self.winner_rule4()[0] == True and self.winner_rule5()[0] == True and \
            self.stock.moving_average(self.stock.close, 20)[-1] > self.stock.moving_average(self.stock.close, 60)[-1] and \
            self.stock.moving_average(self.stock.close, 20)[-1] / self.stock.moving_average(self.stock.close, 20)[-2] >= 1.01 and \
            self.stock.moving_average(self.stock.close, 60)[-1] / self.stock.moving_average(self.stock.close, 60)[-2] >= 1.01):
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule6_neg(self):
        if (self.winner_rule4()[0] == True and self.winner_rule5()[0] == True and \
            self.stock.moving_average(self.stock.close, 20)[-1] < self.stock.moving_average(self.stock.close, 60)[-1] and \
            self.stock.moving_average(self.stock.close, 20)[-2] / self.stock.moving_average(self.stock.close, 20)[-1] >= 1.01 and \
            self.stock.moving_average(self.stock.close, 60)[-2] / self.stock.moving_average(self.stock.close, 60)[-1] >= 1.01):
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule7(self):
        up = (self.stock.close[-1] / self.stock.close[-2] - 1) * 100
        ma5 = self.stock.moving_average(self.stock.close, 5)[-1]
        ma10 = self.stock.moving_average(self.stock.close, 10)[-1]
        ma20 = self.stock.moving_average(self.stock.close, 20)[-1]
        MAs = [ma5, ma10, ma20]
        stdevValue = stdev(MAs)
        if stdevValue <= self.stock.close[-1]/100 and up >= 1:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule7_neg(self):
        down = (self.stock.close[-2] / self.stock.close[-1] - 1) * 100
        ma5 = self.stock.moving_average(self.stock.close, 5)[-1]
        ma10 = self.stock.moving_average(self.stock.close, 10)[-1]
        ma20 = self.stock.moving_average(self.stock.close, 20)[-1]
        MAs = [ma5, ma10, ma20]
        stdevValue = stdev(MAs)
        if stdevValue <= self.stock.close[-1]/100 and down >= 1:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule8(self):
        up = (self.stock.close[-1] / self.stock.close[-2] - 1) * 100
        ma5 = self.stock.moving_average(self.stock.close, 5)[-1]
        ma10 = self.stock.moving_average(self.stock.close, 10)[-1]
        ma20 = self.stock.moving_average(self.stock.close, 20)[-1]
        ma60 = self.stock.moving_average(self.stock.close, 60)[-1]
        MAs = [ma5, ma10, ma20, ma60]
        stdevValue = stdev(MAs)
        if stdevValue <= self.stock.close[-1]/100 and up >= 1:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule8_neg(self):
        down = (self.stock.close[-2] / self.stock.close[-1] - 1) * 100
        ma5 = self.stock.moving_average(self.stock.close, 5)[-1]
        ma10 = self.stock.moving_average(self.stock.close, 10)[-1]
        ma20 = self.stock.moving_average(self.stock.close, 20)[-1]
        ma60 = self.stock.moving_average(self.stock.close, 60)[-1]
        MAs = [ma5, ma10, ma20, ma60]
        stdevValue = stdev(MAs)
        if stdevValue <= self.stock.close[-1]/100 and down >= 1:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule9(self):
        maxPriLast20Days = 0
        for idx in range(2, 21):
            if self.stock.high[-idx] > maxPriLast20Days:
                maxPriLast20Days = self.stock.high[-idx]
            
        if self.stock.close[-1] > maxPriLast20Days:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule9_neg(self):
        minPriLast20Days = 0
        for idx in range(2, 21):
            if self.stock.low[-idx] < minPriLast20Days:
                minPriLast20Days = self.stock.low[-idx]
            
        if self.stock.close[-1] < minPriLast20Days:
            return [True, 2, 2]
        else:
            return [False, 0, 2]


    def winner_rule10(self):
        direction = self.stock.close[-1] - self.stock.open[-1]
        if (abs(self.stock.low[-1] - self.stock.open[-1])) > 2 * (abs(self.stock.open[-1] - self.stock.close[-1])) and direction > 0:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule10_neg(self):
        direction = self.stock.close[-1] - self.stock.open[-1]
        if (abs(self.stock.high[-1] - self.stock.open[-1])) > 2 * (abs(self.stock.open[-1] - self.stock.close[-1])) and direction < 0:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule11(self):
        # TODO
        return [False, 0, 2]

    def winner_rule12(self):
        rsi5_list = []
        up = 0
        total = 0
        for days in range(0,2):
            for T5 in range(0, 5):
                diff = self.stock.close[-1-T5-days] - self.stock.close[-2-T5-days]
                total += abs(diff)
                if diff > 0:
                    up += diff
            if total != 0:
                rsi5 = up*100/total
                if rsi5 == 0:
                    rsi5 = 50
                rsi5_list.append(rsi5)
            else:
                rsi5_list.append(50)

        result = all(i >= 80 for i in rsi5_list)
        if result:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule12_neg(self):
        rsi5_list = []
        up = 0
        total = 0
        for days in range(0,2):
            for T5 in range(0, 5):
                diff = self.stock.close[-1-T5-days] - self.stock.close[-2-T5-days]
                total += abs(diff)
                if diff > 0:
                    up += diff
            if total != 0:
                rsi5 = up*100/total
                if rsi5 == 0:
                    rsi5 = 50
                rsi5_list.append(rsi5)
            else:
                rsi5_list.append(50)

        result = all(i <= 20 for i in rsi5_list)
        if result:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule13(self):
        if self.stock.close[-1] > self.stock.moving_average(self.stock.close, 5)[-1] and \
           self.stock.close[-2] > self.stock.moving_average(self.stock.close, 5)[-2] and \
           self.stock.close[-3] > self.stock.moving_average(self.stock.close, 5)[-3]:
            return [True, 2, 2]
        else:
            return [False, 0, 2]

    def winner_rule13_neg(self):
        if self.stock.close[-1] < self.stock.moving_average(self.stock.close, 5)[-1] and \
           self.stock.close[-2] < self.stock.moving_average(self.stock.close, 5)[-2] and \
           self.stock.close[-3] < self.stock.moving_average(self.stock.close, 5)[-3]:
            return [True, 2, 2]
        else:
            return [False, 0, 2]


    def filter1(self):
        if (abs(self.stock.high[-1] - self.stock.close[-1])) * 2 >= (abs(self.stock.open[-1] - self.stock.close[-1])):
            if (abs(self.stock.low[-1] - self.stock.close[-1])) * 2 >= (abs(self.stock.open[-1] - self.stock.close[-1])):
                return False
            else:
                return True
        else:
            return False

    def filter1_neg(self):
        if (abs(self.stock.low[-1] - self.stock.close[-1])) * 2 >= (abs(self.stock.open[-1] - self.stock.close[-1])):
            if (abs(self.stock.high[-1] - self.stock.close[-1])) * 2 >= (abs(self.stock.open[-1] - self.stock.close[-1])):
                return False
            else:
                return True
        else:
            return False


    def filter2(self):
        if self.stock.volume[-1] < 3000000:
            return True
        else:
            return False

    def filter3(self):
        if self.stock.close[-1] < self.stock.moving_average(self.stock.close, 20)[-1]:
            return True
        else:
            return False

    def filter3_neg(self):
        if self.stock.close[-1] > self.stock.moving_average(self.stock.close, 20)[-1]:
            return True
        else:
            return False
    
    # def filter4(self):
    #     ratio = self.stock.close[-1] / self.stock.moving_average(self.stock.close, 5)[-1]
    #     if ratio >= 1 and ratio <= 1.03:
    #         return False
    #     else:
    #         return True

    # def filter4_neg(self):
    #     ratio = self.stock.moving_average(self.stock.close, 5)[-1] / self.stock.close[-1]
    #     if ratio >= 1 and ratio <= 1.03:
    #         return False
    #     else:
    #         return True

    def best_points(self, raw_check, direction):
        result = []
        check = [x[0] for x in raw_check]
        score = [x[1] for x in raw_check]
        max_score = [x[2] for x in raw_check]
        score = sum(score)
        max_score = sum(max_score)
        normalized_score = round(score/max_score, 2) * 100
        if normalized_score <= 0:
            return None
        if any(check):
            if direction == True:
                positiveFilter = [self.filter1(), self.filter2(), self.filter3()]
                if any(positiveFilter):
                    return None
            else:
                negativeFilter = [self.filter1_neg(), self.filter2(), self.filter3_neg()]
                if any(negativeFilter):
                    return None
            if check.count(True) == 1 and check[0] == True: # The only True result is high volume and no other information
                return None
            for index, v in enumerate(check):
                if v:
                    if direction == True:
                        result.append(self.BEST_WHY_BUY[index])
                    else:
                        result.append(self.BEST_WHY_SELL[index])
            
            if direction == True:
                suggestedPrice = self.stock.moving_average(self.stock.close, 5)[-1] * 1.03
                stopPrice = self.stock.moving_average(self.stock.close, 5)[-1]
                for i in range(7):
                    diff = self.stock.close[-1] - self.stock.open[-1]
                    if diff > 0 and diff >= self.stock.close[-1] * 0.01 and self.stock.open[-1] < stopPrice:
                        stopPrice = self.stock.low[-1]

            else:
                suggestedPrice = self.stock.moving_average(self.stock.close, 5)[-1] * 0.97 * -1
                stopPrice = self.stock.moving_average(self.stock.close, 5)[-1]
                for i in range(7):
                    diff = self.stock.close[-1] - self.stock.open[-1]
                    if diff < 0 and -diff >= self.stock.close[-1] * 0.01 and self.stock.open[-1] > stopPrice:
                        stopPrice = self.stock.high[-1]

            s = f'{normalized_score:.0f}, {self.stock.sid}, {suggestedPrice:.02f}, {stopPrice:.02f}, https://tw.stock.yahoo.com/q/ta?s={self.stock.sid} '
            result.insert(0, s)
            return result
        else:
            return False

    def all_winner_rules(self):
        raw_check_buy = [self.winner_rule1(), self.winner_rule2(), self.winner_rule3(), \
                     self.winner_rule4(), self.winner_rule5(), self.winner_rule6(), \
                     self.winner_rule7(), self.winner_rule8(), self.winner_rule9(), \
                     self.winner_rule10(), self.winner_rule11(), self.winner_rule12(), self.winner_rule13()
                     ]
        raw_check_sell = [self.winner_rule1(), self.winner_rule2(), self.winner_rule3_neg(),
                     self.winner_rule4_neg(), self.winner_rule5_neg(), self.winner_rule6_neg(),
                     self.winner_rule7_neg(), self.winner_rule8(), self.winner_rule9_neg(),
                     self.winner_rule10_neg(), self.winner_rule11(), self.winner_rule12_neg(), self.winner_rule13_neg()
                     ]
        buy = self.best_points(raw_check_buy, direction=True)
        sell = self.best_points(raw_check_sell, direction=False)
        if buy != None:
            M = [round(x[1]/x[2],2) for x in raw_check_buy]
            return (True, buy, M)
        elif sell != None:
            M = [round(x[1]/x[2],2) for x in raw_check_sell]
            return (False, sell, M)

        return None

