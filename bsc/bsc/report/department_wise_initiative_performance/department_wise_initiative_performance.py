# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import (flt,cstr)
from frappe import _, throw

def execute(filters=None):
	columns, data = [], []
	if filters.get('department'):
		filters.department= frappe.parse_json(filters.get("department"))
	if filters.get('month'):
		filters.month= frappe.parse_json(filters.get("month"))

	columns = get_columns()
	data,chart= get_data(filters)
	
	return columns, data, None, chart

def get_data(filters):
	chartdata = {}

	data = []
	for ind in get_indicator(filters):
		#frappe.msgprint("indicator=== {0} ".format(ind.bsc_perspective))
		row = [ind.bsc_perspective, ind.bsc_objective, ind.bsc_indicator, ind.indicator_name, ind.department]
		tar, ach, per = get_tar(ind.bsc_indicator,filters.get("fiscal_year"),ind.department,filters)
		tar_, ach_, per_ = get_tar_total(ind.bsc_indicator,filters.get("fiscal_year"),ind.department)
		if (filters.get("greater") == 1 and tar < ach) or (not filters.get("greater") or filters.get("greater")==0):
			data.append({
				"bsc_perspective": ind.bsc_perspective,
				"bsc_objective": ind.bsc_objective,
				"bsc_indicator": ind.bsc_indicator,
				"bsc_target": ind.name,
				"indicator_name": ind.indicator_name,
				"department": ind.department,
				"target": tar,
				"achieved": ach,
				"percent": per,
				"target_year": tar_,
				"achieved_year": ach_,
				"percent_year": per
			})
			if not chartdata.get(ind.department):
				chartdata[ind.department] = {}
				chartdata[ind.department].setdefault(ind.department)
				chartdata[ind.department]['name'] = ind.department
			chartdata[ind.department]['perc'] = chartdata[ind.department].get('perc',0) + per
			chartdata[ind.department]['total'] = chartdata[ind.department].get('total',0) + 1
	data.extend([{}])
	labels=[]
	values=[]
	for child in chartdata:
		d=chartdata.get(child)
		labels+=[d.get('name','')]
		values+=[d.get('perc',0.0)/d.get('total',0.0) if d.get('total',0.0)>0 else 0]
	chart = {"data": {'labels': labels,'datasets': [{ 'values':values }],'yRegions': [{'label': _("Safe Line"),'start': 50,'end': 100,'options': { 'labelPos': 'right' }}]}}
	chart["type"] = "bar" if filters.get('chart_type')=='Bar' else 'line'
	return data, chart

def get_conditions(filters):
	conditions = []
	if filters.get("department"): conditions.append("tar.department in %(department)s")
	if filters.get("fiscal_year"): conditions.append("tar.fiscal_year = %(fiscal_year)s")
	if filters.get("bsc_indicator"): conditions.append("tar.bsc_indicator = %(bsc_indicator)s")
	if filters.get("bsc_objective"): conditions.append("ind.bsc_objective= %(bsc_objective)s")
	if filters.get("bsc_perspective"): conditions.append("ind.bsc_perspective= %(bsc_perspective)s")
	return "and {}".format(" and ".join(conditions)) if conditions else ""


def get_indicator(filters):
	ind_map = frappe._dict()
	ind_list = frappe.db.sql("""SELECT tar.name, tar.bsc_indicator, tar.indicator_name, 
		ind.bsc_objective, ind.bsc_perspective, tar.department, tar.target, tar.achieved, tar.per_target
		FROM `tabBSC Target` tar 
		INNER JOIN `tabDepartment` dep ON dep.name = tar.department
		INNER JOIN `tabBSC Indicator` ind ON ind.name = tar.bsc_indicator
		INNER JOIN `tabBSC Indicator Assignment` indas ON indas.name = tar.bsc_indicator_assignment
		where tar.docstatus=1 {conditions} order by dep.parent_department ASC
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_dict=True)
	return ind_list

def get_tar(ind,year,dep,filters):
	conditions = "  and bsc_indicator= '%s'" % ind.replace("'", "\\'")
	conditions += "  and fiscal_year= '%s'" % year.replace("'", "\\'")
	conditions += "  and department= '%s'" % dep.replace("'", "\\'")
	if filters.get("month"): conditions += "  and month in %(month)s"
	tar = frappe.db.sql("""SELECT count(entry_number) FROM `tabBSC Ledger Entry` WHERE party_type='BSC Initiative' and entry_type='Targeted' %s""" % conditions,filters)
	ach = frappe.db.sql("""SELECT sum(entry_number) FROM `tabBSC Ledger Entry` WHERE party_type='BSC Initiative' and entry_type='Achieved' and entry_number=1 %s""" % conditions,filters)
	per = flt(((flt(ach[0][0])/flt(tar[0][0]))*100),2) if tar[0][0]>0.0 else 0.0
	return tar[0][0] if tar[0][0] else 0.0, ach[0][0] if ach[0][0] else 0.0, per if per else 0.0

def get_tar_total(ind,year,dep):
	conditions = "  and bsc_indicator= '%s'" % ind.replace("'", "\\'")
	conditions += "  and fiscal_year= '%s'" % year.replace("'", "\\'")
	conditions += "  and department= '%s'" % dep.replace("'", "\\'")
	tar = frappe.db.sql("""SELECT count(entry_number) FROM `tabBSC Ledger Entry` WHERE party_type='BSC Initiative' and entry_type='Targeted' %s""" % conditions)
	ach = frappe.db.sql("""SELECT sum(entry_number) FROM `tabBSC Ledger Entry` WHERE party_type='BSC Initiative' and entry_type='Achieved' and entry_number=1 %s""" % conditions)
	per = flt(((flt(ach[0][0])/flt(tar[0][0]))*100),2) if tar[0][0]>0.0 else 0.0
	return tar[0][0] if tar[0][0] else 0.0, ach[0][0] if ach[0][0] else 0.0, per if per else 0.0


def get_columns():
	return [
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
			"fieldname": "bsc_indicator_assignment",
			"label": _("BSC Indicator Assignment"),
			"fieldtype": "Link",
			"options": "BSC Indicator Assignment",
			"width": 70
		},
		{
			"fieldname": "indicator_name",
			"label": _("Indicator Name"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "target",
			"label": _("Target"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "achieved",
			"label": _("Achieved"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "percent",
			"label": _("Percent"),
			"fieldtype": "Percent",
			"width": 60
		},
		{
			"fieldname": "target_year",
			"label": _("Target/Year"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "achieved_year",
			"label": _("Achieved/Year"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "percent_year",
			"label": _("Percent/Year"),
			"fieldtype": "Percent",
			"width": 60
		}

	]