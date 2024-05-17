import json
import socket
import threading
import sys

router_client_mapping = {}
puertos = [12001, 12002, 12003, 12004]  # Definir los puertos para los otros routers
router_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set to store used ports
puertos_en_uso = set()


# Function to enter client's IP and port
def get_client_listen_address():
    ip = input("Ingresa la dirección IP del router: ")
    port = int(input("Ingresa el puerto del router: "))
    return (ip, port)


# Client's address and port to listen
client_listen_address = get_client_listen_address()

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(client_listen_address)

# Server's address and port
server_address = ('127.0.0.1', 12005)

# Send a test message to the server to establish a minimal connection
client_socket.sendto(b'hello', server_address)


# Function to send a message to the server
def send_message(message):
    client_socket.sendto(message, server_address)


# Function to receive a message from the server



# Function to get the routing table from the node associated with the client
def get_routing_table(message):
    routing_table_data = message
    routing_table_data = routing_table_data[len(b'tablas de enrutamiento'):]
    routing_table = json.loads(routing_table_data.decode())
    return routing_table



# Function to print the routing table
def print_routing_table(routing_table):
    if routing_table:
        print("Tabla de enrutamiento:")
        for node, paths in routing_table.items():
            print(f"Camino más corto a {node}: ", end="")
            for i, path in enumerate(paths):
                target_node = path[-1]
                print(f"[{'-'.join(str(step) for step in path)}]", end="")
                if i < len(paths) - 1:
                    print("-", end="")
            print()
    else:
        print("No se pudo obtener la tabla de enrutamiento desde el servidor.")


# Function to send 'ok' to the server
def send_ok():
    send_message(b'ok')

#crear conexiones con los otros routers
def create_and_bind_sockets():
    puertos = [12001, 12002, 12003, 12004]  # Definir los puertos
    for puerto in puertos:
        try:
            # Creamos el socket
            socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            direccion = ('127.0.0.1', puerto)

            # Intentamos establecer la conexión con el servidor
            socket_cliente.connect(direccion)

            print("Conexión establecida en el puerto", puerto)

        except OSError as e:
            print("Error al establecer conexión en el puerto", puerto, ":", e)


# Function to handle the connection on a specific socket
def handle_connection(address, client_socket):
    try:
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_cliente.bind(address)
        while True:
            message, _ = socket_cliente.recvfrom(65536)
            print(f"Mensaje recibido en {socket_cliente.getsockname()}: {message.decode()}")
    except Exception as e:
        print(f"Error en el socket {address[1]}: {e}")



def deliver_to_client(message,destination_ip):

    if message.startswith(b'mensaje_especial: '):
        destination_ip = destination_ip.decode()
        ip_dest, port_dest = destination_ip.split(",")
        client_socket.sendto(b'es_audio: ' + message, (ip_dest, int(port_dest)))
        print(f"se envio audio a la direccion{destination_ip}")

    else:

        ip_dest, port_dest = destination_ip.split(",")
        client_socket.sendto(message, (ip_dest, int(port_dest)))
        print(f"se envio mensaje a la direccion{destination_ip}")









def route_message(destination_node_name, message, routing_table):
    ip2, puerto2 = client_listen_address
    print("Destination Node Name:", destination_node_name)
    if destination_node_name in router_client_mapping:
        # Obtener el router asociado a ese nodo_name
        router_associated = router_client_mapping.get(destination_node_name)
        print("Router Associated:", router_associated)
        if router_associated:
            ip_router, puerto_router = router_associated.split(',')
            router_associated = ip_router + '_' + puerto_router
            print(f"Router asociado a la dirección {destination_node_name}: {ip_router}:{puerto_router}")
            if (ip_router == ip2 and int(puerto_router) == puerto2):
                # Entregar el mensaje al cliente asociado al router actual
                deliver_to_client(message,destination_node_name)
                print("ya se entregara el mensaje a cliente asociado")
            else:
                if routing_table:
                    shortest_path = routing_table.get(router_associated)
                    if shortest_path:
                        # Enviar el mensaje al siguiente salto según el camino más corto
                        next_hop_ip, next_hop_port = shortest_path[1]
                        print(f"Enviando mensaje al siguiente salto: {next_hop_ip}:{next_hop_port}")
                        # Envío del mensaje en route_message
                        router_socket.sendto(b'enrutar' + message + b'+' + destination_node_name.encode(),(next_hop_ip, int(next_hop_port)))
                else:
                    print(f"No se encontró un camino más corto para {destination_node_name} en la tabla de enrutamiento")
        else:
            print(f"No se encontró un router asociado para la dirección {destination_node_name}")
    else:
        print(f"No se encontró la dirección {destination_node_name} en el mapeo router-cliente")


