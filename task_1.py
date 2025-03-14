from copy import copy
from typing import List, Dict
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

    def __str__(self):
        return f"id: {self.id}\nvolume: {self.volume}\npriority: {self.priority}\nprint_time: {self.print_time}"

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """

    printer_constrains = PrinterConstraints(**constraints)

    # Розподілимо задачі за пріоритетом
    by_priority = defaultdict(list)
    for job in print_jobs:
        print_job = PrintJob(**job)
        by_priority[print_job.priority].append(print_job)

    # Відсортуємо кожен список за часом друку за спаданням
    for priority in by_priority.keys():
        by_priority[priority].sort(key=lambda x: x.print_time)

    # Відсортуємо задачі за пріоритетом та перетворимо словник задач у список
    by_priority = [job for jobs in dict(sorted(by_priority.items())).values() for job in jobs]

    max_time = 0
    starter_queue = copy(by_priority)
    grouped_queue = []
    n = len(starter_queue)

    while n > 0: # Групуємо задачі, поки вони не закінчаться
        if n == 1: # Якщо залишилась одна не згрупована задача, додаємо її до черги
            max_time += starter_queue[0].print_time
            grouped_queue.insert(0, [starter_queue.pop()])
            break

        group = [starter_queue.pop()] # Додаємо до групи останнє завдання з найдовшим часом виконання
        n = len(starter_queue)
        volume = group[0].volume
        max_time += group[0].print_time

        # Якщо у групі менше задач за максимально дозволену кількість
        while len(group) < printer_constrains.max_items:
            # Шукаємо серед завдань, що залишилися те, яке має найдовший час виконання і не перевищує
            # сумарний з усіма завданнями у групі об'єм, допустимий принтером
            # Починаємо з кінця, щоб спочатку згрупувати задачі з найбільшим часом
            for i in range(n - 1, -1, -1):
                if volume + starter_queue[i].volume <= printer_constrains.max_volume:
                    volume += starter_queue[i].volume
                    group.insert(0, starter_queue.pop(i))
                    n = len(starter_queue)
                    break
                else:
                    continue
            # Якщо група не утворилася через перевищення ліміту об'єму
            if len(group) < printer_constrains.max_items:
                break
        # Групу вставляємо на початок черги, таким чином групи з найбільшим часом виконання будуть у кінці
        grouped_queue.insert(0, [*group])

    print_order = [job.id for jobs in grouped_queue for job in jobs]

    return {
        "print_order": print_order,
        "total_time": max_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()

