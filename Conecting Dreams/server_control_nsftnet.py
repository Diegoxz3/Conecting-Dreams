import json
import socket
import threading
import time
import networkx as nx
from cryptography.fernet import Fernet
import os


clave = '86587XYNFG_FDpNaFoqZNa5MUd-TygrIMCas0XWfWMI='
fernet = Fernet(clave)

# Definir la red
nsfnet = nx.Graph()
nsfnet.add_node(('127.0.0.1', 12001))  # WA  Puerto 12001
nsfnet.add_node(('127.0.0.1', 12002))  # CA1  Puerto 12002
nsfnet.add_node(('127.0.0.1', 12003))  # CA2 Puerto 12003
nsfnet.add_node(('127.0.0.1', 12004))  # UT Puerto 12004
nsfnet.add_node(('127.0.0.1', 12005))  # CO Puerto 12005
nsfnet.add_node(('127.0.0.1', 12006))  # TX Puerto 12006
nsfnet.add_node(('127.0.0.1', 12007))  # NE Puerto 12007
nsfnet.add_node(('127.0.0.1', 12008))  # IL Puerto 12008
nsfnet.add_node(('127.0.0.1', 12009))  # PA Puerto 12009
nsfnet.add_node(('127.0.0.1', 120010))  # GA Puerto 12010
nsfnet.add_node(('127.0.0.1', 12011))  # MI Puerto 12011
nsfnet.add_node(('127.0.0.1', 12012))  # NY Puerto 12012
nsfnet.add_node(('127.0.0.1', 12013))  # NJ Puerto 12013
nsfnet.add_node(('127.0.0.1', 12014))  # DC Puerto 12014

for link in [
    (('127.0.0.1', 12001), ('127.0.0.1', 12002), 2100), (('127.0.0.1', 12001), ('127.0.0.1', 12003), 3000), (('127.0.0.1', 12001), ('127.0.0.1', 12008), 4800),
    (('127.0.0.1', 12002), ('127.0.0.1', 12001), 2100), (('127.0.0.1', 12002), ('127.0.0.1', 12003), 1200), (('127.0.0.1', 12002), ('127.0.0.1', 12004), 1500),
    (('127.0.0.1', 12003), ('127.0.0.1', 12001), 3000), (('127.0.0.1', 12003), ('127.0.0.1', 12002), 1200), (('127.0.0.1', 12003), ('127.0.0.1', 12006), 3600),
    (('127.0.0.1', 12004), ('127.0.0.1', 12002), 1500), (('127.0.0.1', 12004), ('127.0.0.1', 12005), 1200), (('127.0.0.1', 12004), ('127.0.0.1', 12011), 3900),
    (('127.0.0.1', 12005), ('127.0.0.1', 12004), 1200), (('127.0.0.1', 12005), ('127.0.0.1', 12006), 2400), (('127.0.0.1', 12005), ('127.0.0.1', 12007), 1200),
    (('127.0.0.1', 12006), ('127.0.0.1', 12003), 3600), (('127.0.0.1', 12006), ('127.0.0.1', 12005), 2400), (('127.0.0.1', 12006), ('127.0.0.1', 12010), 2100), (('127.0.0.1', 12006), ('127.0.0.1', 12014), 3600),
    (('127.0.0.1', 12007), ('127.0.0.1', 12005), 1200), (('127.0.0.1', 12007), ('127.0.0.1', 12008), 1500), (('127.0.0.1', 12007), ('127.0.0.1', 12010), 2700),
    (('127.0.0.1', 12008), ('127.0.0.1', 12001), 4800), (('127.0.0.1', 12008), ('127.0.0.1', 12007), 1500), (('127.0.0.1', 12008), ('127.0.0.1', 12009), 1500),
    (('127.0.0.1', 12009), ('127.0.0.1', 12008), 1500), (('127.0.0.1', 12009), ('127.0.0.1', 12010), 1500), (('127.0.0.1', 12010), ('127.0.0.1', 12012), 600), (('127.0.0.1', 12009), ('127.0.0.1', 12013), 600),
    (('127.0.0.1', 12010), ('127.0.0.1', 12006), 2100), (('127.0.0.1', 12010), ('127.0.0.1', 12007), 2700), (('127.0.0.1', 12010), ('127.0.0.1', 12009), 1500),
    (('127.0.0.1', 12011), ('127.0.0.1', 12004), 3900), (('127.0.0.1', 12011), ('127.0.0.1', 12012), 1200), (('127.0.0.1', 12011), ('127.0.0.1', 12013), 1500),
    (('127.0.0.1', 12012), ('127.0.0.1', 12009), 600), (('127.0.0.1', 12012), ('127.0.0.1', 12011), 1200), (('127.0.0.1', 12012), ('127.0.0.1', 12014), 600),
    (('127.0.0.1', 12013), ('127.0.0.1', 12009), 600), (('127.0.0.1', 12013), ('127.0.0.1', 12011), 1500), (('127.0.0.1', 12013), ('127.0.0.1', 12014), 300),
    (('127.0.0.1', 12014), ('127.0.0.1', 12006), 3600), (('127.0.0.1', 12014), ('127.0.0.1', 12012), 600), (('127.0.0.1', 12014), ('127.0.0.1', 12013), 300)
]:
    nsfnet.add_edge(*link[:2], weight=link[2])




