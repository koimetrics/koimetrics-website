from django.test import TestCase
from websites.models import Website

# Create your tests here.
class CreateWebsiteTestCase(TestCase):
    def setUp(self):
        website = Website.new_website(
            url = "http://www.my-domain.com"
        )
        website.url = website.url
        website.save()

    def test_website_created(self):
        self.assertIsNotNone(Website.get_by_url("http://www.my-domain.com"))
        self.assertIsNone(Website.get_by_url("http://www.nonexistent-domain.com"))
        self.assertIsNotNone(Website.get_by_url("http://www.my-domain.com").apikey)

