from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Question, Answer, Tag

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your login here',
            'maxlength': '25',
            'style': 'background-color: #F5F5DC'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '**********',
            'maxlength': '25',
            'style': 'background-color: #F5F5DC'
        })

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'maxlength': '25',
            'style': 'background-color: #F5F5DC'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background-color: #F5F5DC'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '**********',
            'maxlength': '25',
            'style': 'background-color: #F5F5DC'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '**********',
            'maxlength': '25',
            'style': 'background-color: #F5F5DC'
        })
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control d-none',
            'id': 'regAvatar'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, avatar=self.cleaned_data['avatar'])
        return user


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control d-none',
                'id': 'regAvatar'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            if self.instance.avatar:
                self.fields['avatar'].initial = self.instance.avatar

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background-color: #F5F5DC'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background-color: #F5F5DC'
        })

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
                profile.save()
        return profile

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Enter tags separated by commas")

    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #F5F5DC'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'background-color: #F5F5DC', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        return [tag.strip() for tag in tags_str.split(',') if tag.strip()]

    def save(self, commit=True):
        question = super().save(commit=False)
        if self.user:
            question.author = self.user
        if commit:
            question.save()
            tags = self.cleaned_data.get('tags', [])
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'background-color: #F5F5DC', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = super().save(commit=False)
        if self.user:
            answer.author = self.user
        if self.question:
            answer.question = self.question
        if commit:
            answer.save()
        return answer
