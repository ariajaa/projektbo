import google.generativeai as genai

API_KEY = "MASUKKAN_API_KEY_GEMINI"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt):

    response = model.generate_content(
        f"""
        Kamu adalah customer service perusahaan logistik modern.

        Jawab dengan:
        - ramah
        - singkat
        - profesional
        - mudah dipahami customer

        Pertanyaan:
        {prompt}
        """
    )

    return response.text
