
#!/usr/bin/env python3

import math

def banner():
    print("""
    ##############################################
                    CALCULADORA

       Realizada por: Borja Álvarez García

            Becas Digitaliza Cisco 2020
            Curso: DEVNET

    ==============================================
    """)


def opciones():
    operacion = input("""
    Opciones disponibles:
    ----------------------------------------------
    + ) suma
    - ) resta
    * ) multiplicación
    / ) division
    e ) exponencial
    r ) raíz cuadrada
    
    0 ) Salír

    Por favor, introduce la operación a realizar: """)

    return operacion
    

def suma():
    num1 = int(input("Introduce el primer dígito: "))
    num2 = int(input("Introduce el segundo dígito: "))
    resultado = str(num1 + num2)
    print("\n{} + {} = ".format(num1, num2) + resultado)


def resta():
    num1 = int(input("Introduce el primer dígito: "))
    num2 = int(input("Introduce el segundo dígito: "))
    resultado = str(num1 - num2)
    print("\n{} - {} = ".format(num1, num2) + resultado)


def multiplicacion():
    num1 = int(input("Introduce el primer dígito: "))
    num2 = int(input("Introduce el segundo dígito: "))
    resultado = str(num1 * num2)
    print("\n{} * {} = ".format(num1, num2) + resultado)


def division():
    num1 = int(input("Introduce el primer dígito: "))
    num2 = int(input("Introduce el segundo dígito: "))

    while num2 == 0:
        print("No se puede dividir entre 0 !!!! \n")
        num2 = int(input("Por favor, introduce otro dígito: "))

    resultado = str(num1 / num2)
    print("\n{} / {} = ".format(num1, num2) + resultado)


def exponencial():
    num1 = int(input("Introduce el primer dígito: "))
    num2 = int(input("Ahora introduce el exponente: "))
    resultado = str(num1 ** num2)
    print("\n{} elevado a {} = ".format(num1, num2) + resultado)


def raiz_cuadrada():
    num = int(input("Introduce el número del que quieras saber su raíz cuadrada: "))
    resultado = math.sqrt(num)
    print("\n La raíz cuadrada de", num, "es: ", resultado)


#Comienzo del script
#------------------------------------------------------------------------------------------
banner()

op = 1
while op > 0:
    
    operacion = opciones()
    if operacion == "+":
        suma()
        print("\nDesea realizar otra operación? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
   
    elif operacion == "-":
        resta()
        print("\nDesea realizar otra operación? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)

    elif operacion == "*":
        multiplicacion()
        print("\nDesea realizar otra operación? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)

    elif operacion == "/":
        division()
        print("\nDesea realizar otra operación? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)

    elif operacion == "e":
        exponencial()
        print("\nDesea realizar otra operación? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)

    elif operacion == "r":
        raiz_cuadrada()
        print("\nDesea realizar otra operación? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)

    elif operacion == "0":
        break
    
    else:
        print("\n------------------------------------------------------------------")
        print("La entrada no corresponde a ninguna operación. Fíjate en el menú!!!")
        print("-------------------------------------------------------------------")

    
