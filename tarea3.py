import sympy as sp
import random

# Verifica si la posicion es válida


def posicion_valida(n, m, dim):
    # n: es la fila
    # m: es la columna
    # dim: dimension de la matriz

    if n is None or m is None or dim is None:
        print("Faltan parametros")
        return

    if dim < 0:
        print("Dimensión tiene que ser mayor que 0.")
        return

    if (n >= 0 and n < dim) and (m >= 0 and m < dim):
        return True
    return False


# Obtiene las posiciones que afecta una determinada posicion en la matriz
def posiciones_afectadas(n, m, dim):
    # n: es la fila
    # m: es la columna
    # dim: dimension de la matriz
    if n is None or m is None or dim is None:
        print("Faltan parametros")
        return

    if n < 0 or m < 0 or dim < 0:
        print("Los parametros tienen que ser mayores que 0. 2")
        return

    posiciones = [[n, m], [n, m - 1], [n - 1, m], [n + 1, m], [n, m + 1]]

    validas = []
    for pos in posiciones:
        if posicion_valida(pos[0], pos[1], dim):
            validas.append(pos)
    return validas


# Genera la ecuacion de posiciones afectadas para una determinada posicion de la matriz.
def generar_posiciones_afectada(n, m, dim, posiciones):
    # Esto se debe a que la ecuacion debe tener un 0 si la posicion no es afectada y un 1 si lo es.
    # n: es la fila
    # m: es la columna
    # dim: dimension de la matriz (se supone que es cuadrada)
    # posiciones: son todas las posiciones posibles de la matriz
    if n is None or m is None or dim is None or posiciones is None:
        print("Faltan parametros")
        return

    if n < 0 or m < 0 or dim < 0:
        print("Los parametros tienen que ser mayores que 0.")
        return

    fila = []
    afectadas = posiciones_afectadas(n, m, dim)
    for pos in posiciones:
        if pos in afectadas:
            fila.append(1)
        else:
            fila.append(0)
    return fila


# Para generar las matrices de prueba
def generar_matriz_invertible(N):
    while True:
        matriz = sp.Matrix(N, N, lambda i, j: random.randint(0, 1))

        # Verificar si el determinante es distinto que 0
        if matriz.det() != 0:
            return matriz


# Transforma la solución de 1 y 0 a posiciones que se deben apretar para apagar las luces
def obtener_posicion(solucion):
    posicion = 0
    apagar = []
    # Para cada valor en la solucion, si es un 1, agregar esa posicion a apagar. .
    for x in solucion:
        posicion += 1
        valor = str(x)
        valor = int(valor)
        if valor != 0:
            apagar.append(posicion)
    return apagar


# Imprime la matriz en lineas distintas
def imprimir_matriz(matriz):
    if matriz is None or len(matriz) == 0:
        return

    matriz = sp.Matrix(matriz)
    for row in matriz.tolist():  # Convert matrix to a list of lists
        print(row)


# Resuelve el sistema de ecuaciones y devuelve la matriz
def generar_solucion(matriz):
    # matriz: es la matriz inicial, con 0 o 1

    if matriz is None:
        print("La matriz es nula")
        return
    matriz = sp.Matrix(matriz)
    if matriz.shape[0] != matriz.shape[1]:
        print("La matriz no es cuadrada")
        return

    posiciones = []  # todas las posiciones de la matriz
    vector_b = []
    # se obtiene la dimensión.
    dim = matriz.shape[0]
    matriz_ecuacion = []
    # genera todas las posiciones de la matriz
    for i in range(dim):
        for j in range(dim):
            posiciones.append([i, j])
    # para cada posicion de la matriz, genera la ecuacion que afecta a esa posicion y agrega al vector_b el valor de esa posicion de la matriz
    for pos in posiciones:
        matriz_ecuacion.append(generar_posiciones_afectada(
            pos[0], pos[1], dim, posiciones))
        vector_b.append(matriz[pos[0], pos[1]])

    return eliminacion_gauss(matriz_ecuacion, vector_b)


# Resuelve el sistema de ecuaciones usando suma binaria
def eliminacion_gauss(matriz, vector_b):
    # matriz: la matriz de movimientos
    # vector_b: es el vector con el valor de cada posicion de la matriz original
    try:
        if matriz is None or vector_b is None:
            print("Faltan parametros")
            return

        # Transforma la matriz y vector_b en matrices
        b = sp.Matrix(vector_b)
        A = sp.Matrix(matriz)

        if b.shape[1] > 1 or b.shape[0] != A.shape[0]:
            print("El vector constante tiene tamano incorrecto")
            return

        # Cantidad de filas de la matriz
        n = A.shape[0]

        # Crea la matriz extendida juntando la matriz con el vector_b
        extendida = A.row_join(b)

        # Cantidad de filas de la matriz extendida
        filas = extendida.shape[0]

        # Hace la eliminación de las posiciones de la matriz
        for i in range(n):
            # Verifica que la matriz en esa posicion no sea 0, y si lo es, intercambia esa fila por una que no lo es, que va
            # a ser la fila que se va a usar como pivote
            if extendida[i, i] == 0:
                for j in range(i + 1, filas):
                    if extendida[j, i] == 1:
                        extendida.row_swap(i, j)
                        break

            # Para todas las filas abajo de la fila pivote, si tienen un uno en la posicion [j,i], entonces se suma la fila del pivote
            # con la fila actual, y se realiza el modulo 2 para que sea una suma binaria
            for j in range(i + 1, filas):
                if extendida[j, i] == 1:
                    extendida.row_op(j, lambda x, _: (x + extendida[i, _]) % 2)

        # Crea un arreglo solo con ceros del mismo tamaño que la matriz
        solucion = [0] * n
        for i in range(n - 1, -1, -1):
            # Calcula cada elemento de la solucion restandole la suma de los valores de la derecha del pivote y haciendole el modulo 2
            solucion[i] = (extendida[i, -1] - sum(extendida[i, k] *
                                                  solucion[k] for k in range(i + 1, n))) % 2

        return solucion
    except:
        print("Falló la escalarización")
        return


def main():

    matriz = [[0, 1, 0],
              [0, 0, 0],
              [0, 0, 0]]

    """
    matriz = [[0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]]
    """
    """
    matriz = [[0, 1, 1, 1, 1],
            [1, 0, 1, 1, 0],
            [0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1]]

    matriz = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 1, 0]
    ]
    """

    n = sp.Matrix(matriz).shape[0]
    print("Matriz original: ")
    imprimir_matriz(matriz)
    solucion = generar_solucion(matriz)
    matriz = sp.Matrix(matriz)

    if matriz.shape[0] == matriz.shape[1] and solucion is not None:
        print("Solucion como vector: ", solucion)
        print("Solucion como matriz: ")
        imprimir_matriz(sp.Matrix(solucion).reshape(n, n))
        print("Posiciones a presionar: ", obtener_posicion(solucion))


def generar_matriz(n):
    return sp.Matrix(n, n, lambda i, j: random.randint(0, 1))


if __name__ == "__main__":

    main()


