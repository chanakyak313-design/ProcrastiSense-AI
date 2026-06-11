from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    planned = request.form['planned']
    actual = request.form['actual']
    assigned = request.form['assigned']
    completed = request.form['completed']
    screen = request.form['screen']
    sleep = request.form['sleep']

    prompt = f"""
You are an AI productivity coach.

Analyze the following student data:

Planned Study Hours: {planned}
Actual Study Hours: {actual}
Tasks Assigned: {assigned}
Tasks Completed: {completed}
Screen Time: {screen} hours
Sleep Duration: {sleep} hours

Provide:

1. Productivity Analysis
2. Procrastination Level (Low, Medium, High)
3. Strengths
4. Areas of Improvement
5. Three Personalized Suggestions

Keep the response clear and professional.
"""

    try:
        response = model.generate_content(prompt)
        result = response.text

    except Exception as e:
        result = f"""
Gemini AI is currently unavailable.

Error:
{str(e)}

Temporary Analysis:

• Productivity could not be analyzed using AI.
• Please check Gemini API quota and configuration.
• Try again later.
"""

    return render_template(
        "result.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)