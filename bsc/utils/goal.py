# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def get_graph_data(title, test):
    	chart = {
        	'data': {
			'labels': ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
			'datasets': [
				{ 'name': "Dataset 1", 'values': [18, 40, 30, 35, 8, 52, 17, -4] },
				{ 'name': "Dataset 2", 'values': [30, 50, -10, 15, 18, 32, 27, 14] }
			]
		}
   	}

	return chart
