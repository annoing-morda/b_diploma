import numpy as np
import geometry as geom
from numpy import linalg as la
from quadr_programming import solve_2dim

def read_vector():                  # Ввод координат вектора в 3м пространстве
    inp = input()
    coords = inp.split(' ')         # Координаты вводятся через пробел
    if len(coords) != 3:            # Если меньше трех координат,
                                    # дать еще попытку
        print('Must be 3 coords, try again')
        return(read_vector())
    vec = []
    for i in range(3):
        x = float(coords[i])
        vec += [[x]]            # Преобразуем к столбцу
    return np.array(vec)

c = geom.cylinder(read_vector(), read_vector(), read_vector(), read_vector())
# Считываем цилиндр
if not c.check():   # Проверяем корректность задания цилиндра
    print("Incorrect cylinder, exiting")
    exit()
p = geom.parallelogram(read_vector(),
 read_vector(), read_vector(), read_vector())
# Считываем параллелограмм
if not p.check():   # Проверяем корректность задания параллелограмма
    print("Incorrect parallelogram, exiting")
    exit()
p.transform(c.get_matrix(), c.get_translation())
    # Проводим преобразование базиса

tasks = p.get_tasks()   # Решаем задачу на гранях
for task in tasks:
    if solve_2dim(task):
        print("Cross found")
        exit()

if p.check_begin_inside():  # Если на гранях пересечения не нашли,
                            # проверяем вложенность
    print("Cross found")
    exit()

print("Cross not found")    # Если и вложенности нет, пересечений нет вообще
