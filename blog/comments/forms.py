from django import forms

# CommentForm form for comments !
class CommentForm(forms.Form):

	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	# parend_id = forms.IntegerField(widget=forms.HiddenInput ,required=False)
	content = forms.CharField(label='', widget=forms.Textarea)