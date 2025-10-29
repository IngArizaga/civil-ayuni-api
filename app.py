from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="API Ingeniería Civil Ayuni")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search_pdfs(request: SearchRequest):
    """Endpoint de búsqueda para el GPT de Ingeniería Civil"""
    return {
        "success": True,
        "results": [
            {
                "page": 1,
                "content": f"Información técnica especializada sobre {request.query} - Diseño estructural y normativas aplicables"
            },
            {
                "page": 2,
                "content": f"Aplicaciones prácticas de {request.query} en proyectos de ingeniería civil - Análisis de casos reales"
            },
            {
                "page": 3,
                "content": f"Cálculos y procedimientos para {request.query} según normativas internacionales ACI, AISC y Eurocódigos"
            }
        ]
    }

@app.get("/")
async def root():
    return {"status": "✅ API de Ingeniería Civil Ayuni activa", "version": "1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ⚠️ ESTO ES ESENCIAL - NO LO QUITES ⚠️
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)