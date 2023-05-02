import pytesseract
import requests
from PIL import Image
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
        
        w = x + w
        h = y + h
        
        # Agregar la palabra y sus datos de posición al diccionario
        palabras[word] = [x, y, w, h]

    return palabras


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


def main():
    text, data = loadImage("test1.jpeg")
    palabras = replaceCaracter(data)
    palabras_final, corrected_words = APIcorrection(text, palabras)
    print(text)
    print(palabras_final)
    print(corrected_words)

# Verificación de si el archivo es el archivo principal
if __name__ == "__main__":
    # Llamado a la función principal
    main()