def route_message_audio(destination_node_name, message, routing_table):
    ip2, puerto2 = client_listen_address
    print("Destination Node Name:", destination_node_name.decode())
    if destination_node_name.decode() in router_client_mapping:
        # Obtener el router asociado a ese nodo_name
        router_associated = router_client_mapping.get(destination_node_name.decode())
        print("Router Associated:", router_associated)
        if router_associated:
            ip_router, puerto_router = router_associated.split(',')
            router_associated = ip_router + '_' + puerto_router
            print(f"Router asociado a la dirección {destination_node_name}: {ip_router}:{puerto_router}")
            if (ip_router == ip2 and int(puerto_router) == puerto2):
                # Entregar el mensaje al cliente asociado al router actual
                deliver_to_client(b'mensaje_especial: ' + message +b':',destination_node_name)
                print("ya se entregara el mensaje a cliente asociado")
            else:
                if routing_table:
                    shortest_path = routing_table.get(router_associated)
                    if shortest_path:
                        # Enviar el mensaje al siguiente salto según el camino más corto
                        next_hop_ip, next_hop_port = shortest_path[1]
                        # Envío del mensaje en route_message
                        router_socket.sendto(b'enrutarEspecial:' + message + b':' + destination_node_name,(next_hop_ip, int(next_hop_port)))
                        print(f"Enviando mensaje al siguiente salto: {next_hop_ip}:{next_hop_port}")
                else:
                    print(f"No se encontró un camino más corto para {destination_node_name} en la tabla de enrutamiento")
        else:
            print(f"No se encontró un router asociado para la dirección {destination_node_name}")
    else:
        print(f"No se encontró la dirección {destination_node_name} en el mapeo router-cliente")










