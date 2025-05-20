def create_spiral_matrix(size):
    matrix = [[0] * size for _ in range(size)]
    return matrix

def fill_fibonacci_spiral(matrix, n):
    a, b = 0, 1
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix) - 1
    direction = 0  # 0: left to right, 1: top to bottom, 2: right to left, 3: bottom to top
    
    while n > 0:
        if direction == 0:
            for i in range(left, right + 1):
                if n > 0:
                    matrix[top][i] = a
                    a, b = b, a + b
                    n -= 1
            top += 1
        elif direction == 1:
            for i in range(top, bottom + 1):
                if n > 0:
                    matrix[i][right] = a
                    a, b = b, a + b
                    n -= 1
            right -= 1
        elif direction == 2:
            for i in range(right, left - 1, -1):
                if n > 0:
                    matrix[bottom][i] = a
                    a, b = b, a + b
                    n -= 1
            bottom -= 1
        elif direction == 3:
            for i in range(bottom, top - 1, -1):
                if n > 0:
                    matrix[i][left] = a
                    a, b = b, a + b
                    n -= 1
            left += 1
        direction = (direction + 1) % 4

def print_spiral_matrix(matrix):
    for row in matrix:
        print(" ".join(str(x) for x in row))

# Parámetros
size = 5  # Tamaño de la matriz (5x5, por ejemplo)
num_terminos = size * size  # Número de términos de Fibonacci a imprimir

# Crear y llenar la matriz en forma de espiral
spiral_matrix = create_spiral_matrix(size)
fill_fibonacci_spiral(spiral_matrix, num_terminos)

# Imprimir la matriz en forma de espiral
print_spiral_matrix(spiral_matrix)


