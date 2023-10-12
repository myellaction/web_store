from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from django.forms.widgets import HiddenInput
from .models import *
from django.db.models import Min, Max, Q
from django.contrib.auth.password_validation import get_password_validators, validate_password, password_validators_help_texts
from webstore.settings import AUTH_PASSWORD_VALIDATORS


class StoreAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин или электронная почта',
        widget=forms.TextInput(attrs={'autofocus': True, 'readonly': 'true', 'onfocus': "this.removeAttribute('readonly')"}))
    password = forms.CharField(label='Пароль', widget = forms.PasswordInput(attrs={'readonly': 'true', 'onfocus': "this.removeAttribute('readonly')"}))
    error_messages = {
        "invalid_login": (
            "Логин/электронная почта и пароль введены некорректно. Обратите внимание на регистр."
        ),
        "inactive": ("Аккаунт заблокирован."),
    }

    def is_valid(self):
        username_or_email = self.data.get('username')
        if '@' in username_or_email:
            userquery = User.objects.filter(email=username_or_email)
            if not userquery:
                return False
            else:
                username = userquery[0].username
        else:
            username = username_or_email
        password = self.data.get('password')
        res = authenticate(username=username, password=password)
        if res:
            self.authenticate_res = res
            return True
        return False


class RegisterBuyerForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Ваше имя', help_text='длинна не должна превышать 50 символов', error_messages={
        'invalid': 'длинна не должна превышать 50 символов'})
    username = forms.CharField(max_length=50, label='Логин', help_text='длинна не должна превышать 50 символов', error_messages={
        'invalid': 'длинна не должна превышать 50 символов'}, widget=forms.TextInput(attrs={'readonly': 'true', 'onfocus': "this.removeAttribute('readonly')"}))
    email = forms.EmailField(label='Электронная почта', error_messages={'invalid':'введите корректный адрес электронной почты'})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'register-section__password-input', 'readonly': 'true', 'onfocus': "this.removeAttribute('readonly')"}), label='Пароль', help_text=password_validators_help_texts)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повтор пароля', help_text='пароли должны совпадать')
    allow_mail = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-register'}), label='Разрешить рассылку', required=False)

    def clean_password1(self):
        value = self.cleaned_data.get('password1')
        validator_config = get_password_validators(AUTH_PASSWORD_VALIDATORS)
        validate_password(value, validator_config)
        return value

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            raise ValidationError('пользователь с такой электронной почтой уже зарегистрирован')
        return self.cleaned_data['email']

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('пароли не совпадают')


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label='Имя', error_messages={
        'invalid': 'длинна не должна превышать 50 символов'})
    username = forms.CharField(max_length=50, label='Логин', error_messages={
        'invalid': 'длинна не должна превышать 50 символов'}, widget=forms.TextInput(attrs={'readonly': 'true', 'onfocus': "this.removeAttribute('readonly')"}))
    email = forms.EmailField(label='Электронная почта', error_messages={'invalid': 'некорректный адрес электронной почты'})
    allow_mail = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox-register'}), label='Разрешить рассылку', required=False)

    def clean_email(self):
        if User.objects.filter(~Q(pk=self.user_id), email=self.cleaned_data['email']):
            raise ValidationError('пользователь с такой электронной почтой уже зарегистрирован')
        return self.cleaned_data['email']

    def save(self, commit=True):
        if 'allow_mail' in self.changed_data:
            allow_mail = self.cleaned_data['allow_mail']
            buyer = Buyer.objects.get(user__pk=self.user_id)
            buyer.allow_mail = allow_mail
            buyer.save()
        self.cleaned_data.pop('allow_mail')
        return super().save()

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'allow_mail')


class StoreReviewForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', error_messages={'invalid': 'некорректный адрес электронной почты'})
    class Meta:
        model = StoreReview
        fields = ('name', 'email', 'content', 'buyer')


class ReviewForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', error_messages={'invalid': 'некорректный адрес электронной почты'})
    class Meta:
        model = Review
        fields = ('name', 'email', 'content', 'buyer', 'item', 'to_review')


class ProfilePasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label= ("Введите адрес электронной почты"),
        max_length=254,
        widget=forms.EmailInput(attrs={"readonly": "true", 'onfocus': "this.removeAttribute('readonly')"}),
        error_messages = {'invalid': 'некорректный адрес электронной почты'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email):
            raise ValidationError('пользователь с такой электронной почтой не найден')
        return email


class ProfileNewPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": ("пароли не совпадают"),
    }
    new_password1 = forms.CharField(
        label= ("Новый пароль"),
        widget=forms.PasswordInput(attrs={'class': 'register-section__password-input', "readonly": "true", 'onfocus': "this.removeAttribute('readonly')"}),
        strip=False,
        help_text=password_validators_help_texts,
    )
    new_password2 = forms.CharField(
        label= ("Повтор нового пароля"),
        strip=False,
        widget=forms.PasswordInput(attrs={"readonly": "true", 'onfocus': "this.removeAttribute('readonly')"}),
    )


class MakeOrderForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.HiddenInput(), required=False)
    buyer = forms.ModelChoiceField(queryset=Buyer.objects.all(), widget=forms.HiddenInput(), required=False)
    amount = forms.IntegerField(label='Количество')
    delivery = forms.ModelChoiceField(queryset=OrderDelivery.objects.all(), label='Способ доставки', empty_label=None)
    address = forms.CharField(label='Адрес доставки', max_length=250)
    comment = forms.CharField(widget=forms.Textarea(), label='Комментарий', max_length=2000, required=False)

    class Meta:
        model = OrderItem
        exclude = ('status', 'created')

    def is_valid(self):
        res = super().is_valid()
        print(self.errors)
        return res


class ItemShopCartOrder(forms.ModelForm):
    buyer = forms.ModelChoiceField(queryset=Buyer.objects.all(), widget=forms.HiddenInput())
    item = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.HiddenInput())
    amount = forms.IntegerField(label='Количество', required=False, widget=forms.NumberInput(attrs={'placeholder': 1, 'class': 'no_placeholder_click'}))

    class Meta:
        model = ShopCart
        fields = '__all__'