# Bucle principal para responder al mensaje "ask" del servidor cada 20 segundos
def control():
    # Definir un diccionario para almacenar los fragmentos de audio recibidos
    received_audio_fragments = {}
    while True:
        try:
            message, address = client_socket.recvfrom(65536)
            if message == b'ask':
                send_ok()
            elif message.startswith(b'tablas de enrutamiento'):
                tabla_enrutamiento = get_routing_table(message)
                print_routing_table(tabla_enrutamiento)
            elif message.startswith(b'todos_conectados'):
                create_and_bind_sockets()
            elif message.startswith(b'men_usuario'):
                # print(f"mensaje antes de hacer split en men_usuario:{message.decode()}")
                # Realizar enrutamiento según la tabla de enrutamiento brindada por el servidor.
                # Decodificar el mensaje y extraer la dirección de destino y el mensaje del usuario
                message_parts = message.decode().split(':')
                destination_address = message_parts[2]
                destination_port = message_parts[3]
                destination_node_name = str(destination_address) + ',' + str(destination_port)
                men_user = message_parts[1]
                route_message(destination_node_name, men_user.encode(), tabla_enrutamiento)
                # print(f"mensaje dado a la funcion rute_message: {men_user}")

                # Notificar al router sobre el nuevo cliente asociado
                ip, puerto = address
                ip2, puerto2 = client_listen_address
                mensaje = f'cliente_asociado:{ip},{puerto},{ip2},{puerto2}'.encode()
                for puerto in puertos:
                    direccion = ('127.0.0.1', int(puerto))
                    router_socket.sendto(b'cliente_asociado' + mensaje, direccion)
                    print("Notificando al router en", direccion, "sobre el nuevo cliente.")


            elif message.startswith(b'Es_audio'):

                # Dividir el mensaje en sus partes
                message_parts = message.split(b':')

                # Extraer la información del mensaje
                destination_address = message_parts[1].decode()
                destination_port = message_parts[2].decode()

                audio_name = message_parts[3].decode()
                audio_name = f",{audio_name}".encode()

                audio_data = message_parts[4]

                destination_node_name = f"{destination_address},{destination_port}".encode()

                # Imprimir para verificar los valores extraídos
                # print(f"Nombre del archivo de audio: {audio_name.decode()}")
                # print(f"Datos de audio: {audio_data[:50]}...")  # Solo imprime los primeros 50 bytes como ejemplo
                # print(f"Dirección IP de destino: {destination_address}")
                # print(f"Puerto de destino: {destination_port}")

                # Enviar el audio a la función de enrutamiento
                route_message_audio(destination_node_name, audio_data + audio_name, tabla_enrutamiento)
                print("Se envió el audio a la función de enrutamiento.")

                # Notificar al router sobre el nuevo cliente asociado
                ip, puerto = address
                ip2, puerto2 = client_listen_address
                mensaje = f'cliente_asociado:{ip},{puerto},{ip2},{puerto2}'.encode()

                for puerto in puertos:
                    direccion = ('127.0.0.1', int(puerto))
                    router_socket.sendto(b'cliente_asociado' + mensaje, direccion)
                    print("Notificando al router en", direccion, "sobre el nuevo cliente.")


            elif message.startswith(b'cliente_asociado'):
                # Decodificar el mensaje para extraer las direcciones IP y puertos del cliente y del router
                partes_mensaje = message.decode().split(':')
                datos_cliente = partes_mensaje[1].split(',')
                # Extraer la dirección IP y el puerto del cliente
                ip_cliente, puerto_cliente = datos_cliente[:2]
                # Extraer la dirección IP y el puerto del router
                ip_router_cliente, puerto_router_cliente = datos_cliente[2:]
                # Construir una cadena que represente la dirección del cliente
                dir_cliente = str(ip_cliente) + ',' + str(puerto_cliente)
                # Construir una cadena que represente la dirección del router
                dir_router = str(ip_router_cliente) + ',' + str(puerto_router_cliente)
                # Verificar si la asociación ya existe en el diccionario
                if dir_cliente not in router_client_mapping:
                    # Realizar mapeo router-usuario localmente
                    router_client_mapping[dir_cliente] = (dir_router)
                    print(f"diccionario router-cliente{router_client_mapping}")
                    print("Mapeo router-usuario realizado:", ip_router_cliente + ',' + puerto_router_cliente, "->",
                          (ip_cliente, int(puerto_cliente)))
                else:
                    print("La asociación ya existe:", dir_cliente, "->", router_client_mapping[dir_cliente])
            elif message.startswith(b'enrutarEspecial:'):
                # Extraer el mensaje y el destino
                message_parts = message.split(b':')
                message_bytes = message_parts[1]
                destination_bytes = message_parts[2]

                # Llamar a la función de enrutamiento con los valores en bytes
                route_message_audio(destination_bytes, message_bytes, tabla_enrutamiento)
                print("se envio audio a enrutar de nuevo")

            elif message.startswith(b'enrutar'):
                # Decodificar el mensaje
                message_str = message.decode()
                print(f"el mensaje al inicio es:{message_str}")
                # Definir la palabra clave y el delimitador
                keyword = "enrutar"
                delimiter = "+"
                # Verificar si la palabra clave está en el mensaje
                if keyword in message_str:
                    # Eliminar la palabra clave del mensaje
                    message_str = message_str.replace(keyword, "", 1)  # Solo eliminar la primera ocurrencia
                # Separar el mensaje en partes usando el delimitador
                parts = message_str.split(delimiter)
                # Extraer el mensaje y el destino
                mensaje = delimiter.join(parts[:-1])
                destino = parts[-1]
                #print(f"llego un mensaje de:{address}, que va hacia {destino} ")
                route_message(destino, mensaje.encode(), tabla_enrutamiento)
                #print(f"el mensaje al final es:{mensaje}")
        except KeyboardInterrupt:
            print("Cerrando el cliente...")
            client_socket.close()
            router_socket.close()
            sys.exit()
        except Exception as e:
            print("Error:", e)


# Iniciar el hilo para la actividad del cliente
t_client_control = threading.Thread(target=control)
t_client_control.start()