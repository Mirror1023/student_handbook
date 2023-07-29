from flask import Flask, render_template_string, request, jsonify
import requests
from pathlib import Path

from src.data_prep import load_pdf_data_from_disk
text = load_pdf_data_from_disk(file_name='Inspira Psych Handbook 2023 -2024 edited.pdf')

from src.data_prep import clean_and_format_text
handbook_text = clean_and_format_text(text)

app = Flask(__name__)

# Dummy API key for demonstration. Replace with your actual API key when running locally.
API_KEY = "HIDDEN"
OPENAI_ENDPOINT = "https://api.openai.com/v1/engines/davinci/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Inspira-Psych-Handbook-App"
}

template_string = """
<!doctype html>
<html>
    <head>
        <title>Student Handbook Q&A</title>
    </head>
    <body>
        <h2>Ask a Question About the Student Handbook</h2>
        <form action="/ask_openai" method="post" id="questionForm">
            <textarea name="question" rows="4" cols="50" placeholder="Type your question here..."></textarea><br><br>
            <input type="submit" value="Ask">
        </form>
        <h3>Answer:</h3>
        <div id="answer"></div>
        <script>
            const form = document.getElementById('questionForm');
            form.addEventListener('submit', async (event) => {
                event.preventDefault();
                const formData = new FormData(form);
                const response = await fetch('/ask_openai', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                document.getElementById('answer').textContent = data.answer;
            });
        </script>
    </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(template_string)

@app.route('/ask_openai', methods=['POST'])
def ask_openai():
    question = request.form.get('question')
    prompt = f"The following is a student handbook: {handbook_text}\n\nQ: {question}\nA:"
    data = {
        "prompt": prompt,
        "max_tokens": 250
    }
    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=data)
    response_data = response.json()
    answer = response_data['choices'][0]['text'].strip() if 'choices' in response_data and response_data['choices'] else "Sorry, I couldn't provide an answer at the moment."
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run()
