from src import calc

def main():
    x = float(input("Ingrese el primer numero: "))
    operador = input("Ingrese el operador (+, -, *, /): ")
    y = float(input("Ingrese el segundo numero: "))
    result = calc.calculate(x,y,operador)
    print(f'El resultado es: {result}')

if __name__ == "__main__": 
    main()