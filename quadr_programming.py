import numpy as np
import geometry as geom
from numpy import linalg as la

def calculate_form_value(M, b, vec):
                # Подсчет значения формы M(x,x) - b(x) на векторе vec
    res = np.dot(np.transpose(vec),
    np.dot(M, vec)) + np.dot(np.transpose(b), vec)
    try :
        return res[0, 0]
    except IndexError:
        return res

def solve_1dim(M, b, cond, cond_const, cond_eq, cond_eq_const):
    eq_index = 0
    free_index = 1
    M_diff = 2 * M
    b_diff = -b

    if cond_eq[0] == 0:
        eq_index = 1
        free_index = 0

    M_diff[eq_index] = cond_eq
    b[eq_index] = cond_eq_const
    force_vert_check = False
    if la.det(M_diff) == 0: # На прямой расстояние до оси может  не меняться
         # В этом случае минимум - форма на какой-нибудь точке отрезка
        force_vert_check = True  # Например, на вершине
    else:
        linear_global_min = la.solve(M_diff, b)
    # Ищем минимум на прямой, содержащей ребро
        conditions_check = np.matmul(cond, linear_global_min)
        inside = np.all(np.less_equal(conditions_check, cond_const))
        if inside:      # Проверяем, что минимум лежит внутри ребра
            return (linear_global_min, calculate_form_value(M, b, linear_global_min))
               # Проверяем вершины
    minval = 100
    minvert = np.array([[-1000], [-1000]])
    for i in range(b.shape[0]):
        A_matr = np.vstack((cond_eq, M[i]))
        if la.det(A_matr) != 0:
            b_matr = np.array([[cond_eq_const], [b[i]]])
            vertex = la.solve(A_matr, b_matr)
            conditions_check = np.matmul(cond, vertex)
                # Проверяем, что отобранная точка действительно вершина
            inside = np.all(np.less_equal(conditions_check, cond_const))
            if inside:
                vert_val = calculate_form_value(M, b, vertex)
                if vert_val < minval:
                    minval = vert_val
                    minvert = vertex
    return(minvert, minval)

def solve_2dim(task):
    # Минимизируем функция M(x, x) - bx на ребрах многоугольника, заданной
    # условиями cond*x <= cond_const, сравниваем минимум с константой C
    # Проверяем, не попал ли центр эллипса внутрь многоугольника.
    (M, b, cond, cond_const, C, r) = task
    minval = 100
    minpoint = np.array([[-1000], [-1000]])
    for i in range(cond_const.shape[0]):
        (curpoint, curval) = solve_1dim(M, b,
            np.delete(cond, i, 0), np.delete(cond_const, i, 0),
            cond[i], cond_const[i, 0] )     # Ищем минимум на ребре
        if curval < minval:
            minval = curval
            minpoint = curpoint
            # Устанавливаем минимум на всех ребрах
    if minval <= C:
        # Если минимум на ребрах нас устроил, сообщаем о наличии пересечения
        return True

    if type(r) == type(0):  # Если ось Oz параллельна плоскости многоугольнка,
                # все возможные проверки уже пройдены.
        return False
    conditions_check = np.matmul(cond, r)
    # Проверяем принадлежность центра внутренности многоугольника
    center_inside = np.all(np.less_equal(conditions_check, cond_const))
    return center_inside
