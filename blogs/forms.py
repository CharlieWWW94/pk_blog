import datetime
import datetime
from django import forms


class NewBlogForm(forms.Form):
    title = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-content', 'placeholder': ' Add your blog content here...'}))
    strapline = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-content','placeholder': ' Add a strapline for context...'}))
    is_encrypted = forms.BooleanField(help_text=' Would you like your post asymetrically encrypted?', required=False)
    blog_content = forms.CharField( widget=forms.Textarea(attrs={'class': 'form-content', 'placeholder': ' Add your blog content here...', 'rows': 20, 'cols': 10, }))
    author = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Who are you?'}))

class DecryptForm(forms.Form):
    user_key = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-content-1', 'placeholder': 'Add key here...'}))
    blog_id = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-content-2', 'placeholder': 'Confirm blog ID:'}))
