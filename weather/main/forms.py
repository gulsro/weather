from django.forms import ModelForm, TextInput
from .models import City

# ModelForm links created form to model while defining the form
# sothat i dont need to create an obj in view func for added city, just gonna save it to db
class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name"]
        widget = {"name": TextInput(attrs={"class": "input", "placeholder": "City Name"}),
        }

