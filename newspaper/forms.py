from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import MinValueValidator

from newspaper.models import Newspaper, Redactor


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


class NewspaperSearchForm(forms.Form):
    search_title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title",
                "class": "form-control",
                # "help_text": "",
            }
        )
    )


class RedactorForm(UserCreationForm):
    years_of_experience = forms.IntegerField(
        widget=forms.NumberInput,
        validators=[MinValueValidator(0)]
    )

    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "years_of_experience",)


class RedactorUpdateDataForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = Redactor
        fields = ("first_name", "last_name", "years_of_experience",)
