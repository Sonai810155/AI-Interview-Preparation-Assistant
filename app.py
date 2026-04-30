from flask import Flask, render_template, request, send_file, redirect
from users import check_login
import requests
from database import create_table, save_interview, get_history
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
create_table()
API_KEY = os.getenv("API_KEY")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_login(username, password):
            return redirect('/')

        else:
            return render_template(
                "login.html",
                error="Invalid Username or Password"
            )

    return render_template("login.html")
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    domain = request.form['domain']
    question = request.form['question']
    answer = request.form['answer']

    prompt = f"""
You are a professional technical interviewer for {domain} domain.

Interview Domain:
{domain}

Interview Question:
{question}

Candidate Answer:
{answer}

Please provide:

1. Check if the answer is correct
2. Improved professional answer
3. Missing important points
4. Short interview feedback
5. Score out of 10
6. Performance rating:
   - Excellent
   - Very Good
   - Good
   - Average
   - Needs Improvement

Answer clearly in proper format.
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        feedback = result["choices"][0]["message"]["content"]
    else:
        feedback = "API Error: " + str(result)
    save_interview(domain, question, answer, feedback)

    return render_template(
        "index.html",
        feedback=feedback,
        question=question,
        answer=answer
    )
@app.route('/history')
def history():
    records = get_history()
    return render_template("history.html", records=records)
@app.route('/download')
def download_pdf():
    file_name = "interview_feedback.pdf"

    c = canvas.Canvas(file_name)

    c.drawString(100, 800, "AI Interview Preparation Assistant")
    c.drawString(100, 770, "Interview Feedback Report")

    c.drawString(100, 730, "Generated Successfully")

    c.save()

    return send_file(file_name, as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)