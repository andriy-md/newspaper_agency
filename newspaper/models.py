from django.contrib.auth.models import AbstractUser
from django.db import models


def get_default_topic():
    return Topic.objects.get_or_create(name="General")[0]


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField()

    REQUIRED_FIELDS = ["years_of_experience"]

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def delete(self, using=None, keep_parents=False):
        if self.name == "General":
            raise ValueError("General topic may not be deleted")
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic,
        default=get_default_topic,
        on_delete=models.SET_DEFAULT,
        related_name="newspapers"
    )
    publishers = models.ManyToManyField(
        Redactor,
        related_name="newspapers"
    )

    def __str__(self):
        publishers = [str(publisher) for publisher in self.publishers.all()]
        return f"{self.title} by {', '.join(publishers)}"
