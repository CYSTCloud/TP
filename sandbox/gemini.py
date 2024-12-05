# https://ai.google.dev/gemini-api/docs/quickstart?lang=python

import google.generativeai as genai
import os

api_key = ""

prompt = """
Traduis "J'ai un chien" en anglais. La réponse ne doit contenir que la traduction
"""

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
print(response.text)