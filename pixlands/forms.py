from django import forms
from .models import Topic, Image, ProfilePic, Comment


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'public']
        labels = {'text': '', 'public': 'make public'}


class ImageForm(forms.ModelForm):
    text = forms.CharField(required=False)
    class Meta:
        model = Image
        fields = ['image', 'text']
        labels = {'image': '', 'text': ''}


class EditImageForm(forms.ModelForm):
    text = forms.CharField(required=False)
    class Meta:
        model = Image
        fields = ['text']
        labels = {'text': ''}


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['image']
        labels = {'image': ''}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': ''}
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
