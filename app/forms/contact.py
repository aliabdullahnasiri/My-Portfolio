from wtforms import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

from app.forms import Form


class ContactForm(Form):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=100)]
    )

    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=100)]
    )

    email = EmailField(
        "Email Address", validators=[DataRequired(), Email(), Length(max=150)]
    )

    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10)])

    submit = SubmitField("Send Message")

    def validate_email(self, email): ...


class QuickContactForm(Form):
    email = StringField("Email", validators=[DataRequired(), Email()])

    def validate_email(self, email): ...
