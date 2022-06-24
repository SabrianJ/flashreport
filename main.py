import fitz
from flask import Flask, render_template, flash, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename, redirect
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired, URL
from flask_wtf.file import FileRequired, FileAllowed, FileField
import datetime

text = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class PDFForm(FlaskForm):
    chooseFile = FileField('PDF File', validators=[FileRequired(), FileAllowed(['pdf'], 'PDF only!')], id="chooseFile")
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/", methods=["GET", "POST"])
def main():
    form = PDFForm()
    if form.validate_on_submit():
        try:

            pdf = form.chooseFile.data

            with fitz.open("pdf", pdf.read()) as doc:
                global text
                text = ""
                for page in doc:
                    text += page.getText()

            data = text.split("\n")



            indexs = [1, 4]

            accommodation_total = []
            upgrade_total = []
            parking_total = []
            restaurant_total = []
            income_total = []

            for index in indexs:
                accommodation = []

                ACCOMS = ["Accom early check in", "Accom late check out", "Accommodation Revenue",
                         "Accommodation-No Show", "Courier-on guest behalf",
                         "Credit card fees", "Drycleaning / Laundry Charges", "Guest Attrition Fees",
                         "Guest Cancellation Fees", "Hotel Shop Revenue",
                         "Housekeeping Service", "Internet Charges", "Phone Charges", "Sofa Bed", "Sundry Income"]

                for accom_data in ACCOMS:
                    try:
                        accommodation.append(
                            float(data[data.index(accom_data) + index].replace(',', '')))
                    except ValueError:
                        accommodation.append(0)

                total = 0

                for val in accommodation:
                    total += val
                accommodation_total.append(round(total, 2))


                upgrade = float(data[data.index("Accommodation upgrade") + index].replace(',', ''))

                upgrade_total.append(upgrade)


                parking = float(data[data.index("Car Park Charges") + index].replace(',', ''))
                parking_total.append(parking)

                restaurant = []

                RESTAURANTS = ["Child Full cooked breakfast", "Restaurant All Day Beverage", "Restaurant All Day Food",
                        "Restaurant Box breakfast", "Restaurant Breakfast Food", "Restaurant Dinner Beverage",
                        "Restaurant Dinner Food", "Restaurant Lunch Beverage", "Restaurant Lunch Food",
                        "Room Service Breakfast - Beverage", "Room service Dinner - Beverage", "Vending Machine Revenue-Drinks+snacks", "Vie Venue Hire"]

                for restaurant_data in RESTAURANTS:
                    try:
                        restaurant.append(
                            float(data[data.index(restaurant_data) + index].replace(',', '')))
                    except ValueError:
                        accommodation.append(0)

                total = 0

                for val in restaurant:
                    total += val
                restaurant_total.append(round(total, 2))

                income = income_total.append(float(data[data.index("Total Income") + index].replace(',', '')))

            if round(accommodation_total[0] + upgrade_total[0] + parking_total[0] + restaurant_total[0], 2) == \
                    income_total[0] and \
                    round(accommodation_total[1] + upgrade_total[1] + parking_total[1] + restaurant_total[1], 2) == \
                    income_total[1]:
                titles = ["Daily", "Monthly"]
                return render_template("index.html", form=form, accommodation_total=accommodation_total,
                                       upgrade_total=upgrade_total, parking_total=parking_total,
                                       restaurant_total=restaurant_total, income_total=income_total,
                                       titles=titles, year=datetime.date.today().year)
            else:
                return "<h1>Something is wrong</h1>"
        except ValueError:
            return "<h1>Only flash report is allowed</h1>"

    else:
        errors = form.chooseFile.errors
        return render_template("index.html", form=form, errors=errors, year=datetime.date.today().year)


if __name__ == '__main__':
    app.run(debug=True)
