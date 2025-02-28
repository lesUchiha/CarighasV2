from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import random
import httpx

app = FastAPI(
    title="🐾 Animal Arena API",
    description="Una API moderna y minimalista para apuestas de animales y generación de imágenes.",
    version="1.0",
)

# Base de datos de animales con su nivel de fuerza
animals = {
    "León": 90,
    "Tigre": 85,
    "Elefante": 95,
    "Rinoceronte": 92,
    "Oso": 88,
    "Cocodrilo": 80,
    "Lobo": 70,
    "Águila": 65,
    "Serpiente": 60,
}

# Mensaje de bienvenida estilizado
@app.get("/", summary="Bienvenida a la API", tags=["General"])
def welcome():
    return JSONResponse(
        content={
            "message": "🔥 Bienvenido a Animal Arena API 🔥",
            "description": "Desafía al bot en batallas de animales y obtén imágenes de mascotas aleatorias.",
            "endpoints": {
                "/bet/": "Realiza una apuesta de combate entre animales.",
                "/pet_image/": "Obtén una imagen aleatoria de un perro o un gato."
            },
            "status": "🟢 API funcionando correctamente"
        }
    )

# Endpoint de apuestas de animales
@app.get("/bet/", summary="Realiza una apuesta entre animales", tags=["Apuestas"])
def animal_battle(user_choice: str):
    user_choice = user_choice.capitalize()

    if user_choice not in animals:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Animal no válido",
                "message": f"Por favor elige uno de la lista: {', '.join(animals.keys())}"
            }
        )

    # El bot elige un animal al azar
    bot_choice = random.choice(list(animals.keys()))
    user_strength = animals[user_choice]
    bot_strength = animals[bot_choice]

    # Determina el resultado
    if user_strength > bot_strength:
        result = "🏆 ¡Ganaste!"
    elif user_strength < bot_strength:
        result = "💀 Perdiste..."
    else:
        result = "⚖️ Empate."

    return JSONResponse(
        content={
            "Usuario": {"Animal": user_choice, "Fuerza": user_strength},
            "Bot": {"Animal": bot_choice, "Fuerza": bot_strength},
            "Resultado": result
        }
    )

# Endpoint de generación de imágenes de mascotas
@app.get("/pet_image/", summary="Obtén una imagen de una mascota", tags=["Imágenes"])
async def pet_image():
    pet = random.choice(["dog", "cat"])

    if pet == "dog":
        async with httpx.AsyncClient() as client:
            response = await client.get("https://dog.ceo/api/breeds/image/random")
        if response.status_code == 200:
            data = response.json()
            image_url = data["message"]
        else:
            raise HTTPException(status_code=500, detail="Error al obtener imagen de perro")
    else:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.thecatapi.com/v1/images/search")
        if response.status_code == 200:
            data = response.json()
            image_url = data[0]["url"]
        else:
            raise HTTPException(status_code=500, detail="Error al obtener imagen de gato")

    return JSONResponse(
        content={
            "Tipo": "🐶 Perro" if pet == "dog" else "🐱 Gato",
            "Imagen": image_url
        }
    )
