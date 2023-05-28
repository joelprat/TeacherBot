import pytesseract
import requests
import os
from translate import Translator
from gtts import gTTS
from PIL import Image
from faker import Faker
import speech_recognition as sr
from pydub import AudioSegment
#Test TextToSpeach
from pygame import mixer
import time
import socket
import errno
URL = 'https://languagetool.org/api/v2/check'
HEADERS = {'Content-Type': 'application/x-www-form-URLencoded'}
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def loadImage(imageURL:str):
    # Carga la imagen
    #imageURL = "r" . imageURL
    img = Image.open(imageURL)
    # Convierte la imagen a escala de grises
    img = img.convert('L')

    # Reconoce el texto y la posición de cada palabra en la imagen
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    # Reconoce el texto en la imagen
    text = pytesseract.image_to_string(img)
    return text, data

def replaceCaracter(data:str):
    palabras = {}
    for i in range(len(data['text'])):
        # Obtén la palabra y su posición en la imagen
        word = data['text'][i].replace(" ", "")  # eliminar los espacios en blanco  
        word = word.replace(",", "")
        word = word.replace(".", "")
        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]
        print(data)
        w = x + w
        h = y + h
        
        # Agregar la palabra y sus datos de posición al diccionario
        palabras[word] = [x, y, w, h]

    return palabras

def recibir_todo(sock):
    datos = b""
    buff_size = 4096

    try:
        #sock.setblocking(False)
        sock.settimeout(5)
        while True:
            try:
                datos_temp = sock.recv(buff_size)
                if not datos_temp:
                    break
                datos += datos_temp
                print(len(datos))
                datos_temp = None
            except socket.timeout:
                # Si se produce un timeout, no se cierra el socket, pero se sale del bucle
                break
            except socket.error as e:
                print("Error al recibir datos: ", str(e))
                break

    except socket.error as e:
        print("Error al recibir datos: ", str(e))

    return datos

def APIcorrection(text:str, palabras):
    # Detección de errores para las palabras
    data = {'text': text, 'language': 'ca', 'enabledOnly': 'false'}

    response = requests.post(URL, headers=HEADERS, data=data)

    matches = response.json().get('matches', [])
    errors = []
    corrections = []

    for match in matches:
        if match['rule']['issueType'] == 'misspelling':
            errors.append((match['offset'], match['offset']+match['length'], match['message']))
            corrections.append((match['offset'], match['offset']+match['length'], match['replacements'][0]['value']))

    palabras_error = []

    # Corregir el texto
    corrected_words = []
    for correction in corrections[::-1]:
        corrected_words.append(correction[2])

    # Indicar las palabras con error
    for error in errors[::-1]:
        word = text[error[0]:error[1]]
        palabras_error.append(word)
    
    

    #Guardamos un diccionario unicamente con los datos de las palabras incorrectas
    palabras_final = {}
    for palabra in palabras_error:
        if palabra in palabras:
            #Guardamos la palabra con el error y la posicion
            palabras_final[palabra] = palabras[palabra]
    
    return palabras_final, corrected_words

def convertir_texto_a_audio(texto):
    # Crea un objeto gTTS con el texto proporcionado
    tts = gTTS(text=texto, lang='es')

    # Guarda el audio en un archivo temporal
    archivo_audio = 'temp_audio.mp3'
    tts.save(archivo_audio)

    # Reproduce el audio utilizando el reproductor predeterminado del sistema
    reproducir_audio(archivo_audio)

    # Elimina el archivo temporal de audio
    #os.remove(archivo_audio)

def reproducir_audio(archivo_audio):
    # Verifica el sistema operativo para determinar el reproductor de audio adecuado
    mixer.init()
    mixer.music.load(archivo_audio)
    mixer.music.play()
    time.sleep(10)

def traducir(frase, idioma_origen, idioma_destino):
    translator = Translator(from_lang=idioma_origen, to_lang=idioma_destino)
    traduccion = translator.translate(frase)
    return traduccion

def transcribir_audio(ruta_archivo):
    r = sr.Recognizer()
    with sr.AudioFile(ruta_archivo) as fuente_audio:
        audio = r.record(fuente_audio)
    try:
        texto_transcrito = r.recognize_google(audio, language="es-ES")  # Establece el idioma del audio
        return texto_transcrito
    except sr.UnknownValueError:
        print("No se pudo transcribir el audio")
    except sr.RequestError as e:
        print("Error en la solicitud al servicio de reconocimiento de voz: ", str(e))



def main():
    """Generamos una frase o palabra rng"""
    idioma_origen = "en"
    idioma_destino = "ca"
    faker = Faker('en')  # Establece el idioma a catalán
    num_palabras = faker.random_int(min=10, max=15)  # Genera un número aleatorio de palabras entre 10 y 15
    #frase = faker.sentence(nb_words=num_palabras)   
    frase = faker.word()
    traduccion = traducir(frase, idioma_origen, idioma_destino)


    """Convertimos a audio la frase"""
    convertir_texto_a_audio(traduccion)
    #ruta_audio = "temp_audio.mp3"
    #ruta_audio_wav = "temp_audio.wav"
    #audio = AudioSegment.from_mp3(ruta_audio)
    # audio.export(ruta_audio_wav, format="wav")
    #texto_transcrito = transcribir_audio(ruta_audio_wav)
    #print(texto_transcrito)

    """OCR i Correction"""
    text, data = loadImage("imagen.jpeg")       
    palabras = replaceCaracter(data)
    palabras_final, corrected_words = APIcorrection(text, palabras)
    print(data)
    print(palabras_final)
    print(corrected_words)
# Verificación de si el archivo es el archivo principal
if __name__ == "__main__":
    # Llamado a la función principal
    main()
