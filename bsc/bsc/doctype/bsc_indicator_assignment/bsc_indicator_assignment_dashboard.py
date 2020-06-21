from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'bsc_indicator_assignment',
		'transactions': [
			{
				'label': '',
				'items': ['BSC Initiative', 'BSC Target']
			}
		]
	}
