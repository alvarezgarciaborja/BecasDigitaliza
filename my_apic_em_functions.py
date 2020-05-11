#!/usr/bin/env python3

import json
import requests
from tabulate import *

def banner():

    print("""
    ##############################################
            Script de conexión a APIC-EM 

       Realizado por: Borja Álvarez García

            Becas Digitaliza Cisco 2020
            Curso: DEVNET

    ==============================================
    """)


def opciones():

    opcion = input("""
    Opciones disponibles:
    ----------------------------------------------
    1 ) Imprimir hosts
    2 ) Imprimir dispositivos
    3 ) Geolocolizar Ip
    4 ) Solicitar Ticket de servicio
    
    0 ) Salír

    Por favor, introduce la opción a realizar: """)

    return opcion


def get_ticket():

    requests.packages.urllib3.disable_warnings()
    api_url = "https://sandboxapicem.cisco.com/api/v1/ticket"

    headers = {
        "content-type": "application/json"
    }

    body_json = {
        "username": "devnetuser",
        "password": "Cisco123!"
    }

    resp = requests.post(api_url,json.dumps(body_json),headers=headers,verify=False)

    
    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"]
    
    return serviceTicket


def print_hosts():

    api_url = "https://sandboxapicem.cisco.com/api/v1/host"
    ticket = get_ticket()

    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }

    resp = requests.get(api_url, headers=headers, verify=False)
    

    if resp.status_code != 200:
        raise Exception("El código de estado no es igual a 200. La respuesta es: " + resp.text )

    response_json = resp.json()

    host_list = []
    i = 0
    for item in response_json["response"]:
        i+=1
        host = [
            i,
            item["hostType"],
            item["hostIp"]
        ]
        host_list.append( host )

    table_header = ["Número", "Tipo", "IP"]
    print("")
    print(tabulate(host_list, table_header))


def print_devices():

    api_url = "https://sandboxapicem.cisco.com/api/v1/network-device"
    ticket = get_ticket()

    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }

    resp = requests.get(api_url, headers=headers, verify=False)
    

    if resp.status_code != 200:
        raise Exception("El código de estado no es igual a 200. La respuesta es: " + resp.text )

    response_json = resp.json()

    host_list = []
    i = 0
    for item in response_json["response"]:
        i+=1
        host = [
            i,
            item["type"],
            item["managementIpAddress"]
        ]
        host_list.append( host )

    table_header = ["Número", "Modelo", "IP"]
    print("")
    print(tabulate(host_list, table_header))


def geoip():

    dirip = input("Introduzca la dirección Ip (x.x.x.x): ")


    api_url = "https://sandboxapicem.cisco.com/api/v1/ipgeo/" + dirip
    ticket = get_ticket()

    headers = {
        "content-type": "application/json;charset=UTF-8",
        "X-Auth-Token": ticket
    }

    resp = requests.get(api_url, headers=headers, verify=False)
   

    if resp.status_code != 200:
        raise Exception("La ip que has introducido no es válida!! Revisa el formato.")

    response_json = resp.json()

    ciudad = response_json["response"][dirip]["city"]
    pais = response_json["response"][dirip]["country"]
    latitud = response_json["response"][dirip]["latitude"]
    longitud = response_json["response"][dirip]["longitude"]



    print('\nLa Ip ', dirip, 'se encuentra en ',ciudad,'(',pais,')\n')
    print('Latitud: ', latitud, ' y longitud ', longitud, '\n')

#Comienzo del script
#------------------------------------------------------------------------------------------
banner()

op = 1
while op > 0:
    
    opcion = opciones()
    if opcion == "1":
        print_hosts()
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
   
    elif opcion == "2":
        print_devices()
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)

    elif opcion == "3":
        geoip()
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
            
    elif opcion == "4":
        print("\n El tiquet generado es: "+ get_ticket())
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
           



