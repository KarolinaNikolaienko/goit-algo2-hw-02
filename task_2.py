from typing import List, Dict
from collections import defaultdict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """

    # Тут повинен бути ваш код

    return {
        "max_profit": None,
        "cuts": None,
        "number_of_cuts": None
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """

    if not prices or length <= 0 or min(prices) <= 0 or len(prices) != length:
        return {
            "max_profit": None,
            "cuts": None,
            "number_of_cuts": None
        }

    cuts = defaultdict(list)

    for i in range(1, length + 1):
        current_profit = 0
        current_cuts = []
        n = length // i
        m = length % i
        current_profit += prices[i - 1] * n
        current_cuts.extend([i] * n)
        if m > 0:
            rest_profit = 0
            rest_cuts = []
            for j in range(1, m + 1):
                rn = m // j
                temp_profit = prices[j - 1] * rn
                if temp_profit > rest_profit:
                    rest_profit = temp_profit
                    rest_cuts = [j] * rn
            current_profit += rest_profit
            current_cuts.extend(rest_cuts)

        cuts[current_profit].append(current_cuts)

    max_profit = max(cuts.items())
    max_profit_cuts = max_profit[1] if len(max_profit[1]) > 1 else [cut for cuts in max_profit[1] for cut in cuts]
    if isinstance(max_profit_cuts[0], list):
        number_of_cuts = [len(l) - 1 for l in max_profit_cuts]
    else:
        number_of_cuts = len(max_profit_cuts) - 1

    return {
        "max_profit": max_profit[0],
        "cuts": max_profit_cuts,
        "number_of_cuts": number_of_cuts
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")
        #
        # # Тестуємо мемоізацію
        # memo_result = rod_cutting_memo(test['length'], test['prices'])
        # print("\nРезультат мемоізації:")
        # print(f"Максимальний прибуток: {memo_result['max_profit']}")
        # print(f"Розрізи: {memo_result['cuts']}")
        # print(f"Кількість розрізів: {memo_result['number_of_cuts']}")
        #
        # # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")
        #
        # print("\\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
