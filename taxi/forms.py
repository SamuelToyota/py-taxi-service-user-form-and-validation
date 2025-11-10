from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from .models import Driver, Car


def validate_license_number(value):
    """
    Deve ter 8 caracteres, 3 letras maiúsculas + 5 dígitos.
    Exemplo válido: ABC12345
    """
    import re
    if not re.match(r"^[A-Z]{3}\d{5}$", value):
        raise ValidationError("O número da licença deve ter 3 letras maiúsculas seguidas de 5 dígitos.")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
        help_text="Formato: ABC12345 (3 letras + 5 números)",
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
        help_text="Formato: ABC12345 (3 letras + 5 números)",
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
