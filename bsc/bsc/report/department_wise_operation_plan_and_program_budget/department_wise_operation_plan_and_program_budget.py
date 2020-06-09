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
		_("Target Total") + ":Int:40",	
		_("Time Total") + ":Int:30",
		_("Work Months") + ":Data:160",	
		_("Approved Budget") + ":Currency:80"
	]


def get_conditions(filters):
	conditions = []
	if filters.get("department"): conditions.append("ini.department = %(department)s")
	if filters.get("fiscal_year"): conditions.append("ini.fiscal_year = %(fiscal_year)s")
	if filters.get("bsc_indicator"): conditions.append("ini.bsc_indicator = %(bsc_indicator)s")
	return "where {}".format(" and ".join(conditions)) if conditions else ""


def get_initiative(filters):
	ini_list = frappe.db.sql("""SELECT ini.department, ini.bsc_indicator, ind.full_name, ini.name, ini.target_group,
		ini.target_total, ini.time_total, IFNULL(CONCAT_WS(',',IF(ini.jan>0,"1",NULL),IF(ini.feb>0,"2",NULL),
			IF(ini.mar>0,"3",NULL),IF(ini.apr>0,"4",NULL),
			IF(ini.may>0,"5",NULL),IF(ini.jun>0,"6",NULL),
			IF(ini.jul>0,"7",NULL),IF(ini.aug>0,"8",NULL),
			IF(ini.sep>0,"9",NULL),IF(ini.oct>0,"10",NULL),
			IF(ini.nov>0,"11",NULL),IF(ini.dec>0,"12",NULL)),"") as months,
		ini.total_amount
		FROM `tabBSC Initiative` ini INNER JOIN `tabBSC Indicator` ind ON ind.name = ini.bsc_indicator 
		{conditions} order by ini.bsc_indicator, ini.name
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_list=1)

	return ini_list