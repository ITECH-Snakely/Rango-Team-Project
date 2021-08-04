from django import forms
from django.contrib.auth.models import User
from rango.models import Book, Page, Category, UserProfile, Video

# We could add these forms to views.py, but it makes sense to split them off into their own file.

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    dislikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likeDislikeDefault = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email','website', 'picture',)

class VideoForm(forms.ModelForm):
    title = forms.CharField(max_length=Video.TITLE_MAX_LENGTH, help_text="Please enter the title of the video.")
    url = forms.URLField(max_length=300, help_text="Please enter the URL of the video.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Video
        exclude = ('category',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        string = str(url)
        stringList = string.split('.com/')

        string2 = stringList[0] + ".com/embed/" + stringList[1]
        url = string2
        print(url)
        cleaned_data['url'] = url

        if url and not url.startswith(('http://') or ('https://')):
            url = f'http://{url}'
            cleaned_data['url'] = url 

        return cleaned_data


        
       
