import fitz  # PyMuPDF
import nltk
import json

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Function to identify cities in text
def identify_cities(text):
    # Tokenize and tag parts of speech
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    
    # Load list of cities
    with open('output.json', 'r') as file:
        cities = json.load(file)
    
    city_names = set(city['name'].lower() for city in cities)
    
    # Identify cities based on proper noun tags
    cities_mentioned = set()
    for word, tag in pos_tags:
        if tag == 'NNP' and word.lower() in city_names:
            cities_mentioned.add(word)
    
    return list(cities_mentioned)

# Sample usage
pdf_path = 'cmo_qos_survey_2018_030119.pdf'  # Replace with your PDF file path
text = extract_text_from_pdf(pdf_path)
cities = identify_cities(text)

# Save the cities in a list
cities_list = list(cities)

# Print the cities mentioned in the PDF
print("Cities mentioned in the PDF:", cities_list)
