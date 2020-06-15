from django.test import TestCase
from profiles.models import Analyst
# Create your tests here.

class AnalystRegister(TestCase):
    def setUp(self):
        analyst = Analyst.new_analyst(
            email = "analyst@mail.com",
            password = "$password$",
            full_name= "FirstName LastName",
        )
    
    def test_analyst_created(self):
        self.assertIsNotNone(Analyst.get_by_email("analyst@mail.com"))

class AnalystRegisterWebsite(TestCase):
    def setUp(self):
        analyst = Analyst.new_analyst(
            email = "analyst@mail.com",
            password = "$password$",
            full_name= "FirstName LastName",
        )
        analyst.new_website("http://www.my-domain.com")
    
    def test_analyst_created(self):
        analyst = Analyst.get_by_email("analyst@mail.com")

        self.assertIsNotNone(analyst.get_by_url(url = "http://www.my-domain.com"))