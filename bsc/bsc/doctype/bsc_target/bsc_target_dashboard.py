from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'graph': True,
		'graph_method': "frappe.utils.bsc_goal.get_graph_data",
		'graph_method_args': {
			'title': _('')
		},
		'fieldname': 'bsc_target',
		'transactions': [
			{
				'label': '',
				'items': ['BSC Target Log']
			}
		]
	}
