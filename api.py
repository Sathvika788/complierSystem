from fastapi import FastAPI, HTTPException

app = FastAPI()

# Keep your existing routes
@app.post("/api/compile")
async def compile_code(request: dict):
    # Your existing compile logic
    pass

# ADD THIS NEW ROUTE for compatibility
@app.post("/api/v1/submissions")
async def submissions_v1(request: dict):
    """
    Compatibility endpoint for Judge0-style requests
    """
    try:
        # Convert Judge0 format to your format
        language_id = request.get("language_id")
        source_code = request.get("source_code")
        stdin = request.get("stdin", "")
        
        # Map language_id to language name
        language_map = {
            1: "c",      # C
            2: "cpp",    # C++
            3: "python", # Python
            4: "java",   # Java
            5: "javascript", # JavaScript
            6: "go",     # Go
            7: "rust",   # Rust
            8: "sql"     # SQL
        }
        
        language = language_map.get(language_id)
        if not language:
            raise HTTPException(status_code=400, detail="Unsupported language_id")
        
        # Call your existing compile logic
        result = await execute_code(language, source_code, stdin)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))