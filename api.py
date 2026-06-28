from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import random
from string import punctuation
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

def preprocessing_text(text):
    text = text.lower()
    text = word_tokenize(text)
    text = [word for word in text if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    text = [word for word in text if word not in stop_words and word not in punctuation]
    stemmer = PorterStemmer()
    text = [stemmer.stem(word) for word in text]
    return " ".join(text)


pipeline = joblib.load("model.pkl")
label_encoder = joblib.load("label_encoder.pkl")
file_path = "icthub_dataset.xlsx"

df = pd.read_excel(file_path)

responses_dict = df.groupby('Category')['Chatbot Response'].apply(list).to_dict()

app = FastAPI(
    title="ICT HUB Chatbot API",
    description="API for communicating with the ICT HUB smart chatbot",
    version="1.0"
)

class ChatRequest(BaseModel):
    user_message: str

@app.post("/chat")
def chat_with_bot(request: ChatRequest):
    user_input = request.user_message
    
    cleaned_text = preprocessing_text(user_input)

    predicted_class_array = pipeline.predict([cleaned_text])
    predicted_category = label_encoder.inverse_transform(predicted_class_array)[0]
    
    bot_reply = random.choice(responses_dict[predicted_category])
    
    return {
        "status": "success",
        "predicted_category": predicted_category,
        "bot_response": bot_reply
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the ICT HUB chatbot server!"}