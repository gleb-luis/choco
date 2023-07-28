from django import forms
from .models import Shop, ReviewShop, Pref, Tag
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

 
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = ('owner', 'created_at', 'updated_at', 'views', 'off_flag')
        widgets = {
            'content': SummernoteWidget(),
        }
    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field != 'content':
                field.widget.attrs["class"] = "form-control"


class SearchForm(forms.Form):
    selected_pref = forms.ModelChoiceField(
        label='都道府県',
        required=False,
        queryset=Pref.objects,
    )
    selected_tag = forms.ModelChoiceField(
        label='条件',
        required=False,
        queryset=Tag.objects,
    )
    freeword = forms.CharField(min_length = 1, max_length = 100, label='', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selected_pref = self.fields['selected_pref']
        selected_tag = self.fields['selected_tag']


class ReviewForm(forms.ModelForm):   
    class Meta:
        model = ReviewShop
        fields = ['score', 'comment']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['score'].required = True
                
    def clean(self):
        score = self.cleaned_data.get('score')
        if score == 0:
            raise forms.ValidationError('星マークをクリックして５段階評価を入れてください。')