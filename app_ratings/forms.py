
import html
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit, MultiField, Div 
from django.forms import ModelForm
from app_ratings.models import Rating
from django.forms.widgets import NumberInput

class RangeInput(NumberInput):
    input_type = 'range'

class RateCountryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Vote out of 10',
                'score'
            ),
            Submit('save', 'Submit vote'),
        )
    
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': RangeInput(attrs={'min': 1, 'max': 10, 'step': 1, 'value': 1,'oninput':"num.value = this.value"}, )
        }
        labels = {
            'score': "What do you rate {{ country }} out of 10?"
        }
