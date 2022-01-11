from django.test import TestCase
from landing.forms import MyRegisterForm
from django.contrib.auth.models import User

#Checks whether custom user creation form is valid
class TestAppForms(TestCase):
    def setUp(self) -> None:
        self.username = 'user'
        self.first_name = 'MyFirstName'
        self.last_name = 'MySurName'
        self.email = 'myemail@email.com'
        self.password = 'MyNicePass'

    def test_registrationForm_Valid(self):
        form = MyRegisterForm( data = {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertTrue(form.is_valid()) 
        self.assertTrue(form.save())
