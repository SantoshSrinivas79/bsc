# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	if filters.get('month'):
		filters.month= frappe.parse_json(filters.get("month"))

	columns = get_columns()
	data = get_initiative(filters)

	return columns, data

def get_columns():
	return [
		_("Department") + ":Link/Department:130",	
		_("BSC Indicator") + ":Link/BSC Indicator:100",
		_("BSC Initiative") + ":Link/BSC Initiative:100",
		_("Initiative Name") + ":Data:200",
		_("Month") + ":Data:80",	
		_("Is Achieved") + ":Data:80",	
		_("Weakness Reasons") + ":Data:200",
		_("Suggested Solutions") + ":Data:200"
	]


def get_conditions(filters):
	conditions = []
	if filters.get("department"): conditions.append("log.department = %(department)s")
	if filters.get("month"): conditions.append("log.month in %(month)s")
	if filters.get("fiscal_year"): conditions.append("log.fiscal_year = %(fiscal_year)s")
	if filters.get("bsc_indicator"): conditions.append("ini.bsc_indicator = %(bsc_indicator)s")
	return "where {}".format(" and ".join(conditions)) if conditions else ""


def get_initiative(filters):
	log_list = frappe.db.sql("""SELECT log.department, ini.bsc_indicator, log.bsc_initiative, ini.initiative_name, log.month,
		log.is_achieved, log.weakness_reasons, log.suggested_solutions
		FROM `tabBSC Initiative Log` log INNER JOIN `tabBSC Initiative` ini ON ini.name = log.bsc_initiative
		{conditions} order by log.department, log.bsc_initiative
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_list=1)

	return log_list