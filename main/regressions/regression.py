import matplotlib.pyplot as plt
from typing import Tuple, Union
import numpy as np
import random


# class DataGenerator(namedtuple("DataGenerator", "dimension, args_min, args_max, args_step, generator_func")):
#    def __new__(cls, **args):

class Regression:
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Regression class is static class")

    @staticmethod
    def rand_in_range(rand_range: Union[float, Tuple[float, float]] = 1.0) -> float:
        if isinstance(rand_range, float):
            return random.uniform(-0.5 * rand_range, 0.5 * rand_range)
        if isinstance(rand_range, tuple):
            return random.uniform(rand_range[0], rand_range[1])
        return random.uniform(-0.5, 0.5)

    @staticmethod
    def test_data_along_line(k: float = 1.0, b: float = 0.1, arg_range: float = 1.0,
                             rand_range: float = 0.05, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Генерирует линию вида y = k * x + b + dy, где dy - аддитивный шум с амплитудой half_disp
        :param k: наклон линии
        :param b: смещение по y
        :param arg_range: диапазон аргумента от 0 до arg_range
        :param rand_range: диапазон шума данных
        :param n_points: количество точек
        :return: кортеж значений по x и y
        """
        x_step = arg_range / (n_points - 1)
        return np.array([i * x_step for i in range(n_points)]),\
               np.array([i * x_step * k + b + Regression.rand_in_range(rand_range) for i in range(n_points)])

    def test_data_along_cosh(k: float = 1.0, b: float = 0.1, arg_range: float = 1.0,
                             rand_range: float = 0.05, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Генерирует линию вида y = k * x + b + dy, где dy - аддитивный шум с амплитудой half_disp
        :param k: наклон линии
        :param b: смещение по y
        :param arg_range: диапазон аргумента от 0 до arg_range
        :param rand_range: диапазон шума данных
        :param n_points: количество точек
        :return: кортеж значений по x и y
        """
        x_step = arg_range / (n_points - 1)
        return np.array([i * x_step for i in range(n_points)]),\
               np.array([np.cosh(i * x_step) + Regression.rand_in_range(rand_range) for i in range(n_points)])

    @staticmethod
    def second_order_surface_2d(surf_params:
                                Tuple[float, float, float, float, float, float] = (1.0, -2.0, 3.0, 1.0, 2.0, -3.0),
                                args_range: float = 1.0, rand_range: float = .1, n_points: int = 1000) -> \
                                Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Генерирует набор тестовых данных около поверхности второго порядка.
        Уравнение поверхности:
        z(x,y) = a * x^2 + x * y * b + c * y^2 + d * x + e * y + f
        :param surf_params: 
        :param surf_params [a, b, c, d, e, f]:
        :param args_range x in [x0, x1], y in [y0, y1]:
        :param rand_range:
        :param n_points:
        :return:
        """
        x = np.array([Regression.rand_in_range(args_range) for _ in range(n_points)])
        y = np.array([Regression.rand_in_range(args_range) for _ in range(n_points)])
        dz = np.array([surf_params[5] + Regression.rand_in_range(rand_range) for _ in range(n_points)])
        return x, y, surf_params[0] * x * x + surf_params[1] * y * x + surf_params[2] * y * y + \
               surf_params[3] * x + surf_params[4] * y + dz

    @staticmethod
    def test_data_2d(kx: float = -2.0, ky: float = 2.0, b: float = 12.0, args_range: float = 1.0,
                     rand_range: float = 1.0, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Генерирует плоскость вида z = kx*x + ky*x + b + dz, где dz - аддитивный шум в диапазоне rand_range
        :param kx: наклон плоскости по x
        :param ky: наклон плоскости по y
        :param b: смещение по z
        :param args_range: диапазон аргументов по кажой из осей от 0 до args_range
        :param rand_range: диапазон шума данных
        :param n_points: количество точек
        :returns: кортеж значенией по x, y и z
        """
        x = np.array([Regression.rand_in_range(args_range) for _ in range(n_points)])
        y = np.array([Regression.rand_in_range(args_range) for _ in range(n_points)])
        dz = np.array([b + Regression.rand_in_range(rand_range) for _ in range(n_points)])
        return x, y, x * kx + y * ky + dz

    @staticmethod
    def test_data_nd(surf_settings: np.ndarray = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 12.0]), args_range: float = 1.0,
                     rand_range: float = 0.1, n_points: int = 125) -> np.ndarray:
        """
        Генерирует плоскость вида z = k_0*x_0 + k_1*x_1...,k_n*x_n + d + dz, где dz - аддитивный шум в диапазоне rand_range
        :param surf_settings: параметры плоскости в виде k_0,k_1,...,k_n,d
        :param args_range: диапазон аргументов по кажой из осей от 0 до args_range
        :param n_points: количество точек
        :param rand_range: диапазон шума данных
        :returns: массив из строк вида x_0, x_1,...,x_n, f(x_0, x_1,...,x_n)
        """
        n_dims = surf_settings.size - 1
        data = np.zeros((n_points, n_dims + 1,), dtype=float)
        for i in range(n_dims):
            data[:, i] = np.array([Regression.rand_in_range(args_range) for _ in range(n_points)])
            data[:, n_dims] += surf_settings[i] * data[:, i]
        dz = np.array([surf_settings[n_dims] + Regression.rand_in_range(rand_range) for _ in range(n_points)])
        data[:, n_dims] += dz
        return data

    @staticmethod
    def distance_sum(x: np.ndarray, y: np.ndarray, k: float, b: float) -> float:
        """
        Вычисляет сумму квадратов расстояний от набора точек до линии вида y = k*x + b при фиксированных k и b
        по формуле: F(k, b) = (Σ(yi -(k * xi + b))^2)^0.5 (суммирование по i)
        :param x: массив значений по x
        :param y: массив значений по y
        :param k: значение параметра k (наклон)
        :param b: значение параметра b (смещение)
        :returns: F(k, b) = (Σ(yi -(k * xi + b))^2)^0.5
        """
        return np.sqrt(np.power((y - x * k + b), 2.0).sum())

    @staticmethod
    def distance_field(x: np.ndarray, y: np.ndarray, k: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Вычисляет сумму квадратов расстояний от набора точек до линии вида y = k*x + b, где k и b являются диапазонами
        значений. Формула расстояния для j-ого значения из набора k и k-ого значения из набора b:
        F(k_j, b_k) = (Σ(yi -(k_j * xi + b_k))^2)^0.5 (суммирование по i)
        :param x: массив значений по x
        :param y: массив значений по y
        :param k: массив значений параметра k (наклоны)
        :param b: массив значений параметра b (смещения)
        :returns: поле расстояний вида F(k, b) = (Σ(yi -(k * xi + b))^2)^0.5 (суммирование по i)
        """
        return np.array([[Regression.distance_sum(x, y, k_i, b_i) for k_i in k.flat] for b_i in b.flat])

    @staticmethod
    def linear_regression(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """
        Линейная регрессия.\n
        Основные формулы:\n
        yi - xi*k - b = ei\n
        yi - (xi*k + b) = ei\n
        (yi - (xi*k + b))^2 = yi^2 - 2*yi*(xi*k + b) + (xi*k + b)^2 = ei^2\n
        yi^2 - 2*(yi*xi*k + yi*b) + (xi^2 * k^2 + 2 * xi * k * b + b^2) = ei^2\n
        yi^2 - 2*yi*xi*k - 2*yi*b + xi^2 * k^2 + 2 * xi * k * b + b^2 = ei^2\n
        d ei^2 /dk = - 2*yi*xi + 2 * xi^2 * k + 2 * xi * b = 0\n
        d ei^2 /db = - 2*yi + 2 * xi * k + 2 * b = 0\n
        ====================================================================================================================\n
        d ei^2 /dk = (yi - xi * k - b) * xi = 0\n
        d ei^2 /db =  yi - xi * k - b = 0\n
        ====================================================================================================================\n
        Σ(yi - xi * k - b) * xi = 0\n
        Σ yi - xi * k - b = 0\n
        ====================================================================================================================\n
        Σ(yi - xi * k - b) * xi = 0\n
        Σ(yi - xi * k) = n * b\n
        ====================================================================================================================\n
        Σyi - k * Σxi = n * b\n
        Σxi*yi - xi^2 * k - xi*b = 0\n
        Σxi*yi - Σxi^2 * k - Σxi*b = 0\n
        Σxi*yi - Σxi^2 * k - Σxi*(Σyi - k * Σxi) / n = 0\n
        Σxi*yi - Σxi^2 * k - Σxi*Σyi / n + k * (Σxi)^2 / n = 0\n
        Σxi*yi - Σxi*Σyi / n + k * ((Σxi)^2 / n - Σxi^2)  = 0\n
        Σxi*yi - Σxi*Σyi / n = -k * ((Σxi)^2 / n - Σxi^2)\n
        (Σxi*yi - Σxi*Σyi / n) / (Σxi^2 - (Σxi)^2 / n) = k\n
        окончательно:\n
        k = (Σxi*yi - Σxi*Σyi / n) / (Σxi^2 - (Σxi)^2 / n)\n
        b = (Σyi - k * Σxi) /n\n
        :param x: массив значений по x
        :param y: массив значений по y
        :returns: возвращает пару (k, b), которая является решением задачи (Σ(yi -(k * xi + b))^2)->min
        """
        n = x.size
        k = (np.sum((x*y)) - np.sum(x) * np.sum(y) / n) / (np.sum(x*x) - np.sum(x)**2 / n)
        b = (np.sum(y) - k * np.sum(x))/n
        return k, b

    @staticmethod
    def bi_linear_regression(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Tuple[float, float, float]:
        """
        Билинейная регрессия.\n
        Основные формулы:\n
        zi - (yi * ky + xi * kx + b) = ei\n
        zi^2 - 2*zi*(yi * ky + xi * kx + b) + (yi * ky + xi * kx + b)^2 = ei^2\n
        ei^2 = zi^2 - 2*yi*zi*ky - 2*zi*xi*kx - 2*zi*b + ((yi*ky)^2 + 2 * (xi*kx*yi*ky + b*yi*ky) + (xi*kx + b)^2)\n
        ei^2 = zi^2 - 2*yi*zi*ky - 2*zi*xi*kx - 2*zi*b + (yi*ky)^2 + 2*xi*kx*yi*ky + 2*b*yi*ky + (xi*kx + b)^2\n
        ei^2 =\n
        zi^2 - 2*zi*yi*ky - 2*zi*xi*kx - 2*zi*b + (yi*ky)^2 + 2*xi*kx*yi*ky + 2*b*yi*ky + (xi*kx)^2 + 2*xi*kx*b+ b^2\n
        ei^2 =\n
        zi^2 - 2*zi*yi*ky - 2*zi*xi*kx - 2*zi*b + (yi*ky)^2 + 2*xi*kx*yi*ky + 2*b*yi*ky + (xi*kx)^2 + 2*xi*kx*b+ b^2\n
        ei^2 =\n
        zi^2 - 2*zi*yi*ky - 2*zi*xi*kx - 2*zi*b + (yi*ky)^2 + 2*xi*kx*yi*ky + 2*b*yi*ky + (xi*kx)^2 + 2*xi*kx*b + b^2\n
        ====================================================================================================================\n
        d Σei^2 /dkx = Σ-zi*xi + ky*xi*yi + kx*xi^2 + xi*b = 0\n
        d Σei^2 /dky = Σ-zi*yi + ky*yi^2 + kx*xi*yi + b*yi = 0\n
        d Σei^2 /db  = Σ-zi + yi*ky + xi*kx = 0\n
        ====================================================================================================================\n
        d Σei^2 /dkx / dkx = Σ xi^2\n
        d Σei^2 /dkx / dky = Σ xi*yi\n
        d Σei^2 /dkx / db  = Σ xi\n
        ====================================================================================================================\n
        d Σei^2 /dky / dkx = Σ xi*yi\n
        d Σei^2 /dky / dky = Σ yi^2\n
        d Σei^2 /dky / db  = Σ yi\n
        ====================================================================================================================\n
        d Σei^2 /db / dkx = Σ xi\n
        d Σei^2 /db / dky = Σ yi\n
        d Σei^2 /db / db  = n\n
        ====================================================================================================================\n
        Hesse matrix:\n
        || d Σei^2 /dkx / dkx;  d Σei^2 /dkx / dky;  d Σei^2 /dkx / db ||\n
        || d Σei^2 /dky / dkx;  d Σei^2 /dky / dky;  d Σei^2 /dky / db ||\n
        || d Σei^2 /db  / dkx;  d Σei^2 /db  / dky;  d Σei^2 /db  / db ||\n
        ====================================================================================================================\n
        Hesse matrix:\n
                       | Σ xi^2;  Σ xi*yi; Σ xi |\n
        H(kx, ky, b) = | Σ xi*yi; Σ yi^2;  Σ yi |\n
                       | Σ xi;    Σ yi;    n    |\n
        ====================================================================================================================\n
                          | Σ-zi*xi + ky*xi*yi + kx*xi^2 + xi*b |\n
        grad(kx, ky, b) = | Σ-zi*yi + ky*yi^2 + kx*xi*yi + b*yi |\n
                          | Σ-zi + yi*ky + xi*kx                |\n
        ====================================================================================================================\n
        Окончательно решение:\n
        |kx|   |1|\n
        |ky| = |1| -  H(1, 1, 0)^-1 * grad(1, 1, 0)\n
        | b|   |0|\n

        :param x: массив значений по x
        :param y: массив значений по y
        :param z: массив значений по z
        :returns: возвращает тройку (kx, ky, b), которая является решением задачи (Σ(zi - (yi * ky + xi * kx + b))^2)->min
        """
        hesse = ([np.sum((x * x)), np.sum((x * y)), np.sum(x)],
                [np.sum((x* y)), np.sum((y*  y)), np.sum(y)],
                [np.sum(x),   np.sum(y),   x.size])

        hesseInv = np.linalg.inv(hesse)
        # def grad(kx, ky, b):
        #     return [sum(np.multiply(-z, x) + ky * np.multiply(x, y) + kx * np.multiply(x, x) + b*x),
        #                  sum(np.multiply(-z, y) + ky * np.multiply(y, y) + kx * np.multiply(x, y) + b*y),
        #                  sum(-z + y*ky + x*kx)]
        grad = ([np.sum((-z* x) + (x* y) + (x* x)),
                         np.sum((-z* y) + (y* y) + (x* y)),
                         np.sum(-z + y + x)])

        return np.array([1, 1, 0]) - np.dot(hesseInv, grad)

    @staticmethod
    def n_linear_regression(data_rows: np.ndarray) -> np.ndarray:
        """
        H_ij = Σx_i * x_j, i in [0, rows - 1] , j in [0, rows - 1]
        H_ij = Σx_i, j = rows i in [rows, :]
        H_ij = Σx_j, j in [:, rows], i = rows

               | Σkx * xi^2    + Σky * xi * yi + b * Σxi - Σzi * xi|\n
        grad = | Σkx * xi * yi + Σky * yi^2    + b * Σyi - Σzi * yi|\n
               | Σyi * ky      + Σxi * kx                - Σzi     |\n

        x_0 = [1,...1, 0] =>

               | Σ xi^2    + Σ xi * yi - Σzi * xi|\n
        grad = | Σ xi * yi + Σ yi^2    - Σzi * yi|\n
               | Σxi       + Σ yi      - Σzi     |\n

        :param data_rows:  состоит из строк вида: [x_0,x_1,...,x_n, f(x_0,x_1,...,x_n)]
        :return:
        """
        s_rows, s_cols = data_rows.shape

        hessian = np.zeros((s_cols, s_cols), dtype=float)

        grad = np.zeros(s_cols, dtype=float)

        x_0 = np.zeros(s_cols, dtype=float)

        for row in range(s_cols - 1):
            x_0[row] = 1.0
            for col in range(row + 1):
                hessian[row, col] = hessian[col, row] = np.sum(data_rows[:, row] @ data_rows[:, col])
            value = np.sum(data_rows[:, row])
            hessian[row, -1] = hessian[-1, row] = value



        hessian[-1, -1] = data_rows.shape[0]

        for row in range(s_cols - 1):
            grad[row] = np.sum(hessian[row, :-1]) - np.dot(data_rows[:, -1], data_rows[:, row])

        grad[-1] = np.sum(hessian[-1, :-1]) - np.sum(data_rows[:, -1])

        return x_0 - np.linalg.inv(hessian) @ grad

    @staticmethod
    def poly_regression(x: np.ndarray, y: np.ndarray, order: int = 5) -> np.ndarray:
        """
        Полином: y = Σ_j x^j * bj
        Отклонение: ei = yi - Σ_j xi^j * bj
        Минимизируем: Σ_i(yi - Σ_j xi^j * bj)^2 -> min
        Σ_i(yi - Σ_j xi^j * bj)^2 = Σ_iyi^2 - 2 * yi * Σ_j xi^j * bj +(Σ_j xi^j * bj)^2
        условие минимума: d/dbj Σ_i ei = d/dbj (Σ_i yi^2 - 2 * yi * Σ_j xi^j * bj +(Σ_j xi^j * bj)^2) = 0
        :param x: массив значений по x
        :param y: массив значений по y
        :param order: порядок полинома
        :return: набор коэффициентов bi полинома y = Σx^i*bi
        """

        n = x.size
        Xm = np.zeros((n, order))
        Xm[:, 0] = 1

        for i in range(1, order):
            Xm[:, i] = Xm[:, i - 1] * x

        XmT = np.transpose(Xm)

        x1 = np.linalg.inv(np.dot(XmT, Xm))
        x2 = np.dot(x1, XmT)
        x3 = np.dot(x2, y)

        return x3

    @staticmethod
    def polynom(x: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        :param x: массив значений по x\n
        :param b: массив коэффициентов полинома\n
        :returns: возвращает полином yi = Σxi^j*bj\n
        """
        x_curr = np.ones_like(x)
        result = np.zeros_like(x)
        for p, c in enumerate(b.flat):
            result += x_curr * c
            x_curr *= x
        return result

    @staticmethod
    def quadratic_regression_2d(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
        """
        Генерирует набор коэффициентов поверхности второго порядка. Уравнение поверхности:
        z(x,y) = a * x^2 + x * y * b + c * y^2 + d * x + e * y + f
        Поверхность максимальна близка ко всем точкам их набора.
        Получить коэффициенты можно по формуле:
        C = A^-1 * B
        C = {a, b, c, d, e, f}^T (вектор столбец искомых коэффициентов)
        Далее введём обозначения:
        x_i - i-ый элемент массива x
        y_i - i-ый элемент массива y
        z_i - i-ый элемент массива z
        C = {a, b, c, d, e, f}^T (вектор столбец искомых коэффициентов)
        B = {Σ xi^2 * zi,
             Σ xi * yi * zi,
             Σ yi^2 * zi,
             Σ xi * zi,
             Σ yi * zi,
             Σ zi} - (вектор свободных членов)
        Чтобы построить матрицу A введём новую матрицу D, составленную из условий:
        D = { x^2 | x * y | y^2 | x | y | 1 }.
        Строка этой матрицы имеет вид:
        di = { xi^2, xi * yi, yi^2, xi, yi, 1 }.

        Матричный элемент матрицы A выражается из матрицы D следующим образом:
        a_ij = (D[:,i], D[:,j]), где (*, *) - скалярное произведение.
        Матрица A - симметричная и имеет размерность 6x6.
        :param x:
        :param y:
        :param z:
        :return:
        """

        n = x.size

        B = np.array([np.sum(x * x * z), np.sum(x * y * z), np.sum(y * y * z), np.sum(x * z), np.sum(y * z), np.sum(z)])

        D = np.array([np.array([x[i] * x[i], x[i] * y[i], y[i] * y[i], x[i], y[i], 1]) for i in range(0, n)])

        A = np.array([np.array([np.sum(D[:, i] * D[:, j]) for j in range(0, 6)]) for i in range(0, 6)])

        Ainv = np.linalg.inv(A)

        return np.dot(Ainv, B)

    @staticmethod
    def distance_field_example():
        """
        Функция проверки поля расстояний:\n
        1) Посчитать тестовыe x и y используя функцию test_data\n
        2) Задать интересующие нас диапазоны k и b (np.linspace...)\n
        3) Рассчитать поле расстояний (distance_field) и вывести в виде изображения.\n
        4) Проанализировать результат (смысл этой картинки в чём...)\n
        :return:
        """
        print("distance field test:")
        x, y = Regression.test_data_along_line()
        k_, b_ = Regression.linear_regression(x, y)
        print(f"y(x) = {k_:1.5} * x + {b_:1.5}\n")
        k = np.linspace(-2.0, 2.0, 128, dtype=float)
        b = np.linspace(-2.0, 2.0, 128, dtype=float)
        z = Regression.distance_field(x, y, k, b)
        plt.imshow(z, extent=[k.min(), k.max(), b.min(), b.max()])
        plt.plot(k_, b_, 'r*')
        plt.xlabel("k")
        plt.ylabel("b")
        plt.title("Поле расстояний")
        plt.grid(True)
        plt.show()

    @staticmethod
    def linear_reg_example():
        """
        Функция проверки работы метода линейной регрессии:\n
        1) Посчитать тестовыe x и y используя функцию test_data\n
        2) Получить с помошью linear_regression значения k и b\n
        3) Вывести на графике x и y в виде массива точек и построить\n
           регрессионную прямую вида: y = k*x + b\n
        :return:
        """

        x, y = Regression.test_data_along_line()
        k, b = Regression.linear_regression(x, y)
        xl = np.linspace(0, 1, 1000)
        yl = xl * k + b
        print("linear reg test:")
        print(f"y(x) = {k:.5f} * x + {b:.5f}\n")

        plt.scatter(x, y, color='red')
        plt.plot(xl, yl)
        plt.xlabel("k")
        plt.ylabel("b")
        plt.title("График линейной регрессии")
        plt.grid(True)
        plt.show()

    @staticmethod
    def bi_linear_reg_example():
        """
        Функция проверки работы метода билинейной регрессии:\n
        1) Посчитать тестовыe x, y и z используя функцию test_data_2d\n
        2) Получить с помошью bi_linear_regression значения kx, ky и b\n
        3) Вывести на трёхмерном графике x, y и z в виде массива точек и построить\n
           регрессионную плоскость вида:\n z = kx*x + ky*y + b\n
        :return:
        """

        x, y, z = Regression.test_data_2d()
        kx, ky, b = Regression.bi_linear_regression(x, y, z)

        print("bi-linear reg test:")
        print(f"z(x, y) = {kx:.4f} * x + {ky:.4f} * y + {b:.4f}")

        xl = np.linspace(-1, 1, 128, dtype=float)
        yl = np.linspace(-1, 1, 128, dtype=float)

        XL, YL = np.meshgrid(xl, yl)

        ZL = kx * XL + ky * YL + b

        ax = plt.axes(projection='3d')
        ax.plot_surface(XL, YL, ZL, alpha=0.5)
        ax.scatter(x, y, z, color='red')
        plt.title('График билинейной регрессии')

        plt.grid(True)
        plt.show()

    @staticmethod
    def poly_reg_example():
        """
        Функция проверки работы метода полиномиальной регрессии:\n
        1) Посчитать тестовыe x, y используя функцию test_data\n
        2) Посчитать набор коэффициентов bi полинома y = Σx^i*bi используя функцию poly_regression\n
        3) Вывести на графике x и y в виде массива точек и построить\n
           регрессионную кривую. Для построения кривой использовать метод polynom\n
        :return:
        """
        print('\npoly regression test:')
        x, y = Regression.test_data_along_cosh()
        coefficients = Regression.poly_regression(x, y)
        y_ = Regression.polynom(x, coefficients)

        print(f"y(x) = {' + '.join(f'{coefficients[i]:.4} * x^{i}' for i in range(coefficients.size))}\n")
        plt.scatter(x, y, color="red")
        plt.plot(x, y_)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("График полиномиальной регрессии")
        plt.grid(True)
        plt.show()

    @staticmethod
    def n_linear_reg_example():
        nd = Regression.test_data_nd()
        coefficients = Regression.n_linear_regression(nd)
        print("\nn linear regression test:")
        print(f"z(X) = {' + '.join(f'{coefficients[i]:.4} * x_{i}' if i != coefficients.size - 1 else f'{coefficients[i]:.4}' for i in range(coefficients.size))}\n")




        # print("n linear regression test on bi linear regression:")
        # x, y, z = Regression.test_data_2d()
        # kx, ky, b = Regression.n_linear_regression(np.array([x, y, z]))
        # print(f"z(x,y) = {kx:1.5} * x + {ky:1.5} * y + {b:1.5}\n")
        #
        # xr = np.linspace(-1, 1, 128, dtype=float)
        # yr = np.linspace(-1, 1, 128, dtype=float)
        #
        # XR, YR = np.meshgrid(xr, yr)
        # ZR = XR * kx + YR * ky + b
        #
        # ax = plt.axes(projection='3d')
        # ax.plot_surface(XR, YR, ZR, alpha=0.5)
        # ax.scatter(x, y, z, color='red')
        # plt.title("График n-линейной регрессии")
        # plt.grid(True)
        # plt.show()

    @staticmethod
    def quadratic_reg_example():

        print('2d quadratic regression test:')
        x, y, z = Regression.second_order_surface_2d()
        coeffs = Regression.quadratic_regression_2d(x, y, z)

        # def zF(x, y):
        #     return coeffs[0] * x ** 2 + x * y * coeffs[1] + coeffs[2] * y ** 2 + coeffs[3] * x + coeffs[4] * y + coeffs[5]

        xr = np.linspace(-1, 1, 128, dtype=float)
        yr = np.linspace(-1, 1, 128, dtype=float)

        XR, YR = np.meshgrid(xr, yr)
        ZR = coeffs[0] * XR ** 2 + XR * YR * coeffs[1] + coeffs[2] * YR ** 2 + coeffs[3] * XR + coeffs[4] * YR + coeffs[5]

        ax = plt.axes(projection='3d')
        ax.plot_surface(XR, YR, ZR, alpha=0.5)
        ax.scatter(x, y, z, color='red')
        plt.title('График квадратичной регрессии')
        plt.grid(True)
        plt.show()
        # y_ = polynom(x, coefficients)
        print(
            f"z(x, y) = {coeffs[0]:1.3} * x^2 + {coeffs[1]:1.3} * x * y + {coeffs[2]:1.3} * y^2 + {coeffs[3]:1.3} * x + {coeffs[4]:1.3} * y + {coeffs[5]:1.3}")
