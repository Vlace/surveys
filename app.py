from flask import Flask, render_template, request, redirect, flash
from surveys import surveys

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
responses = []


@app.route('/')
def home():
    satisfaction_survey = surveys["satisfaction"]
    return render_template('questions.html', satisfaction_survey=satisfaction_survey)

@app.route("/questions/<int:quest_num>")
def questions(quest_num):
    satisfaction_survey = surveys["satisfaction"].questions
    num = quest_num
    satisfaction_choices = satisfaction_survey[num].choices
    
    if(len(responses) == len(satisfaction_survey)):
        return redirect("/survey_complete")
    
    if (len(responses) != num):
        flash("You shall not pass!")
        return redirect (f"/questions/{len(responses)}")
    else:
        return render_template("answers.html", satisfaction_choices=satisfaction_choices, quest_num=num, satisfaction_survey=satisfaction_survey)

@app.route("/answers", methods=["POST"])
def answers():
    answer = request.form["answer"]
    responses.append(answer)
    satisfaction_survey = surveys["satisfaction"].questions

    if len(responses) == len(satisfaction_survey):
        return redirect("/survey_complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/survey_complete")
def thanks():
    return render_template("thanks.html")
