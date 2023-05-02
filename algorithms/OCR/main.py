import pytesseract
import requests
from PIL import Image
url = 'https://languagetool.org/api/v2/check'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Carga la imagen
img = Image.open(r'C:\Users\cives\OneDrive\Escritorio\test1.jpeg')

# Convierte la imagen a escala de grises
img = img.convert('L')

# Reconoce el texto en la imagen
text = pytesseract.image_to_string(img)

# Imprime el texto reconocido
print(text)

# Reconoce el texto y la posición de cada palabra en la imagen
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

# Inicializar un diccionario vacío para almacenar los datos
palabras = {}

# Iterar a través de los datos y agregar cada palabra al diccionario
long = len(data['text'])
for i in range(long):
    # Obtén la palabra y su posición en la imagen
    word = data['text'][i].replace(" ", "")  # eliminar los espacios en blanco  
    word = word.replace(",", "")
    x = data['left'][i]
    y = data['top'][i]
    w = data['width'][i]
    h = data['height'][i]
    
    w = x + w
    h = y + h
    
    # Agregar la palabra y sus datos de posición al diccionario
    palabras[word] = [x, y, w, h]   

# Detección de errores para las palabras
data = {'text': text, 'language': 'ca', 'enabledOnly': 'false'}

response = requests.post(url, headers=headers, data=data)

matches = response.json().get('matches', [])
errors = []

for match in matches:
    if match['rule']['issueType'] == 'misspelling':
        errors.append((match['offset'], match['offset']+match['length'], match['message']))

palabras_error = [];
print(errors[::-1])
# Indicar las palabras con error
for error in errors[::-1]:
    start = text[:error[0]].rfind(' ') + 1
    end = text[error[1]:].find(' ') + error[1]
    if end == -1:
        end = len(text)
    word = text[start:end + 1]
    word = word.replace(" ", "")
    word = word.replace(",", "")
    palabras_error.append(word)
    print(word)    

print(palabras_error)

#Guardamos un diccionario unicamente con los datos de las palabras incorrectas
palabras_final = {}
for palabra in palabras_error:
    if palabra in palabras:
        #Guardamos la palabra con el error y la posicion
        palabras_final[palabra] = palabras[palabra]

print(palabras_final)
        
