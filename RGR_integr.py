import math

# ПРОСТЕЙШИЕ ФУНКЦИИ

def rectangles(f, n, a, b):
    h = (b - a) / n
    result = 0
    for i in range(n):
        x_mid = a + (i + 0.5) * h
        result += f(x_mid)
    return h * result


def trapezoid(f, n, a, b):
    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    y = [f(xi) for xi in x]
    return h * ((y[0] + y[-1]) / 2 + sum(y[1:-1]))


def simpson(f, n, a, b):
    if n % 2 != 0:
        n += 1  # чтобы точно было четным
    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    y = [f(xi) for xi in x]
    return h / 3 * (y[0] + y[-1] + 4 * sum(y[1:-1:2]) + 2 * sum(y[2:-1:2]))


def three_eighths(f, n, a, b):
    if n % 3 != 0:
        n = ((n + 2) // 3) * 3  # чтобы точно было кратным 3
    h = (b - a) / n
    result = 0
    for i in range(0, n, 3):
        x0 = a + i * h
        x1 = a + (i + 1) * h
        x2 = a + (i + 2) * h
        x3 = a + (i + 3) * h
        result += (3 * h / 8) * (f(x0) + 3 * f(x1) + 3 * f(x2) + f(x3))
    return result


#ОШИБКА РУНГЕ

def runge_error(I_n, I_2n, p):
    return abs(I_n - I_2n) / (2 ** p - 1)

# ПОСЛЕДОВАТЕЛЬНО РАЗБИВАЕМ НА ВСЕ БОЛЬШЕЕ ЧИСЛО КУСКОВ

def adaptive_integrate(method, f, a, b, eps, p, method_name):
    n = 4
    max_iter = 20

    print(f"\nМетод: {method_name}")
    print(f"{'n':>5} {'h':>10} {'I':>12} {'error':>12}")

    for iteration in range(max_iter):
        h = (b - a) / n
        I_n = method(f, n, a, b)
        I_2n = method(f, 2 * n, a, b)

        error = runge_error(I_n, I_2n, p)

        print(f"{n:5d} {h:10.6f} {I_2n:12.8f} {error:12.2e}")

        if error < eps:
            print(f"Достигнута точность {eps} за {iteration + 1} итераций")
            return I_2n, n

        n *= 2

    print("Достигнуто максимальное число итераций")
    return I_2n, n


#ФУНКЦИИ КОТОРУЮ ИНТЕГРИРУЕМ
def f_power(x):
    return x**2

def f_poisson(x):
    return math.exp(-x * x)

def f_abs(x):
    return abs(x)

def f_runge(x):
    return 1 / (1 + 25 * x * x)

#НАЧАЛЬНЫЕ ДАННЫЕ ДЛЯ РАЗНЫХ ФУНКЦИЙ

test_tasks = {
    'x²': {
        'f': f_power,
        'a': 0, 'b': 1,
        'exact': 1/3,
        'note': 'Многочлен 2 степени'
    },
    'Интеграл Пуассона': {
        'f': f_poisson,
        'a': -2, 'b': 2,
        'exact': 1.77245,
        'note': 'Гладкая, неберущаяся'
    },
    '|x|': {
        'f': f_abs,
        'a': -1, 'b': 1,
        'exact': 1.0,
        'note': 'Разрыв первой производной'
    },
    'Функция Рунге': {
        'f': f_runge,
        'a': -1, 'b': 1,
        'exact': 0.54936,
        'note': 'Проблемная для интерполяции'
    }
}

# ОСНОВНАЯ ЧАСТЬ
eps = 1e-6

methods = [
    (rectangles, 2, "Прямоугольники"),
    (trapezoid, 2, "Трапеции"),
    (simpson, 4, "Симпсон"),
    (three_eighths, 4, "Три восьмых")
]

for task_name, task in test_tasks.items():
    print(f"\n{'=' * 70}")
    print(f"ТЕСТ: {task_name} — {task['note']}")
    print(f"Отрезок [{task['a']}, {task['b']}], точное значение: {task['exact']:.8f}")
    print(f"{'=' * 70}")

    for method, p, method_name in methods:
        try:
            result, n = adaptive_integrate(
                method, task['f'], task['a'], task['b'],
                eps, p, method_name
            )
            actual_error = abs(task['exact'] - result)

            print(f"Результат: {result:.8f}")
            print(f"Фактическая ошибка: {actual_error:.2e}")
            print(f"Число разбиений: {n}")
            print("-" * 50)

        except Exception as e:
            print(f"Ошибка для {method_name}: {e}")
            print("-" * 50)