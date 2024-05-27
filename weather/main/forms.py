from django.forms import ModelForm, TextInput
from .models import City

# ModelForm links created form to model while defining the form
class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name"]
        widget = {"name": TextInput(attrs={"class": "input", "placeholder": "City Name"}),
        }

