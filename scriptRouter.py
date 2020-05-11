#!/usr/bin/env python3

import json, requests
from netmiko import ConnectHandler
from tabulate import *
from ncclient import manager
import xml.dom.minidom
import xmltodict
requests.packages.urllib3.disable_warnings()



def banner():
    
    print("""
    ##############################################
              Script Router CSR100V

       Realizado por: Borja Álvarez García

            Becas Digitaliza Cisco 2020
            Curso: DEVNET

    ==============================================
    """)


def opciones():

    opcion = input("""
    Opciones disponibles:
    ----------------------------------------------
    1 ) Obtener un listado de interfaces
    2 ) Crear interfaces
    3 ) Borrar interfaces
    4 ) Obtener la tabla de routing
    5 ) Petición al modulo ietf-routing.yang
    6 ) Petición al módulo ietf-yang-library.yang
    
    0 ) Salír

    Por favor, introduce la opción a realizar: """)

    return opcion


def listInterfaces(direccion, usuario, password):
   
    api_url = "https://"+direccion+"/restconf/data/ietf-interfaces:interfaces"
    api_url2 = "https://"+direccion+"/restconf/data/ietf-interfaces:interfaces-state"
   
    headers = {
        "Accept": "application/yang-data+json",
        "Content-type": "application/yang-data+json"
    }

    basic_auth = (usuario,password)

    resp = requests.get(api_url, auth=basic_auth, headers=headers, verify=False)
    resp_json = resp.json()

    resp2 = requests.get(api_url2, auth=basic_auth, headers=headers, verify=False)
    resp2_json = resp2.json()

    int_list = []
    i = 0
    for item in resp_json["ietf-interfaces:interfaces"]["interface"]:
        i += 1
        interfaces = [
            i,
            item["name"],
            item["description"],         
        ]
        int_list.append(interfaces)

    int_list2 =[]
    for item in resp2_json["ietf-interfaces:interfaces-state"]["interface"]:
        interface = [
            item["phys-address"],
        ]
        int_list2.append(interface)

    int_list3 = []  
    for i, w in enumerate(int_list):
        int_list3.append(int_list[i] + int_list2[i])

    table_header = ["Número", "Nombre", "Descripción", "Mac"]

    print("\nEstas son las Interfaces actuales: ")
    print()
    print(tabulate(int_list3, table_header))


def listRutas(direccion, usuario, password):
    
    sshCli = ConnectHandler(
    device_type='cisco_ios',
    host=direccion,
    port=22,
    username=usuario,
    password=password
    )   

    output = sshCli.send_command("show ip route")
    print("La tabla de rutas es: \n{}\n".format(output))


def crearInterface(direccion, usuario, password):

    print("Vamos a proceder a crear una interfaz Loopback")
    numInt = input("Introduzca el número que le quiere dar a la nueva interfaz: ")

    api_url = "https://"+direccion+"/restconf/data/ietf-interfaces:interfaces/interface=Loopback" + numInt

    headers = {
        "Accept": "application/yang-data+json",
        "Content-type": "application/yang-data+json"
    }

    basic_auth = (usuario,password)

    yangConfiguration = {
        "ietf-interfaces:interface": {
            "name": "Loopback"+numInt,
            "description": "WHATEVER"+numInt,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": numInt+"."+numInt+"."+numInt+"."+numInt,
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(api_url, data=json.dumps(yangConfiguration), auth=basic_auth, headers=headers, verify=False)


def delInterface(direccion, usuario, password):
    
    sshCli = ConnectHandler(
    device_type='cisco_ios',
    host=direccion,
    port=22,
    username=usuario,
    password=password
    )   

    output = sshCli.send_command("show ip int brief")
    print("\nEstas son las interfaces actuales:\n{}\n".format(output))
    interface = (input("\nIntroduzca el nombre de la Interfaz que desea borrar: "))

    api_url = "https://"+direccion+"/restconf/data/ietf-interfaces:interfaces/interface=" + interface

    headers = {
        "Accept": "application/yang-data+json",
        "Content-type": "application/yang-data+json"
    }

    basic_auth = (usuario,password)

    resp = requests.delete(api_url, auth=basic_auth, headers=headers, verify=False)


def modulo1(direccion, usuario, password):
    
    m = manager.connect (
    host=direccion,
    port=830,
    username=usuario,
    password=password,
    hostkey_verify=False
    )

    prueba_filter = """
    <filter>
        <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>
    </filter>
    """

    netconf_reply = m.get(filter = prueba_filter)
    netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


def modulo2(direccion, usuario, password):
    
    m = manager.connect (
    host=direccion,
    port=830,
    username=usuario,
    password=password,
    hostkey_verify=False
    )

    prueba_filter = """
    <filter>
        <modules-state xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-library"/>
    </filter>
    """

    netconf_reply = m.get(filter = prueba_filter)
    netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())




#Comienzo del script
#-------------------------------------------------------------------------------------------
banner()

direccion = input("\nPor favor, introduce la Ip del router: ")
usuario = input("\n Introduce el usuario: ")
password = input("\n Por último, introduce el password: ")

op = 1
while op > 0:
    
    opcion = opciones()
    if opcion == "1":
        listInterfaces(direccion, usuario, password)
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
   
    elif opcion == "2":
        crearInterface(direccion, usuario, password)
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
    elif opcion == "3":
        delInterface(direccion, usuario, password)
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
    elif opcion == "4":
        listRutas(direccion, usuario, password)
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
    elif opcion == "5":
        modulo1(direccion, usuario, password)
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
    elif opcion == "6":
        modulo2(direccion, usuario, password)
        print("\nDesea escoger otra opción? ")
        parar = input("Pulsa 0 para salir o cualquier tecla para continuar: ")
        if parar == "0":
            op = int(parar)
    elif opcion == "0":
        break
    else:
        print("\n------------------------------------------------------------------")
        print("La entrada no corresponde a ninguna opción. Fíjate en el menú!!!")
        print("-------------------------------------------------------------------")

