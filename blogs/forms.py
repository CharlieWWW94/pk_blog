import datetime
import datetime
from django import forms


class NewBlogForm(forms.Form):
    
    title = forms.CharField(max_length=200, help_text='What is the title of your blog post?')
    strapline = forms.CharField(max_length=500, help_text='Add a strapline for further context')
    is_encrypted = forms.BooleanField(help_text='Would you like your post asymetrically encrypted?', required=False)
    blog_content = forms.CharField(help_text='Add your blog content here...')
    author = forms.CharField(max_length=100, help_text='Who are you?')
