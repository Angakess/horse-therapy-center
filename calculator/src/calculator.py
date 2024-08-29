from calculator.src import operations


def calculate(a, b, op):
    if op == "+":
        return operations.suma(a,b)
    elif op == "-":
        print("Sin implementar")
    elif op == "*":
        print("Sin implementar")
    elif op == "/":
        print("Sin implementar")
    else:
        raise(ValueError(f"Operador no valido: {op}"))