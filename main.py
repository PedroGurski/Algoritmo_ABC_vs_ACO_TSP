import sys

# sys.argv é uma lista com os argumentos passados pelo terminal
# argv[0] = nome do arquivo (main.py)
# argv[1] = primeiro argumento
# argv[2] = segundo argumento

if len(sys.argv) < 3:
    print("Uso: python3 main.py num1 num2")
    sys.exit(1)

# Captura e converte para inteiro
a = int(sys.argv[1])
b = int(sys.argv[2])

# Operação desejada
resultado = a + b

print(resultado)
