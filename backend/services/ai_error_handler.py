def handle_ai_error(error):
    return {
        "success": False,
        "message": "An error occurred while processing the AI request.",
        "error": str(error)
    }