def save_shortest_paths(network):
    shortest_paths = {}
    for node in network.nodes():
        ip, port = node[0], node[1]
        shortest_paths[f"{ip}_{port}"] = {}  # Convertir la clave de tupla a string
        for target_node in network.nodes():
            if node != target_node:
                try:
                    shortest_path = nx.shortest_path(network, source=node, target=target_node)
                    shortest_paths[f"{ip}{port}"][f"{target_node[0]}{target_node[1]}"] = shortest_path
                except nx.NetworkXNoPath:
                    pass

    for node, paths in shortest_paths.items():
        filename = f"{node}_routing_table.json"
        with open(filename, 'w') as f:
            json.dump(paths, f)


# Calcular y guardar los caminos más cortos en archivos JSON
save_shortest_paths(nsfnet)

# Dirección y puerto del servidor
server_address = ('127.0.0.1', 12015)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)
print("El servidor está en funcionamiento...")

# Diccionario para mapear puerto de cliente a nodo de la red
client_node_mapping = {}

# Diccionario para mapear nodo de router a dirección IP de cliente
router_client_mapping = {}

# Lista para mantener el estado de los clientes que han respondido
responded_clients = []

# Crear un objeto de bloqueo
lock = threading.Lock()

# Función para asignar un nodo de la red a un puerto de cliente
def assign_node(client_address):
    if len(client_node_mapping) == 14:
        print("Ya se han asignado nodos a los 4 puertos de los clientes.")
    else:
        nodes = list(nsfnet.nodes())
        node = nodes[len(client_node_mapping)]
        client_node_mapping[client_address] = node
        print(f"El puerto {client_address} está asociado al nodo {node}")

        # Envía la tabla de enrutamiento correspondiente al cliente recién conectado
        routing_table_filename = f"{node[0]}_{node[1]}_routing_table.json"
        if os.path.exists(routing_table_filename):  # Verificar si el archivo existe
            send_routing_table(client_address, routing_table_filename)
        else:
            print(f"Error: No se encontró el archivo de tabla de enrutamiento para {node}.")




# Función para enviar la tabla de enrutamiento a un cliente
def send_routing_table(client_address, routing_table_filename):
    with open(routing_table_filename, 'rb') as f:
        routing_table_data = f.read()
    server_socket.sendto(b'tablas de enrutamiento' + routing_table_data, client_address)  # Agregar la palabra clave antes de los datos de la tabla

# Función para enviar todas las tablas de enrutamiento a los clientes
def send_routing_tables():
    for client_address, node in client_node_mapping.items():
        routing_table_filename = f"{node[0]}_{node[1]}_routing_table.json"
        send_routing_table(client_address, routing_table_filename)

# Función para eliminar un nodo de la red
def remove_node(node):
    if node in nsfnet.nodes():
        # Eliminar el nodo de la red
        nsfnet.remove_node(node)
        print(f"Node {node} has been removed from the network.")

        # Eliminar cualquier enlace asociado al nodo
        nsfnet.remove_edges_from(list(nsfnet.edges(node)))
        print(f"Associated links to node {node} have been removed.")

        # Actualizar la tabla de enrutamiento
        save_shortest_paths(nsfnet)

        # Enviar las tablas de enrutamiento actualizadas a los clientes
        send_routing_tables()

    else:
        print(f"Node {node} not found in the network.")

