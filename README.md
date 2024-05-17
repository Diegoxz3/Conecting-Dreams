# Sistema de Mensajería UDP con Encriptación de Mensajes y Envío de Audio

Este proyecto es una implementación de un sistema de mensajería que permite a los usuarios enviar mensajes de texto y archivos de audio a través de una red utilizando sockets UDP. Los mensajes de texto se cifran utilizando la librería cryptography.fernet para garantizar la seguridad de la comunicación.

## Características

- Envío de mensajes de texto cifrados.
- Envío de archivos de audio en formato WAV.
- Grabación de audio desde el micrófono del usuario.
- Recepción de mensajes y archivos de audio.
- Interfaz de línea de comandos para interactuar con el sistema.

## Requisitos del Sistema

- Python 3.x
- Bibliotecas Python: cryptography, pyaudio, wave, pydub

## Uso

1. Clona el repositorio: git clone https://github.com/tu_usuario/sistema-mensajeria-udp.git
2. Instala las dependencias: pip install -r requirements.txt
3. Ejecuta el programa: python server_contorl2.py
4. Ejecuta el programa: python clientes_routers.py
5. se instancia en el terminal clientes_routers, debe tener, para el nodo 1 la direccion 127.0.0.1:12001,nodo 2 127.0.0.1:12002 y asi segun la tipolgia que se armo en el server. deben ir en orden ascendente y secuenciales las instancias que se hagan en la terminal
6. se ejecuta: python clientesDeRouters.py

### Funcionalidades Adicionales

El programa permite al usuario seleccionar entre enviar mensajes de texto o archivos de audio. Para enviar un mensaje de texto, el usuario debe escribir el mensaje y especificar la dirección IP y puerto del destinatario, asi como ip y puerto del router al que esta asociado. Para enviar un archivo de audio, el usuario puede grabar un archivo de audio desde el micrófono y enviarlo al destinatario.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama: git checkout -b nueva-caracteristica.
3. Haz tus cambios y haz commit: git commit -am 'Agrega nueva característica'.
4. Haz push a la rama: git push origin nueva-caracteristica.
5. Crea un pull request en GitHub.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más información.

---

Recuerda adaptar este README a las características específicas de tu proyecto y añadir cualquier otra información relevante que consideres importante para los usuarios y colaboradores potenciales.
