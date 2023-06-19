from django import test
from django.contrib.auth import get_user_model
from django.urls import reverse

from newspaper.models import Newspaper, Topic


NewspaperListPath = reverse("newspaper:newspaper-list")
NewspaperCreatePath = reverse("newspaper:newspaper-create")
RedactorListPath = reverse("newspaper:redactor-list")
RedactorCreatePath = reverse("newspaper:redactor-create")


class NewspaperListViewTest(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        topic = Topic.objects.create(name="Test topic")

        for i in range(10):
            Newspaper.objects.create(
                title="Newspaper for Testing",
                content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                       "sed do eiusmod tempor incididunt ut labore et "
                       "dolore magna aliqua.",
                topic=topic,
            )

    def test_url_accessible(self):
        response = self.client.get(NewspaperListPath)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(NewspaperListPath)

        self.assertTemplateUsed(response, "newspaper/newspaper_list.html")

    def test_pagination_works(self):
        response = self.client.get(NewspaperListPath)

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["newspaper_list"]), 7)

    def test_search_by_title(self):
        Newspaper.objects.create(
            title="Target Newspaper to be found",
            content="Some test content for test newspaper",
            topic=Topic.objects.get(name="Test topic")
        )
        response = self.client.get(NewspaperListPath, data={"search_title": "Target"})
        expected_result = Newspaper.objects.filter(title__icontains="target")

        self.assertEqual(list(response.context["newspaper_list"]), list(expected_result))


class PrivateNewspaperCreateViewTest(test.TestCase):
    def setUp(self) -> None:
        test_user = get_user_model().objects.create_user(
            username="testuser",
            password="rewq4321",
            years_of_experience=1
        )
        self.client.force_login(test_user)

    def test_url_accessible(self):
        response = self.client.get(NewspaperCreatePath)

        self.assertEqual(response.status_code, 200)

    def test_url_uses_correct_template(self):
        response = self.client.get(NewspaperCreatePath)

        self.assertTemplateUsed(response, "newspaper/newspaper_form.html")

    def test_view_redirect(self):
        Topic.objects.create(name="Test topic")
        get_user_model().objects.create(
            username="test_user2",
            password="rewq4321",
            years_of_experience=2,
            first_name="John",
            last_name="Tester"
        )

        newspaper_data = {
            "title": "Test Newspaper",
            "content": "Some test content for test newspaper",
            "topic": 1,
            "publishers": [2]
        }
        response = self.client.post(NewspaperCreatePath, data=newspaper_data)

        self.assertRedirects(response, reverse("newspaper:newspaper-detail", args=[1]))


class PublicNewspaperCreateViewTest(test.TestCase):
    def test_url_not_accessible(self):
        response = self.client.get(NewspaperCreatePath)

        self.assertNotEqual(response.status_code, 200)


class RedactorListViewTest(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(12):
            get_user_model().objects.create(
                username="test_user" + str(i),
                password="rewq4321",
                years_of_experience=3
            )

    def test_url_accessible(self):
        response = self.client.get(RedactorListPath)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(RedactorListPath)

        self.assertTemplateUsed(response, "newspaper/redactor_list.html")

    def test_pagination_works(self):
        response = self.client.get(RedactorListPath)

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["redactor_list"]), 10)


class PrivateRedactorCreateViewTest(test.TestCase):
    def setUp(self):
        test_user = get_user_model().objects.create(
            username="test_user",
            password="rewq4321",
            years_of_experience=1
        )
        self.client.force_login(test_user)

    def test_url_accessible(self):
        response = self.client.get(RedactorCreatePath)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(RedactorCreatePath)

        self.assertTemplateUsed(response, "newspaper/redactor_form.html")

    def test_view_redirects(self):
        redactor_data = {
            "username": "test_user2",
            "password1": "rewq4321",
            "password2": "rewq4321",
            "first_name": "Adam",
            "last_name": "Adamson",
            "years_of_experience": 1
        }
        response = self.client.post(RedactorCreatePath, data=redactor_data)

        self.assertRedirects(response, reverse("newspaper:redactor-detail", args=[2]))


class PublicRedactorCreateViewTest(test.TestCase):
    def test_url_not_accessible(self):
        response = self.client.get(RedactorCreatePath)

        self.assertNotEqual(response.status_code, 200)
