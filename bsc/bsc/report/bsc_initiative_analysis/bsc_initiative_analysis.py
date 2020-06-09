# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	
	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_columns():
	return [
		_("Department") + ":Link/Department:130",
		_("BSC Perspective") + ":Link/BSC Perspective:100",
		_("BSC Objective") + ":Link/BSC Objective:100",
		_("BSC Indicator") + ":Link/BSC Indicator:100",
		_("Initiative Name") + ":Data:300",
		_("BSC Initiative Log") + ":Link/BSC Initiative Log:100",
		_("Month") + ":Data:40",
		_("Fiscal Year") + ":Data:40",
		_("is_achieved") + ":Data:70"	
		]


def get_conditions(filters):
	conditions = []
	if filters.get("department"): conditions.append("log.department = %(department)s")
	if filters.get("fiscal_year"): conditions.append("log.fiscal_year = %(fiscal_year)s")
	if filters.get("bsc_indicator"): conditions.append("tar.bsc_indicator = %(bsc_indicator)s")
	if filters.get("bsc_objective"): conditions.append("ind.bsc_objective = %(bsc_objective)s")
	if filters.get("bsc_perspective"): conditions.append("obj.bsc_perspective = %(bsc_perspective)s")
	if filters.get("bsc_month"): conditions.append("log.month = %(bsc_month)s")
	return "where {}".format(" and ".join(conditions)) if conditions else ""


def get_data(filters):
	ini_list = frappe.db.sql("""SELECT log.department, obj.bsc_perspective, 
		ind.bsc_objective, tar.bsc_indicator, tar.initiative_name, log.name, 
		log.month, log.fiscal_year, log.is_achieved
		FROM `tabBSC Initiative Log` log 
		INNER JOIN `tabBSC Initiative` tar ON log.bsc_initiative = tar.name
		INNER JOIN `tabBSC Indicator` ind ON tar.bsc_indicator = ind.name
		INNER JOIN `tabBSC Objective` obj ON ind.bsc_objective = obj.name
		{conditions} order by log.modified ASC
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_list=1)

	return ini_list
