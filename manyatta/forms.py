from django import forms


class SearchForm(forms.Form):
    query = forms.CharField()


class EmailForm(forms.Form):
    email = forms.EmailField()


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
