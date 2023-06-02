import requests
import speech_recognition as sr
import easyocr
import cv2

URL = 'https://languagetool.org/api/v2/check'
HEADERS = {'Content-Type': 'application/x-www-form-URLencoded'}

def perform_ocr(image_path):
    # Cargar la imagen
    image = cv2.imread(image_path)

    # Inicializar el lector OCR
    reader = easyocr.Reader(['en'])

    # Realizar OCR en la imagen
    results = reader.readtext(image)

    # Extraer el texto y las coordenadas de cada palabra
    ocr_results = []
    for (bbox, text, _) in results:
        x_0 = bbox[0]
        x_1 = bbox[2]
        ocr_results.append({
            'text': text,
            'bounding_box': (x_0,x_1)
        })

    return ocr_results

def isCorrect(colection):
    incorrects= []
    for i in colection:
        data = {'text': i['text'], 'language': 'ca', 'enabledOnly': 'false'}
        response = requests.post(URL, headers=HEADERS, data=data)
        matches = response.json().get('matches', [])
        matches = response.json().get('matches', [])
        errors = []
        corrections = []

        for match in matches:
            if match['rule']['issueType'] == 'misspelling':
                incorrects.append(i)
    return incorrects






def text_recognition():   
    """OCR i Correction"""     
    conjunt = perform_ocr("imagen.jpeg")    
    palabras_error = isCorrect(conjunt)
    #print("Palabras and boxes:")
    print(palabras_error)
    return palabras_error

#text_recognition()
