import pytesseract
import requests
from PIL import Image
url = 'https://languagetool.org/api/v2/check'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# Carga la imagen
img = Image.open('test4.jpeg')

# Convierte la imagen a escala de grises
img = img.convert('L')

# Reconoce el texto en la imagen
text = pytesseract.image_to_string(img)
# Imprime el texto reconocido
print(text)

# Reconoce el texto y la posición de cada palabra en la imagen
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

# Itera sobre cada palabra reconocida en la imagen
for i in range(len(data['text'])):
    # Obtén la palabra y su posición en la imagen
    word = data['text'][i]
    x = data['left'][i]
    y = data['top'][i]
    w = data['width'][i]
    h = data['height'][i]
    
    # Imprime la palabra y su posición en la imagen
    print('Palabra: {} | Posición: ({}, {}) - ({}, {})'.format(word, x, y, x+w, y+h))
    


data = {'text': text, 'language': 'ca', 'enabledOnly': 'false'}

response = requests.post(url, headers=headers, data=data)

errors = []

matches = response.json().get('matches', [])

for match in matches:
    if match['rule']['issueType'] == 'misspelling':
        errors.append((match['offset'], match['offset']+match['length'], match['message']))

palabras = [];
# Indicar las palabras con error
for error in errors[::-1]:
    start = text[:error[0]].rfind(' ') + 1
    end = text[error[1]:].find(' ') + error[1]
    if end == -1:
        end = len(text)
    word = text[start:end]
   # if word in data['text']:
       # palabras['text'].append(data['text'][data['text'].index(word)]);
        #palabras['left'].append(data['left'][data['text'].index(word)]);
        #palabras['top'].append(data['top'][data['text'].index(word)]);
        #palabras['width'].append(data['width'][data['text'].index(word)]);
        #palabras['height'].append(data['height'][data['text'].index(word)]);
    print(word)


print(errors)

