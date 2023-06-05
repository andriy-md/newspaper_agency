from django import forms
from django.contrib.auth import get_user_model

from newspaper.models import Topic, Newspaper


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Newspaper
        fields = ["title", "content", "topic", "publishers"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter Newspaper's title"}),
            "content": forms.Textarea(attrs={"placeholder": "Enter text"})
        }
