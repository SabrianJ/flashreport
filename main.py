import fitz
from flask import Flask, render_template, flash, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename, redirect
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired, URL
from flask_wtf.file import FileRequired, FileAllowed, FileField

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
                early_check_in = accommodation.append(
                    float(data[data.index("Accom early check in") + index].replace(',', '')))
                late_check_out = accommodation.append(
                    float(data[data.index("Accom late check out") + index].replace(',', '')))
                accom_revenue = accommodation.append(
                    float(data[data.index("Accommodation Revenue") + index].replace(',', '')))
                accom_noshow = accommodation.append(
                    float(data[data.index("Accommodation-No Show") + index].replace(',', '')))
                courier = accommodation.append(float(data[data.index("Courier-on guest behalf") + index].replace(',', '')))
                credit_card = accommodation.append(float(data[data.index("Credit card fees") + index].replace(',', '')))
                dry_cleaning = accommodation.append(
                    float(data[data.index("Drycleaning / Laundry Charges") + index].replace(',', '')))
                guest_attrition = accommodation.append(
                    float(data[data.index("Guest Attrition Fees") + index].replace(',', '')))
                guest_cancellation = accommodation.append(
                    float(data[data.index("Guest Cancellation Fees") + index].replace(',', '')))
                hotel_shop = accommodation.append(float(data[data.index("Hotel Shop Revenue") + index].replace(',', '')))
                housekeeping_service = accommodation.append(
                    float(data[data.index("Housekeeping Service") + index].replace(',', '')))
                internet_charge = accommodation.append(float(data[data.index("Internet Charges") + index].replace(',', '')))
                phone_charges = accommodation.append(float(data[data.index("Phone Charges") + index].replace(',', '')))
                sofabed = accommodation.append(float(data[data.index("Sofa Bed") + index].replace(',', '')))
                sundry = accommodation.append(float(data[data.index("Sundry Income") + index].replace(',', '')))

                total = 0

                for val in accommodation:
                    total += val
                accommodation_total.append(round(total, 2))

                upgrade = float(data[data.index("Accommodation upgrade") + index].replace(',', ''))
                upgrade_total.append(upgrade)

                parking = float(data[data.index("Car Park Charges") + index].replace(',', ''))
                parking_total.append(parking)

                restaurant = []
                child_bf = restaurant.append(
                    float(data[data.index("Child Full cooked breakfast") + index].replace(',', '')))
                all_day_beverage = restaurant.append(
                    float(data[data.index("Restaurant All Day Beverage") + index].replace(',', '')))
                all_day_food = restaurant.append(
                    float(data[data.index("Restaurant All Day Food") + index].replace(',', '')))
                box_bf = restaurant.append(
                    float(data[data.index("Restaurant Box breakfast") + index].replace(',', '')))
                bf_food = restaurant.append(
                    float(data[data.index("Restaurant Breakfast Food") + index].replace(',', '')))
                dinner_beverage = restaurant.append(
                    float(data[data.index("Restaurant Dinner Beverage") + index].replace(',', '')))
                dinner_food = restaurant.append(
                    float(data[data.index("Restaurant Dinner Food") + index].replace(',', '')))
                lunch_beverage = restaurant.append(
                    float(data[data.index("Restaurant Lunch Beverage") + index].replace(',', '')))
                lunch_food = restaurant.append(
                    float(data[data.index("Restaurant Lunch Food") + index].replace(',', '')))
                room_service = restaurant.append(
                    float(data[data.index("Room Service Breakfast - Beverage") + index].replace(',', '')))
                vending_machine = restaurant.append(
                    float(data[data.index("Vending Machine Revenue-Drinks+snacks") + index].replace(',', '')))
                venue_hire = restaurant.append(
                    float(data[data.index("Vie Venue Hire") + index].replace(',', '')))

                total = 0

                for val in restaurant:
                    total += val
                restaurant_total.append(round(total, 2))

                income = income_total.append(float(data[data.index("Total Income") + index].replace(',', '')))

            if round(accommodation_total[0] + upgrade_total[0] + parking_total[0] + restaurant_total[0], 2) == income_total[0] and \
                    round(accommodation_total[1] + upgrade_total[1] + parking_total[1] + restaurant_total[1], 2) == income_total[1]:
                titles = ["Daily", "Monthly"]
                return render_template("index.html", form=form, accommodation_total=accommodation_total,
                                       upgrade_total=upgrade_total, parking_total=parking_total,
                                       restaurant_total=restaurant_total, income_total=income_total,
                                       titles=titles)
            else:
                return "<h1>Something is wrong</h1>"
        except ValueError:
            return "<h1>Only flash report is allowed</h1>"
    else:
        errors = form.chooseFile.errors
        return render_template("index.html", form=form, errors=errors)


if __name__ == '__main__':
    app.run(debug=True)
