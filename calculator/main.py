from src import calc

def main():
    x = float(input("Ingrese el primer numero: "))
    operador = input("Ingrese el operador (+, -, *, /): ")
    y = float(input("Ingrese el segundo numero: "))
    try:
        result = calc.calculate(x,y,operador)
        print(f'El resultado es: {result}')
    except ZeroDivisionError:
        print("No se puede dividir por 0")

if __name__ == "__main__": 
    main()
