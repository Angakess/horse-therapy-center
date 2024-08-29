from src import calculator

def main():
    x = float(input("Ingrese el primer numero: "))
    operador = input("Ingrese el operador (+, -, *, /): ")
    y = float(input("Ingrese el segundo numero: "))
    result = calculator.calculate(x,y,operador)
    print("El resultado es: {result}")

if __name__ == "__main__": 
    main()