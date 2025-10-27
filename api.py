from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Multi-Language Compiler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Compiler API is running!", "status": "active"}

@app.post("/api/compile")
async def compile_code(request: dict):
    return {"message": "Compile endpoint works", "data": request}

@app.post("/api/v1/submissions")
async def submissions_v1(request: dict):
    return {"message": "Submissions endpoint works!", "data": request}

@app.get("/debug/routes")
async def debug_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": getattr(route, 'name', ''),
            "methods": list(getattr(route, 'methods', []))
        })
    return {"routes": routes}