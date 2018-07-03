from django import forms
from django.core.validators import RegexValidator

from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset


class UserRegisterForm(forms.Form):
    title_choices = (('Mr.', 'Mr'), ('Ms', 'Ms',), ('Dr.', 'Dr.',),)
    country_choices = (('Kenya', 'Kenya'),)
    organization_choices = (('kenet', 'KENET'),('other', 'Select other'),)
    first_name = forms.CharField(required=True, max_length=255)
    last_name = forms.CharField(required=True, max_length=255)
    email = forms.EmailField(required=True)
    title = forms.ChoiceField(required=False, choices=title_choices)
    designation = forms.CharField(max_length=200)
    organization = forms.ChoiceField(required=True, choices=organization_choices)
    username = forms.CharField(required=True, max_length=30, help_text='Choose a memorable name e.g jdoe',
                               validators=[
                                   RegexValidator(
                                       regex='^[a-zA-Z0-9_]*$',
                                       message='Username must be Alphanumeric. Allowed chars [a-zA-Z0-9_]',
                                       code='invalid_username'
                                   ),
                               ]
                               )
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    phone = forms.CharField(required=True, max_length=200)
    address = forms.CharField(max_length=1000, widget=forms.Textarea())
    country = forms.ChoiceField(required=True, choices=country_choices)  # Set to default to your country
    gender = forms.TypedChoiceField(
        choices=((0, "Male"), (1, "Female"),),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial='0',
        required=True)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-personal-data-form'
        self.helper.form_method = 'post'
        #self.helper.form_action = reverse('register')
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Personal Data',
                     Field('first_name', placeholder='Your first name',
                           css_class="some-class"),
                     Div('last_name', title="Your last name"),
                     'email', 'phone', 'gender', 'title', 'designation', 'organization',),
            Fieldset('Login Details', 'username', 'password', 'password1', style="color: brown;"),
            Fieldset('Address', 'address', 'country',))
                      #Tab('More Info', 'more_info')))
