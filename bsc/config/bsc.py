from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("BSC Initiative"),
			"items": [
				{
					"type": "doctype",
					"name": "BSC Initiative Log",
					"description":_("BSC Initiative Log"),
					"onboard": 1,
					"dependencies": ["BSC Initiative"],
				},
				{
					"type": "doctype",
					"name": "BSC Initiative",
					"description":_("BSC Initiative"),
					"onboard": 1,
					"dependencies": ["BSC Initiative Assignment"],

				},
				{
					"type": "doctype",
					"name": "BSC Initiative Assignment",
					"description":_("BSC Initiative Assignment"),
					"onboard": 1,
					"dependencies": ["BSC Indicator"],

				}
			]
		},
		{
			"label": _("BSC Target"),
			"items": [
				{
					"type": "doctype",
					"name": "BSC Target Log",
					"description":_("BSC Target Log"),
					"onboard": 1,
					"dependencies": ["BSC Target"],
				},
				{
					"type": "doctype",
					"name": "BSC Target",
					"description":_("BSC Target"),
					"onboard": 1,
					"dependencies": ["BSC Indicator"],

				}
			]
		},
		{
			"label": _("BSC Meeting"),
			"items": [
				{
					"type": "doctype",
					"name": "BSC Meeting",
					"description":_("BSC Meeting"),
				},
				{
					"type": "doctype",
					"name": "BSC Meeting Minutes",
					"description":_("BSC Meeting Minutes"),
					"onboard": 1,
					"dependencies": ["BSC Meeting"],
				},
				{
					"type": "doctype",
					"name": "BSC Meeting Recommendation",
					"description":_("BSC Meeting Recommendation"),
					"onboard": 1,
					"dependencies": ["BSC Meeting Minutes"],
				}
			]
		},
		{
			"label": _("Reports"),
			"icon": "fa fa-list",
			"items": [
				{
					"type": "report",
					"name": "BSC Initiative Analysis",
					"doctype": "BSC Initiative Log",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "BSC Target Analysis",
					"doctype": "BSC Target Log",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Department-wise Operation Plan and Program Budget",
					"doctype": "BSC Initiative",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Department-wise Initiative Achievement Report",
					"doctype": "BSC Initiative Log",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "BSC Performance Report",
					"doctype": "BSC Perspective",
					"is_query_report": True
				}
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "BSC Perspective",
					"description":_("BSC Perspective"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "BSC Objective",
					"description":_("BSC Objective"),
					"onboard": 1,
					"dependencies": ["BSC Perspective"],
				},
				{
					"type": "doctype",
					"name": "BSC Indicator",
					"description":_("BSC Indicator"),
					"onboard": 1,
					"dependencies": ["BSC Objective"],
				},
				{
					"type": "doctype",
					"name": "BSC Target Group",
					"description":_("BSC Target Group"),
					"onboard": 1
				},



			]
		},
	]