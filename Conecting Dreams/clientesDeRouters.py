import socket
import random
import threading
from cryptography.fernet import Fernet
import os
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import time



# Ruta donde están los audios
audio_directory = './Audios/'
audios_disponibles = os.listdir(audio_directory)
ffmpeg_path = r"/C:\pythonAudio\bin/"
AudioSegment.converter = ffmpeg_path

# Obtener la ruta completa al ejecutable ffmpeg
#ffmpeg_path = r"C:\Users\ASUS\PycharmProjects\pythonUNCAUCA\Audios\ffmpeg.exe"


# Establecer la ubicación de ffmpeg para PyDub
#AudioSegment.converter = ffmpeg_path


def grabarAudio(duracion, nombreArchivo):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16, channels=2,
                        rate=44100, input=True,
                        frames_per_buffer=1024)

    print("Grabando ...")
    frames = []

    for i in range(0, int(44100 / 1024 * duracion)):
        data = stream.read(1024)
        frames.append(data)

    print("Grabacion a terminado ")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(os.path.join(audio_directory, nombreArchivo), 'wb')
    waveFile.setnchannels(2)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(44100)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()




def cargarClave():
    # Clave de cifrado
    clave = '86587XYNFG_FDpNaFoqZNa5MUd-TygrIMCas0XWfWMI='
    return (clave)


def desencriptar(mensaje, clave):
    f = Fernet(clave)
    mensaje_des = f.decrypt(mensaje)
    return (mensaje_des)


def encriptar(mensaje, clave):
    f = Fernet(clave)
    mensaje_encr = f.encrypt(mensaje.encode())
    return (mensaje_encr)



# Function to enter router's IP and port
def get_router_address():
    ip = input("Ingresa la dirección IP del router: ")
    port = int(input("Ingresa el puerto del router: "))
    return (ip, port)

# Create a socket for the user
user_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Generate a random port number between 21001 and 30000
random_port = random.randint(21001, 30000)

# Bind the socket to a specific port to receive messages
user_socket.bind(('localhost', random_port))



def receive_messages():
    while True:
        clave = cargarClave()
        # Recibir el mensaje y la dirección del remitente
        message, sender_address = user_socket.recvfrom(65536)
        if message.startswith(b'es_audio'):
            print("Llegó un audio")
            # Separar los fragmentos de audio y el nombre del archivo
            audio_info = message.split(b':', 1)[1]  # Obtener la parte después de 'es_audio:'
            audio_data, audio_name = audio_info.rsplit(b',',1)  # Separar los datos de audio y el nombre del archivo desde el final

            # Decodificar el nombre del archivo y eliminar cualquier carácter adicional al final
            audio_name = audio_name.strip().decode().rstrip(':')

            print("Nombre del archivo de audio recibido:", audio_name)

            direccion=audio_directory+"copy"+audio_name

            if direccion.endswith('.wav'):
                # Save the received audio to the system's file system

                with open(direccion, 'wb') as file:
                    while True:
                        audio_data,_= user_socket.recvfrom(65507)  # Receive larger fragments
                        # Separar los fragmentos de audio y el nombre del archivo
                        audio_info = message.split(b':', 1)[1]  # Obtener la parte después de 'es_audio:'
                        audio_data, audio_name = audio_info.rsplit(b',', 1)  # Separar los datos de audio y el no
                        # Decodificar el nombre del archivo y eliminar cualquier carácter adicional al final
                        audio_name = audio_name.strip().decode().rstrip(':')
                        if not audio_data:  # If there's no more data to receive, break the loop
                            break

                        file.write(audio_data)

                        # Reproduce the audio
                        #audio = AudioSegment.from_file(audio_name, format='wav')
                        #play(audio)

        else:
            message = message.decode()
            message_desencrypt = desencriptar(message, clave)
            print(f"Mensaje recibido de {sender_address}: {message_desencrypt}")










# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    try:
        # Get the router's address
        router_address = get_router_address()
        # Ask the user for the type of message
        eleccion=input("\n que va a enviar, texto o audio¿?")
        if eleccion=="texto":
            message_type = input("ecriba el mensaje que va a enviar: ")
            clave=cargarClave()
            message_type=encriptar(message_type,clave)
            # Ask for destination address and port
            destination_address = input("Ingresa la dirección IP del destino: ")
            destination_port = int(input("Ingresa el puerto del destino: "))
            # Create a message
            message = f":{destination_address}:{destination_port}".encode()
            # Send the message to the router
            user_socket.sendto(b'men_usuario :' + message_type+message, router_address)
            print("Mensaje enviado exitosamente.")
        elif eleccion=="audio":

            # Ask for destination address and port
            destination_address = input("Ingresa la dirección IP del destino: ")
            destination_port = int(input("Ingresa el puerto del destino: "))
            # Parámetros de la grabación de audio:
            duracion = float(input("Digite cuanto va a durar su audio:\n"))
            archivo = input("Escriba el nombre que le va a dar a su audio con .wav al final: ")

            # Grabar audio
            grabarAudio(duracion, archivo)

            # Leer todo el contenido del archivo de audio
            with open(audio_directory + archivo, 'rb') as file:
                audio_data = file.read()

            # Divide los datos de audio en fragmentos más pequeños
            fragment_size = 32768  # Tamaño arbitrario, puedes ajustarlo según tus necesidades
            fragments = [audio_data[i:i + fragment_size] for i in range(0, len(audio_data), fragment_size)]

            # Crea un mensaje con la información necesaria para reconstruir los fragmentos
            message_info = f":{destination_address}:{destination_port}:{archivo}".encode()

            for i, fragment in enumerate(fragments):
                # Envía cada fragmento con el nuevo formato de mensaje
                message = b'Es_audio' + message_info + b':' + fragment
                user_socket.sendto(message, router_address)

                # Agrega un delay de 1 segundo
                #time.sleep(1)

            print("Se envió el audio al router")


        else:
            print("escriba una opcion correcta")

    except KeyboardInterrupt:
        print("Saliendo del programa...")
        break
    except Exception as e:
        print("Error:", e)


