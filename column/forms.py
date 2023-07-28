from django import forms
from .models import Column
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

 
class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ("title", "content", "thumbnail", "is_draft", "is_index", "content_script")
        widgets = {
            # 'text': SummernoteInplaceWidget(),
            'content': SummernoteWidget(),
        }
    def __init__(self, *args, **kwargs):
        super(ColumnForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field != 'content':
                field.widget.attrs["class"] = "form-control"

