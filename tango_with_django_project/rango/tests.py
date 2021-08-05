from operator import truediv
from os import name
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
import datetime as dt
from rango.models import Book, Category
import random
import populate_rango

class RegisterViewTest(TestCase):
    def test_register_page(self):
        
        time1 = dt.datetime.now()
        response = self.client.get(reverse('rango:register'))
        #testing if http response is valid
        self.assertEqual(response.status_code, 200)
        #testing if correct page content is loaded 
        self.assertContains(response, '*Optional')
        #testing if loading time is under 5s
        time2 = dt.datetime.now()
        self.assertGreater(5,(time2-time1).total_seconds())

class noItemsinCategoryView(TestCase):

    def test_empty_index_response(self):
        """
        Checks to see whether the correct messages appear for no categories and pages.
        """
        test = Category.objects.create(name='n', views=0, likes=0, dislikes=0, likeDislikeDefault=0, slug=str(random.randint(0, 100000000000000000)))
        response = self.client.get(reverse('rango:show_category', args=(test.slug)))
        self.assertContains(response, '<strong>No pages currently in this category.</strong>')
        self.assertContains(response, '<strong>No videos currently in this category.</strong>')
        self.assertContains(response, '<strong>No books currently in this category.</strong>')

class CategoryMethodTests(TestCase):
    def test_ensure_likes_dislikes_are_positive(self):
        """
        Creates a test category which should always fail, because negative values not possible for Likes and Dislikes.
        When the exception is caught the testFailedCheck flips.
        """
        testFailedCheck = False

        try:
            test = Category.objects.create(name='n', views=0, likes=-1, dislikes=-1, likeDislikeDefault=0, slug=str(random.randint(0, 100000000000000000)))
        except IntegrityError:
            testFailedCheck = True
        
        self.assertTrue(testFailedCheck)

class QuoteChecker(TestCase):
    """
    Test that the quote engine is returning a valid quote and not empty string
    """
    def test_if_quote_exists(self):
        populate_rango.populate()
        response = self.client.get(reverse('rango:index'))
        self.assertNotContains(response, '<h1 id="quote_display"></h1>')