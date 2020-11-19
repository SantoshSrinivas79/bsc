# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	
	columns = get_columns()
	data = get_initiative(filters)

	return columns, data

def get_columns():
	return [
		_("Department") + ":Link/Department:130",	
		_("BSC Indicator") + ":Link/BSC Indicator:100",
		_("Indicator Name") + ":Data:350",
		_("BSC Initiative") + ":Link/BSC Initiative:100",
		_("BSC Target Group") + ":Link/BSC Target Group:100",
		_("Initiative Target") + ":Int:40",	
		_("Initiative Count") + ":Int:30",
		_("Work Months") + ":Data:160",	
		_("Approved Budget") + ":Currency:80"
	]


def get_conditions(filters):
	conditions = []
	conditions.append("ini.docstatus < 2")
	if filters.get("department"): conditions.append("ini.department = %(department)s")
	if filters.get("fiscal_year"): conditions.append("ini.fiscal_year = %(fiscal_year)s")
	if filters.get("bsc_indicator"): conditions.append("tar.bsc_indicator = %(bsc_indicator)s")
	return "where {}".format(" and ".join(conditions)) if conditions else ""


def get_initiative(filters):
	ini_list = frappe.db.sql("""SELECT ini.department, tar.bsc_indicator, ind.full_name, ini.name, ini.initiative_group,
		ini.initiative_target, ini.initiative_count, 
		IFNULL(GROUP_CONCAT(inil.month order by inil.idx SEPARATOR ', '),"") as months,
		ini.total_amount
		FROM `tabBSC Target Month` inil
		INNER JOIN `tabBSC Initiative` ini on ini.name=inil.parent
		INNER JOIN `tabBSC Target` tar ON tar.name = ini.bsc_target 
		INNER JOIN `tabBSC Indicator` ind ON ind.name = tar.bsc_indicator 
		{conditions} group by inil.parent order by tar.bsc_indicator, ini.name 
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_list=1)

	return ini_list