# Función para eliminar un enlace de la red
def remove_link(node1, node2):
    if nsfnet.has_edge(node1, node2):
        # Eliminar el enlace de la red
        nsfnet.remove_edge(node1, node2)
        print(f"Enlace entre {node1} y {node2} ha sido eliminado de la red.")

        # Actualizar la tabla de enrutamiento
        save_shortest_paths(nsfnet)

        # Enviar las tablas de enrutamiento actualizadas a los clientes
        send_routing_tables()
    else:
        print(f"Enlace entre {node1} y {node2} no encontrado en la red.")



# Función para verificar el estado de los nodos y eliminarlos si no responden
def check_client_responses():
    while True:
        with lock:
            # Crear una copia del diccionario para evitar el RuntimeError
            client_node_mapping_copy = dict(client_node_mapping)

        for client_address in client_node_mapping_copy.keys():
            try:
                # Intentar enviar una solicitud ('ask') al cliente
                server_socket.sendto(b'ask', client_address)
            except OSError:
                # Si se produce un error al enviar, se considera que el enlace ha fallado
                print(f"El enlace con el cliente en el puerto {client_address} ha fallado.")
                node = client_node_mapping_copy.get(client_address)
                # Eliminar el nodo y sus enlaces vecinos
                remove_node_and_neighbors(node)
                del client_node_mapping[client_address]
                continue  # Ir al siguiente cliente

        # Esperar 5 segundos para que todos los clientes respondan con 'ok'
        time.sleep(5)

        with lock:
            # Verificar si algún cliente no respondió con 'ok'
            for client_address in client_node_mapping_copy.keys():
                if client_address not in responded_clients:
                    print(f"El cliente en el puerto {client_address} no respondió.")
                    node = client_node_mapping_copy.get(client_address)
                    remove_node(node)
                    del client_node_mapping[client_address]

            # Limpiar la lista de clientes que han respondido
            responded_clients.clear()

        # Esperar 10 segundos antes de volver a verificar el estado de los clientes
        time.sleep(10)

# Función para eliminar un nodo de la red y sus enlaces vecinos
def remove_node_and_neighbors(node):
    if node in nsfnet.nodes():
        # Obtener los enlaces vecinos del nodo
        neighbors = list(nsfnet.neighbors(node))
        # Eliminar el nodo de la red
        nsfnet.remove_node(node)
        print(f"Node {node} has been removed from the network.")
        # Eliminar los enlaces asociados al nodo y a sus vecinos
        for neighbor in neighbors:
            nsfnet.remove_edge(node, neighbor)
        print(f"Associated links to node {node} and its neighbors have been removed.")
        # Actualizar la tabla de enrutamiento
        save_shortest_paths(nsfnet)
        # Enviar las tablas de enrutamiento actualizadas a los clientes
        send_routing_tables()
    else:
        print(f"Node {node} not found in the network.")

# Hilo para verificar el estado de los nodos
thread_check_client_responses = threading.Thread(target=check_client_responses)
thread_check_client_responses.start()

# Función para recibir mensajes de los clientes y routers
def receive():
    while True:
        try:
            message, address = server_socket.recvfrom(1024)
            print(f"Mensaje recibido desde {address}: {message.decode()}")

            # Si el mensaje proviene de un router, actualizar la tabla de mapeo
            if address[0] in router_client_mapping:
                router_client_mapping[address[0]] = message.decode()
                print(f"Dirección IP del cliente asociada al router {address[0]} actualizada: {message.decode()}")
            else:
                port = address[1]
                if address not in client_node_mapping:
                    assign_node(address)
                else:
                    # Si el nodo ya está conectado, actualiza su tabla de enrutamiento
                    node = client_node_mapping.get(address)
                    routing_table_filename = f"{node[0]}_{node[1]}_routing_table.json"
                    send_routing_table(address, routing_table_filename)
                    responded_clients.append(address)  # Marcar el cliente como respondido

        except Exception as e:
            print(f"Error al recibir mensaje: {e}")

# Hilo para recibir mensajes de los clientes
thread_receive = threading.Thread(target=receive)
thread_receive.start()


def check_clients_connected():
    while True:
        with lock:
            if len(client_node_mapping) == 14:
                print("¡Todos los clientes están conectados!")
                for client_address in client_node_mapping.keys():
                    server_socket.sendto(b'todos_conectados', client_address)
                    time.sleep(2)

                break
        time.sleep(4)

# Hilo para verificar si los cuatro clientes están conectados
thread_check_clients_connected = threading.Thread(target=check_clients_connected)
thread_check_clients_connected.start()