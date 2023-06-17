from django import test
from django.contrib.auth import get_user_model
from django.db.models import Q

from newspaper.forms import NewspaperForm, NewspaperSearchForm, RedactorForm
from newspaper.models import Topic


class NewspaperFormTest(test.TestCase):
    def test_newspaper_create(self):

        topic = Topic.objects.create(
            name="Topic of test"
        )
        publisher1 = get_user_model().objects.create(
            username="test_user1",
            password="rewq4321",
            years_of_experience=3
        )
        publisher2 = get_user_model().objects.create(
            username="test_user2",
            password="rewq4321",
            years_of_experience=0
        )
        form_data = {
            "title": "Test Newsp",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                       "sed do eiusmod tempor incididunt ut labore et "
                       "dolore magna aliqua.",
            "topic": topic,
            "publishers": [publisher1, publisher2]
        }
        newspaper_form = NewspaperForm(data=form_data)

        self.assertTrue(newspaper_form.is_valid())

        newspaper_form.cleaned_data["publishers"] = list(newspaper_form.cleaned_data["publishers"])
        form_data["publishers"] = list(get_user_model().
                                       objects.filter(Q(username="test_user1") | Q(username="test_user2")))
        self.assertEqual(newspaper_form.cleaned_data, form_data)


class NewspaperSearchFormTest(test.TestCase):
    def test_newspaper_search_form(self):
        form_data = {"search_title": "test_title"}
        form = NewspaperSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class RedactorFormTest(test.TestCase):
    def test_redactor_create(self):
        form_data = {
            "username": "test_user1",
            "password1": "rewq4321",
            "password2": "rewq4321",
            "first_name": "Adam",
            "last_name": "Adamson",
            "years_of_experience": 1
        }
        redactor_form = RedactorForm(data=form_data)

        self.assertTrue(redactor_form.is_valid())
        self.assertEqual(redactor_form.cleaned_data, form_data)

        form_data["years_of_experience"] = -1
        self.assertFalse(RedactorForm(form_data).is_valid(), msg="Years of experience may not be negative")


