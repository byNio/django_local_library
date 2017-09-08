from django import forms #provide Form class inside

from django.core.exceptions import ValidationError #to raise error in user input
from django.utils.translation import ugettext_lazy as _ #for translation feature
import datetime #to access date and time in django system

class RenewBookForm(forms.Form):
	#there are many arguments to be put in Field(args)
	#such as required, label, label_suffix, initial, help_text, error_message, etc
	#if label is not specified then django create one from field name(renewal_date -> Renewal date:)
	#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
	renewal_date = forms.DateField(help_text="Enter a date up to 4 weeks from now (default 3)")
	
	#override method clean_<field_name>() for user input validation
	def clean_renewal_date(self):
		#sanitise data:
		#self.cleaned_data['fields'] is very important to sanitise user input for security
		sntzd_renewal_date = self.cleaned_data['renewal_date']
		
		#validate data:
		if sntzd_renewal_date < datetime.date.today():
			#the _ in ValidationError is ugettext_lazy() for translation feature
			raise ValidationError(_('Invalid date - cannot choose before today'))
		if sntzd_renewal_date > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Invalid date - cannot choose date more than 4 weeks'))
		
		#data after sanitised and validated:
		return sntzd_renewal_date
