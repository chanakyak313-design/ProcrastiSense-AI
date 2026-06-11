from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    planned = float(request.form['planned'])
    actual = float(request.form['actual'])
    assigned = int(request.form['assigned'])
    completed = int(request.form['completed'])
    screen = float(request.form['screen'])
    sleep = float(request.form['sleep'])

    productivity = round((actual / planned) * 100, 2)

    score = 0

    if actual < planned:
        score += 30

    if completed < assigned:
        score += 30

    if screen > 5:
        score += 20

    if sleep < 7:
        score += 20

    if score <= 30:
        level = "Low"
    elif score <= 60:
        level = "Medium"
    else:
        level = "High"

    suggestions = []

    if actual < planned:
        suggestions.append("Follow a fixed study schedule")

    if completed < assigned:
        suggestions.append("Break tasks into smaller goals")

    if screen > 5:
        suggestions.append("Reduce screen time")

    if sleep < 7:
        suggestions.append("Improve sleep duration")

    return render_template(
        'result.html',
        productivity=productivity,
        level=level,
        suggestions=suggestions
    )

if __name__ == '__main__':
    app.run(debug=True)