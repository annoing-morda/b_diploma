import numpy as np
import geometry as geom
from numpy import linalg as la

def read_vector():                  # Ввод координат вектора в 3м пространстве
    inp = input()
    coords = inp.split(' ')         # Координаты вводятся через пробел
    if len(coords) != 3:            # Если меньше трех координат, дать еще попытку
        print('Must be 3 coords, try again\n')
        return(read_vector())
    vec = []
    for i in range(3):
        x = float(coords[i])
        vec += [[x]]            # Преобразуем к столбцу
    return np.array(vec)

def _get_2_projection(matr, coord_num):                       # Возвращает X_2 или Y_2
    rows = np.vstack((matr[1:coord_num], matr[coord_num + 1:]))
    m = np.hstack((rows[:, 1:coord_num], rows[:, coord_num + 1:]))
    return m


#c = geom.cylinder(read_vector(), read_vector(), read_vector(), read_vector())
#p = geom.parallelogram(read_vector(), read_vector(), read_vector(), read_vector())
#print(c.check())
#p.transform(c.get_matrix(), c.get_translation())
#p.dbg_prn()
#print(p._get_X_4())
#p.get_tasks()
