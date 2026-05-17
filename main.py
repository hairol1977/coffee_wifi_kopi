#ambil ni

#jadi sangat bagus

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, URL
import csv
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# -------------------- FORM CONFIG -------------------- #
class CafeForm(FlaskForm):
    cafe = StringField("Café Name", validators=[DataRequired()])
    location = StringField("Google Maps Location", validators=[DataRequired(), URL()])
    open = StringField("Opening Time (e.g. 8AM)", validators=[DataRequired()])
    close = StringField("Closing Time (e.g. 5PM)", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee", choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
    wifi_rating = SelectField("Wi-Fi", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power_rating = SelectField("Power Outlet", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    review = TextAreaField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Submit")

# -------------------- ROUTES -------------------- #
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", current_year=datetime.now().year)

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding="utf-8") as file:
            file.write(f"\n{form.cafe.data},{form.location.data},{form.open.data},{form.close.data},"
                       f"{form.coffee_rating.data},{form.wifi_rating.data},{form.power_rating.data},{form.review.data}")
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form, current_year=datetime.now().year)

@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        cafe_data = list(reader)
    return render_template("cafes.html", cafes=cafe_data, current_year=datetime.now().year)

# -------------------- START -------------------- #
if __name__ == "__main__":
    app.run(debug=True, port=5002)