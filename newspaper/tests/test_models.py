from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from newspaper.models import Topic, Newspaper


class TopicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Topic.objects.create(name="General")
        Topic.objects.create(name="Sport")

    def test_str(self):
        expected = "Sport"

        self.assertEqual(
            str(Topic.objects.get(name="Sport")), expected
        )

    def test_delete_general_topic_raises_error(self):
        with self.assertRaises(ValueError):
            Topic.objects.get(name="General").delete()

    def test_delete_topic(self):
        Topic.objects.get(name="Sport").delete()
        with self.assertRaises(ObjectDoesNotExist):
            Topic.objects.get(name="Sport")


class RedactorModelTest(TestCase):
    def setUp(self) -> None:
        get_user_model().objects.create_user(
            username="test_user",
            password="test123",
            first_name="Bob",
            last_name="Smith",
            years_of_experience=1
        )

    def test_str(self):
        expected = "test_user (Bob Smith)"
        redactor = get_user_model().objects.get(username="test_user")

        self.assertEqual(str(redactor), expected)


class NewspaperModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="test_user_bob",
            password="test123",
            first_name="Bob",
            last_name="Smith",
            years_of_experience=1
        )
        self.user2 = get_user_model().objects.create_user(
            username="test_user_cris",
            password="test123",
            first_name="Cris",
            last_name="Crison",
            years_of_experience=1
        )

        self.topic = Topic.objects.create(name="Science")

        self.newspaper = Newspaper(
            title="Article about tests",
            content="Content of article",
            topic=self.topic,
        )
        self.newspaper.save()
        self.newspaper.publishers.add(self.user1, self.user2)
        self.newspaper.save()

    def test_str(self):
        expected = "Article about tests by test_user_bob (Bob Smith), test_user_cris (Cris Crison)"

        self.assertEqual(str(self.newspaper), expected)

    def test_topic_sets_to_default(self):
        topic_politics = Topic.objects.create(name="Politics")
        topic_general = Topic.objects.create(name="General")
        newspaper2 = Newspaper(
            title="Article about tests",
            content="Content of article",
            topic=topic_politics,
        )
        newspaper2.save()
        newspaper2.publishers.add(self.user1, self.user2)
        newspaper2.save()
        topic_politics.delete()
        newspaper2.refresh_from_db()

        self.assertEqual(newspaper2.topic, topic_general)
