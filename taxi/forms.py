from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# pega dinamicamente o modelo de usuário (pode ser User ou um custom user)
UserModel = get_user_model()


def validate_license_number(value):
    import re
    if not re.match(r"^[A-Z]{3}\d{5}$", value):
        raise ValidationError("O número da licença deve ter 3 letras maiúsculas seguidos de 5 dígitos (ex: ABC12345).")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
        help_text="Formato: ABC12345 (3 letras maiúsculas + 5 dígitos)",
    )

    class Meta:
        model = UserModel
        # caso o seu User model NÃO contenha license_number, substitua por ('profile__license_number',) conforme seu design.
        fields = ["license_number"]


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_number],
        help_text="Formato: ABC12345 (3 letras maiúsculas + 5 dígitos)",
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = forms.models.get_model("taxi", "Car") if hasattr(forms.models, "get_model") else None
        # fallback: se seu projeto tem um modelo Car em taxi.models, importe localmente ou ajuste.
        # Para evitar erro nesta cópia, definiremos fields = "__all__" abaixo (troque se necessário)
        fields = "__all__"
