# Helper function with automatic fallback for high-demand errors
def generate_ai_response(client, prompt):
    models_to_try = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.8-flash"]
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                continue # Try the next model
            else:
                raise e
    raise Exception("All models are currently busy. Please try again in a few moments.")
