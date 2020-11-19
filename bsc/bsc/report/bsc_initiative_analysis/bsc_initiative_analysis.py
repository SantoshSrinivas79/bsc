# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import (flt,cstr)

def execute(filters=None):
	if not filters: filters = {}
	formatted_data = []
	columns = get_columns()
	data = get_data(filters)
	for d in data:
		formatted_data.append({
			"department": d[0],
			"bsc_perspective": d[1],
			"bsc_objective": d[2],
			"bsc_indicator": d[3],
			"bsc_initiative_log": d[5],
			"initiative_name": d[4],
			"month": _(d[6]),
			"fiscal_year": d[7],
			"is_achieved": _(d[8])
		})
	formatted_data.extend([{}])
	return columns, formatted_data

def get_columns():
	return [
		{
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 130
		},
		{
			"fieldname": "bsc_perspective",
			"label": _("BSC Perspective"),
			"fieldtype": "Link",
			"options": "BSC Perspective",
			"width": 70
		},
		{
			"fieldname": "bsc_objective",
			"label": _("BSC Objective"),
			"fieldtype": "Link",
			"options": "BSC Objective",
			"width": 70
		},
		{
			"fieldname": "bsc_indicator",
			"label": _("BSC Indicator"),
			"fieldtype": "Link",
			"options": "BSC Indicator",
			"width": 70
		},
		{
			"fieldname": "bsc_initiative_log",
			"label": _("BSC Initiative Log"),
			"fieldtype": "Link",
			"options": "BSC Initiative Log",
			"width": 130
		},
		{
			"fieldname": "initiative_name",
			"label": _("Initiative Name"),
			"fieldtype": "Data",
			"width": 450
		},
		{
			"fieldname": "month",
			"label": _("Month"),
			"fieldtype": "Data",
			"width": 70
		},
		{
			"fieldname": "fiscal_year",
			"label": _("Fiscal Year"),
			"fieldtype": "Data",
			"width": 70
		},
		{
			"fieldname": "is_achieved",
			"label": _("Is Achieved"),
			"fieldtype": "Data",
			"width": 70
		}
		]


def get_conditions(filters):
	docstatus={"Draft":0,"Submitted":1}
	conditions = []
	if filters.get("department"): conditions.append("log.docstatus < 2")
	if filters.get("department"): conditions.append("log.department = %(department)s")
	if filters.get("fiscal_year"): conditions.append("log.fiscal_year = %(fiscal_year)s")
	if filters.get("bsc_indicator"): conditions.append("ind.name = %(bsc_indicator)s")
	if filters.get("bsc_objective"): conditions.append("obj.name = %(bsc_objective)s")
	if filters.get("bsc_perspective"): conditions.append("obj.bsc_perspective = %(bsc_perspective)s")
	if filters.get("bsc_month"): conditions.append("log.month = %(bsc_month)s")
	if filters.get("docstatus"): conditions.append("log.docstatus = %s"%cstr(docstatus[filters.get("docstatus")]))
	return "where {}".format(" and ".join(conditions)) if conditions else ""


def get_data(filters):
	ini_list = frappe.db.sql("""SELECT log.department, obj.bsc_perspective, 
		ind.bsc_objective, tarr.bsc_indicator, tar.initiative_name, log.name, 
		log.month, log.fiscal_year, log.is_achieved
		FROM `tabBSC Initiative Log` log 
		INNER JOIN `tabBSC Initiative` tar ON log.bsc_initiative = tar.name
		INNER JOIN `tabBSC Target` tarr ON tar.bsc_target = tarr.name
		INNER JOIN `tabBSC Indicator` ind ON tarr.bsc_indicator = ind.name
		INNER JOIN `tabBSC Objective` obj ON ind.bsc_objective = obj.name
		{conditions} order by log.modified ASC
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_list=1)

	return ini_list
