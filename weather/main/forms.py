from django.forms import ModelForm, TextInput
from .models import Block



# ModelForm links created form to model while defining the form
# sothat i dont need to create an obj in view func for added city, just gonna save it to db
class BlockForm(ModelForm):
    class Meta:
        model = Block
        fields = ["city"]
        widget = {"city": TextInput(attrs={"class": "input", "placeholder": "City name"}),
        }

# 3 steps need to be followed:
# - get hold of it in the view (fetch it from the database, for example)
        # (i already did it above)
# - pass it to the template context
# - expand it to HTML markup using template variables