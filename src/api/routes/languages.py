from fastapi import APIRouter
from src.core.compiler import compiler_manager

router = APIRouter(prefix="/languages", tags=["languages"])

@router.get("")
async def get_languages():
    """Get all supported languages"""
    languages_info = []
    
    for lang_id in compiler_manager.get_supported_languages():
        languages_info.append({
            "id": lang_id,
            "name": compiler_manager.languages.get(lang_id, "Unknown")
        })
    
    return languages_info

@router.get("/{language_id}")
async def get_language(language_id: int):
    """Get specific language information"""
    if language_id not in compiler_manager.get_supported_languages():
        return {"error": "Language not found"}
    
    return {
        "id": language_id,
        "name": compiler_manager.languages.get(language_id, "Unknown")
    }