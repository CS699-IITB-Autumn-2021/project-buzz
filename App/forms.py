from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
import re


class PhoneNumberForm(FlaskForm):
    def validate_contact_no(self, contact_no_to_check):
        Pattern = re.compile("\+(91)[7-9][0-9]{9}")
        valid = Pattern.match(contact_no_to_check.data)
        if valid:
            return
        raise ValidationError('Allowed input format : +919123456789 --- +91<yourPhoneNumber>')

    contact_no = StringField(label='Phone Number', validators=[Length(min=13, max=13), DataRequired()])
    submit = SubmitField(label='Click to enter OTP')

