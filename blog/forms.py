from blog.models import Post
from django.forms import ModelForm


class ItemForm(ModelForm):
    class Meta:
        model = Post
        fields = ['item_name', 'title', 'description', 'img']
