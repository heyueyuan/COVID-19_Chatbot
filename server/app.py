# -*- coding: UTF-8 -*-
from fastapi import FastAPI,Body,Form
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Predicted import predicted

app = FastAPI()


app.add_middleware(         
    CORSMiddleware,        
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],    
)

@app.get("/")
async def main():
    return "Hello, I am a COVID-19 Chatbot, I will do my best to answer what you wanna know about this virus."

@app.get("/{a}")
async def regist(a):
    if a == 'Hello':
        return "Hello, I am a COVID-19 Chatbot, I will do my best to answer what you wanna know about this virus."
    else:
        print('Message is: ',a)
        # print(type(a))
        try:
            result = predicted(a)
        except KeyError:
            result = "Please ask again. You can ask \"What is coronavirus?\", etc. "
         
        return result
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)