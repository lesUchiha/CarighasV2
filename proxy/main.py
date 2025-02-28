from fastapi import FastAPI
import httpx

app = FastAPI()

# URLs de las APIs desplegadas en Railway
API1_URL = "https://animalarena.up.railway.app"
API2_URL = "https://autofarm.up.railway.app"

@app.api_route("/{api_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(api_name: str, path: str):
    async with httpx.AsyncClient() as client:
        if api_name == "api1":
            url = f"{API1_URL}/{path}"
        elif api_name == "api2":
            url = f"{API2_URL}/{path}"
        else:
            return {"error": "API no encontrada"}

        response = await client.request(method="GET", url=url)
        return response.json()
