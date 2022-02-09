from django.forms import ModelForm
from .models import Room
# from .forms import RoomForm

class RoomForm(ModelForm):
  class Meta:
    model = Room
    fields = '__all__'
    exclude = ['host', 'participants']
