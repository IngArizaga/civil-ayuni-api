from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import PyPDF2
import glob

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


def buscar_en_pdfs(query):
    """Busca el texto en todos los PDFs de la carpeta"""
    resultados = []
    pdf_folder = "./pdfs"

    if not os.path.exists(pdf_folder):
        return [{"page": 1, "content": "Carpeta de PDFs no encontrada"}]

    for pdf_file in glob.glob(os.path.join(pdf_folder, "*.pdf")):
        try:
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if query.lower() in text.lower():
                        resultados.append({
                            "archivo": os.path.basename(pdf_file),
                            "page": page_num + 1,
                            "content": text[:500] + "..."  # Primeros 500 caracteres
                        })
        except Exception as e:
            continue

    if not resultados:
        return [{"page": 1, "content": f"No se encontraron resultados para '{query}'"}]

    return resultados


@app.post("/search")
async def search_pdfs(request: SearchRequest):
    """Endpoint de búsqueda en PDFs reales"""
    resultados = buscar_en_pdfs(request.query)

    return {
        "success": True,
        "results": resultados
    }


@app.get("/")
async def root():
    return {"status": "✅ API de Ingeniería Civil Ayuni activa", "version": "1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)