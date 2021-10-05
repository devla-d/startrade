from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth  import login,authenticate,logout
from .models import Account




COUNTRY  = (
		('FIRST', "First"),
		('SECOND', "Second"),
	)

 


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'placeholder':"Email"
            }
        ),
        label = '',
        required=True
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder':"Username"
            }
        ),
        label = '',
        required=True
    )
    password1 = forms.CharField( max_length=30, min_length=6,label='', widget=forms.PasswordInput(attrs={'placeholder': "PASSWORD", 'class': 'form-control',}))
    #password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': "CONFIRM PASSWORD", 'class': 'form-control',}))

    class Meta:
        model = Account
        fields = ('username','email','password1')

    '''def clean_password1(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        #password2 = self.cleaned_data.get("password2")
        if password1.lenght > 6:
            raise ValidationError("Password must be greeter than 6")
        return password1'''

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]








class LoginForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                "placeholder":'EMAIL'
            }
        ),
        label = '',
        required=True
    )
    password = forms.CharField( max_length=30, min_length=6,label='', widget=forms.PasswordInput(attrs={'placeholder': "PASSWORD", 'class': 'form-control',}))

    class Meta:
        model = Account
        fields = ['email','password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password =  self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError('Invalid Credentials Note : Make Sure Your Email Address Is Verified')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label = '',
        required=True
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = '',
        required=True
    )
   
    class Meta:
        model = Account
        fields = ['username','email']




class UserUpdateForm(forms.ModelForm):
 
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'FIRSTNAME'
            }
        ),
        label = '',
        required=True
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'LASTNAME'
            }
        ),
        label = '',
        required=True
    )
    postalcode = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'ZIPCODE'
            }
        ),
        label = '',
        required=True
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'ADDRESS'
            }
        ),
        label = '',
        required=True
    )
    country = forms.CharField(
            widget=forms.Select(
                choices = COUNTRY,
                attrs={
                    'class': 'browser-default custom-select',
                     'class': 'form-control',
                }
            ),
            label = "",
            required=True
        )

    date_of_birth = forms.DateTimeField(
            widget=forms.TextInput(
                attrs={
                    'type': 'date',
                     'class': 'form-control',
                }
            ),
             label = '',
            required=True)

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                'placeholder':'9090775808'
            }
        ),
        label = "",
         required=True
    )
   
    class Meta:
        model = Account
        fields = ['first_name','last_name','address','phone','date_of_birth','country','postalcode']










class PasswordChangeForm(forms.ModelForm):
    user_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'hidden',
                'class': 'form-control',
                 
            }
        ),
        label = "",
         required=True
    )
    oldpassword = forms.CharField( max_length=30, min_length=6,label='', widget=forms.PasswordInput(attrs={'placeholder': "OLD PASSWORD", 'class': 'form-control',}))
    password1 = forms.CharField( max_length=30, min_length=6,label='', widget=forms.PasswordInput(attrs={'placeholder': "NEW PASSWORD", 'class': 'form-control',}))
    password2 = forms.CharField( max_length=30, min_length=6,label='', widget=forms.PasswordInput(attrs={'placeholder': "CONFIRN NEW PASSWORD", 'class': 'form-control',}))

    class Meta:
        model = Account
        fields = ['user_id','oldpassword','password1','password2']

    def clean(self):
        if self.is_valid():
            user_id = int(self.cleaned_data['user_id'])
            oldpassword = self.cleaned_data['oldpassword']
            password1 =  self.cleaned_data['password1']
            password2 =  self.cleaned_data['password2']
            user = Account.objects.get(id=user_id)
            if password1 != password2:
                raise forms.ValidationError("Passwords don\'t match")
            if not user.check_password(oldpassword):
                raise forms.ValidationError("Old password don\'t match")