from django import forms

class file_form(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="username",
        error_messages={'required': 'Please input username'},
        widget=forms.TextInput(
            attrs={
                'placeholder':"username",
                'class': "form-control",

            }
        ),
    )   
    password = forms.CharField(
        required=True,
        label="password",
        error_messages={'required': 'Please input password'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':"password",
                'class': "form-control",
            }
        ),
    ) 
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("name and pass is required")
        else:
            cleaned_data = super(LoginForm, self).clean()