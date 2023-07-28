from django import forms

from .models import Post, Country, Taste, Review


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("picture", "text", "country", "taste", "cacao")
        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs["class"] = "form-control"
                

class SearchForm(forms.Form):
    selected_country = forms.ModelChoiceField(
        label='原産国',
        required=False,
        queryset=Country.objects,
    )
    selected_taste = forms.ModelChoiceField(
        label='テイスト',
        required=False,
        queryset=Taste.objects,
    )
    freeword = forms.CharField(min_length = 2, max_length = 100, label='', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selected_country = self.fields['selected_country']
        selected_taste = self.fields['selected_taste']


class ReviewForm(forms.ModelForm):   
    class Meta:
        model = Review
        fields = ['score', 'comment']