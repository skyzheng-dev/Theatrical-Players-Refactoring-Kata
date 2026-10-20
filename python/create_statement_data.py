import math


class PerformanceCalculator:
    def __init__(self, performance, play):
        self.performance = performance
        self.play = play

    def amount(self):
        raise NotImplementedError

    def volume_credits(self):
        return max(self.performance['audience'] - 30, 0)


class TragedyCalculator(PerformanceCalculator):
    def amount(self):
        result = 40000
        if self.performance['audience'] > 30:
            result += 1000 * (self.performance['audience'] - 30)
        return result


class ComedyCalculator(PerformanceCalculator):
    def amount(self):
        result = 30000
        if self.performance['audience'] > 20:
            result += 10000 + 500 * (self.performance['audience'] - 20)
        result += 300 * self.performance['audience']
        return result

    def volume_credits(self):
        # original code divides by 5 (not 10 as its comment said), kept as-is
        return super().volume_credits() + math.floor(self.performance['audience'] / 5)


class HistoricalCalculator(PerformanceCalculator):
    def amount(self):
        result = 50000
        if self.performance['audience'] > 20:
            result += 1500 * (self.performance['audience'] - 20)
        return result

    def volume_credits(self):
        # historical plays don't get the base "over 30" credits, only 1 per 5 people
        return math.floor(self.performance['audience'] / 5)


def create_performance_calculator(performance, play):
    if play['type'] == "tragedy":
        return TragedyCalculator(performance, play)
    if play['type'] == "comedy":
        return ComedyCalculator(performance, play)
    if play['type'] == "historical":
        return HistoricalCalculator(performance, play)
    raise ValueError(f'unknown type: {play["type"]}')


def create_statement_data(invoice, plays):
    performances = []
    for perf in invoice['performances']:
        play = plays[perf['playID']]
        calculator = create_performance_calculator(perf, play)
        performances.append({
            'play': play,
            'audience': perf['audience'],
            'amount': calculator.amount(),
            'volume_credits': calculator.volume_credits(),
        })

    return {
        'customer': invoice['customer'],
        'performances': performances,
        'total_amount': sum(p['amount'] for p in performances),
        'total_volume_credits': sum(p['volume_credits'] for p in performances),
    }
