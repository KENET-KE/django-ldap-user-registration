from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator

from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset

from .models import Institution
from .ldap import LDAPOperations


class UserRegisterForm(forms.Form):
    title_choices = (('Mr.', 'Mr'), ('Ms', 'Ms',), ('Mrs.', 'Mrs.',), ('Dr.', 'Dr.',), ('Prof.', 'Prof.',),)
    country_choices = (('Kenya', 'Kenya'),)

    first_name = forms.CharField(required=True, max_length=255)
    last_name = forms.CharField(required=True, max_length=255)
    gender = forms.TypedChoiceField(
        choices=((0, "Male"), (1, "Female"),),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial='0',
        required=True)
    email = forms.EmailField(required=True)
    title = forms.ChoiceField(required=True, choices=title_choices)
    designation = forms.CharField(max_length=200)
    department = forms.CharField(required=True, max_length=255)
    organization = forms.ModelChoiceField(required=False, queryset=Institution.objects.all(),
                                          empty_label='Select an organization', to_field_name='name')
    username = forms.CharField(required=True, min_length=3, max_length=30, help_text='Choose a memorable name e.g jdoe',
                               validators=[UnicodeUsernameValidator()])
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Confirm Password')
    phone = forms.CharField(required=True, max_length=200)
    address = forms.CharField(max_length=1000, widget=forms.Textarea())
    country = forms.ChoiceField(required=False, choices=country_choices)  # Set to default to your country

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.ldap_ops = LDAPOperations()
        self.helper = FormHelper()
        self.helper.form_id = 'id-user-data-form'
        self.helper.form_method = 'post'
        # self.helper.form_action = 'register'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Fieldset('Personal Data',
                     Field('first_name', placeholder='Your first name',
                           css_class="some-class"),
                     Div('last_name', title="Your last name"),
                     'email', 'phone', 'gender', 'title', 'designation', 'department', 'organization',),
            Fieldset('Login Details', 'username', 'password', 'password1',),
            Fieldset('Address', 'address', 'country',))

    def clean_username(self):
        # check username existence in LDAP
        username = self.cleaned_data['username']
        result = self.ldap_ops.check_attribute('uid', username)
        if result:
            raise forms.ValidationError("Username " + username + " is not available (in use)",
                                        code='username_exists_ldap')
        return username

    def clean_email(self):
        # check email existence in LDAP
        mail = self.cleaned_data['email']
        result = self.ldap_ops.check_attribute('mail', mail)
        if result:
            raise forms.ValidationError("Email " + mail + " is not available (in use)",
                                        code='email_exists_ldap')
        return mail

    def clean(self):

        # Check for password matching

        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')

        if password != password1:
            self._errors["password"] = self.error_class(["Passwords do not match"])

        return self.cleaned_data