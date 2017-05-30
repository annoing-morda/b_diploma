import numpy as np;
from numpy import linalg as la

def calculate_form_value(M, b, vec):
    return np.transpose(vec) * M * vec + np.transpose(b) * vec

def solve_1dim(M, b, cond, cond_const, cond_eq, cond_eq_const):
    eq_index = 0
    free_index = 1
    M_diff = 2 * M
    b_diff = -b

    if cond_eq[0] == 0:
        eq_index = 1
        free_index = 0

    M_diff[eq_index] = cond_eq
    b[eq_index, 0] = cond_eq_const

    linear_global_min = la.solve(M_diff, b)
    conditions_check = np.matmul(cond, global_min)

    inside = np.all(np.less_equal(conditions_check, cond_const))
    if inside:      # Minimum is on edge
        return (linear_global_min, calculate_form_value(linear_global_min))
    else:           # Check vertexes
        minval = 100
        minvert = np.array([[-1000], [-1000]])
        for i in b.shape[0]:
            A_matr = np.vstack(cond_eq, M[i])
            if la.det(A_matr) != 0:
                b_matr = np.array(cond_eq_const, b[i, 0])
                vertex = la.solve(A_matr, b_matr)
                vert_val = calculate_form_value(M, b, vertex)
                if vert_val < minval:
                    minval = vert_val
                    minvert = vertex
        return(minvert, minval)


def solve_2dim(M, b, cond, cond_const):  # Here we minimize function M(x, x) - bx with conditions described in c
                                    # condition is c*x <= cond_const and describes a polygon.
    global_min = la.solve(2 * M, -b)
    conditions_check = np.matmul(cond, global_min)
    inside = np.all(np.less_equal(conditions_check, cond_const))
    if inside:
        return (global_min, calculate_form_value(M, b, global_min))
    minval = 100
    minpoint = np.array([[-1000], [-1000]])
    for i in cond_const.shape[0]:
        (curval, curpoint) = solve_1dim(M, b, np.delete(cond, i), np.delete(cond, i))




print(solve_2dim(np.array([[0, 1], [1, 0]]), 
    np.array([[1], [2]]), 
    np.array([[1, 0], [0, 1]]),
    np.array([[-2], [-2]]) ))