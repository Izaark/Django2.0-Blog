from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget #PagedownWidget add widgets to template only is esthetic :D

#PostForm inherit all from post models as modelform
class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget(show_preview=False))

	class Meta:
		model = Post
		fields = ['title','content','image','draft','publish']

		labels = {
			'title':'Titulo',
			'image':'Imagen',
			'draft':'Borrador',
			'publish':'Publicar',
		}
		widgets = {'publish':forms.SelectDateWidget(),}