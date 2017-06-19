import numpy as np
from numpy import linalg as la

class cylinder:                                                         # Класс, описывающий цилиндр
    def __init__(self, o, a, b, c):                                     # o - центр основания, a, b - оси эллпса, c - центральная ось цилиндра
        self.o = o
        self.a = a
        self.b = b
        self.c = c

    def check(self):                                                    # Проверка корректности задания цилиндра
        if np.all(np.matmul(np.transpose(self.a), self.b) == 0):        # a и b должны быть ортогональны
            matr = np.hstack((self.a, self.b, self.c))                  # a, b и c должны быть ЛНЗ системой
            if la.det(matr) != 0:
                return True
        return False

    def get_translation(self):                                       # Возвращает вектор параллельного переноса (для смены базиса)
        return -self.o

    def get_matrix(self):                                            # Возвращет матрицу перехода в базис (a, b, c)
        return la.inv(np.hstack((self.a, self.b, self.c)))

class parallelogram:                                                    # Класс, описывающий параллелограмм
    def __init__(self, o, a, b, c):
        self.o = o
        self.a = a
        self.b = b
        self.c = c

    def check(self):                                                    # Проверка корректности задания цилиндра
        matr = np.hstack((self.a, self.b, self.c))                      # a, b и c должны быть ЛНЗ системой
        if la.det(matr) != 0:
            return True
        return False

    def transform(self, matr, delta):                                         # Преобразование координат
        self.o = np.matmul(matr, self.o + delta)                            # delta - вектор переноса
        self.a = np.matmul(matr, self.a)                                     # matr - матрица перехода
        self.b = np.matmul(matr, self.b)
        self.c = np.matmul(matr, self.c)

    def _get_X_4(self):                                     # Возвращает матрицу X_4 (описана в тексте)
        matr = np.hstack((self.o, self.a, self.b, self.c))
        v = [matr[0, ]]
        print(v)
        return np.matmul(np.transpose(v), v)

    def _get_Y_4(self):                                     # Возвращает матрицу Y_4 (описана в тексте)
        matr = np.hstack((self.o, self.a, self.b, self.c))
        v = [matr[1, ]]
        print(v)
        return np.matmul(np.transpose(v), v)

    def _get_2_projection(self, matr, coord_num):                       # Возвращает X_2 или Y_2
        rows = np.vstack((matr[1:coord_num], matr[coord_num + 1:]))
        m = np.hstack((rows[:, 1:coord_num], rows[:, coord_num + 1:]))
        return m

    def _get_b(self, matr, coord_num, val):                             # Возвращает b_X или b_Y
        rows = np.vstack((matr[1], matr[coord_num]))
        m = np.hstack((rows[:, 1:coord_num], rows[:, coord_num + 1:]))
        return 2 * np.matmul(np.array([1, val]), m)

    def: _get_C(self, matr, coord_num, val):                            # Возвращает C_x или C_y
        rows = np.vstack((matr[1], matr[coord_num]))
        m = np.hstack((rows[:, 1], rows[:, coord_num]))
        r = np.array([1, val])
        return np.matmul(np.matmul(r, m), np.transpose(m))[0, 0]

    def _get_z_coefs(self, coord):                                      # Возвращает коэффициенты из неравенства, вытекающего из ограничения по z
        matr = np.hstack((self.o, self.a, self.b, self.c))
        v = [matr[2, ]]
        return np.hstack((v[:, 1:coord_num], v[:, coord_num + 1:]))

    def _get_z_const(self, coord, val):                                       # Возвращает константы из неравенства, вытекающего из ограничения по z
        matr = np.hstack((self.o, self.a, self.b, self.c))
        v = [matr[2, ]]
        const = v[0] + v[coord] * val
        return np.array([[1 - const], [-const]])

    def _get_cyl_axis_cross_plane(self, coord, val)             # Находим координаты (внутренние для параллелепипеда)
                                                                # пересечения оси Oz с гранью
        matr = np.hstack((self.o, self.a, self.b, self.c))
        rows = matr[:2]
        left = rows[:,1:]
        right =  - rows[:, 0]
        left_last = np.array([[0, 0, 0]])
        left_last[0, coord - 1] = 1
        left = np.vstack((left, left_last))
        right = np.vstack((right, np.array([[val]])))
        r = la.solve(left, right)                       # Находим координаты (внутренние для параллелепипеда) пересечения оси и грани
        r = np.delete(r, cond - 1, 0)                   # Удаляем константную координату
        return r

    def get_tasks(self):                                    # Постановка задач оптимизации на гранях
                                                            # Названия - как в описании
        X_4 = self._get_X_4()
        Y_4 = self._get_Y_4()
        tasks = []
        for coord in (1, 2, 3):                             # Описание всех граней: каждая грань - пара из номера
            for val in (0., 1.):                            # внутренней координаты, обращенной в константу, и константы (0 или 1)
                M = self._get_2_projection(X_4, coord) + self._get_2_projection(Y_4, coord)
                b = self._get_b(X_4, coord, val) + self._get_b(Y_4, coord, val)
                C = 1 - self._get_C(X_4, coord, val) - self._get_b(Y_4, coord, val)
                conds = np.vstack((np.eye(2), -np.eye(2)))
                cond_const = np.transpose(np.array([1, 1, 0, 0]))  # Задаем ограничения по изменяющимся внутренним координатам
                conds = np.vstack((conds, self._get_z_coefs(coord), -self._get_z_coefs(coord)))
                cond_const = np.vstack((cond_const, self._get_z_const(coord, val))) # Задаем ограничения по z
                r = self(coord, val)    # Находим координаты пересечения
                tasks.append((M, b, conds, cond_const, C, r))          # Добавляем кортеж, задающий систему неравенств, наличие решения равнозначно наличию пересечения грани и цилиндра

        return tasks

    def check_begin_inside(self):                             # Проверяем принадлежность точки (0, 0, 0) параллелограмму
        matr = np.hstack((self.a, self.b, self.c))
        r = np.solve(matr, -self.o)
        return np.all(r <= 1) and np.all(r >=0)