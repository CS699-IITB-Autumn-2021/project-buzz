from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
import re


class PhoneNumberForm(FlaskForm):
    """
    This class is to create a phone number form and perform validations on it, It inherits the FLASKFORM class from
    flask_wtf forms:

    Fields:
        :contact_no: A stringfield to enter the contact number.
        :submit: A Submitfield so that user can submit their response.
    """
    def validate_contact_no(self, contact_no_to_check):
        """
        This function is a validation method for validating the contact number entered by the user

        Inputs:
            :contact_no_to_check: The response entered by the user in the contact_no field
            :type contact_no_to_check: StringField

        Returns:
            :: None if validation is successful else raises a validation error
        """
        Pattern = re.compile("\+(91)[7-9][0-9]{9}")
        valid = Pattern.match(contact_no_to_check.data)
        if valid:
            return
        raise ValidationError('Allowed input format : +919123456789 --- +91<yourPhoneNumber>')

    contact_no = StringField(label='Phone Number', validators=[Length(min=13, max=13), DataRequired()])
    submit = SubmitField(label='Click to enter OTP')

