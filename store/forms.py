from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    RATING_CHOICES = [
        (5, "★★★★★"),
        (4, "★★★★☆"),
        (3, "★★★☆☆"),
        (2, "★★☆☆☆"),
        (1, "★☆☆☆☆"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:

        model = Review

        fields = [
            "rating",
            "comment",
        ]

        widgets = {

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Tell other customers about this product..."
                }
            )

        }