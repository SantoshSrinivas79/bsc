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
		tar, ach, per = get_tar(ind.bsc_indicator,ind.department,filters.get('fiscal_year'),0,filters)
		tar_, ach_, per_ = get_tar(ind.bsc_indicator,ind.department,filters.get('fiscal_year'),1,filters)
		if flt(tar)>0.0:
			if (filters.get("greater") == 1 and tar < ach) or (not filters.get("greater") or filters.get("greater")==0):
				data.append({
					"bsc_perspective": ind.bsc_perspective,
					"bsc_objective": ind.bsc_objective,
					"bsc_indicator": ind.bsc_indicator,
					"bsc_target": "",
					"indicator_name": ind.full_name,
					"department": ind.department,
					"target": tar,
					"achieved": ach,
					"percent": per,
					"target_year": tar_,
					"achieved_year": ach_,
					"percent_year": per_
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
	if filters.get("month"): conditions.append("tar.month in %(month)s")
	if filters.get("department"): conditions.append("tar.department in %(department)s")
	if filters.get("fiscal_year"): conditions.append("tar.fiscal_year = %(fiscal_year)s")
	if filters.get("bsc_indicator"): conditions.append("tar.bsc_indicator = %(bsc_indicator)s")
	if filters.get("bsc_objective"): conditions.append("ind.bsc_objective= %(bsc_objective)s")
	if filters.get("bsc_perspective"): conditions.append("ind.bsc_perspective= %(bsc_perspective)s")
	return "and {}".format(" and ".join(conditions)) if conditions else ""


def get_indicator(filters):
	ind_map = frappe._dict()
	ind_list = frappe.db.sql("""SELECT tar.bsc_indicator, ind.full_name, 
		ind.bsc_objective, ind.bsc_perspective, tar.department
		FROM `tabBSC Ledger Entry` tar 
		INNER JOIN `tabDepartment` dep ON dep.name = tar.department
		INNER JOIN `tabBSC Indicator` ind ON ind.name = tar.bsc_indicator
		{conditions} group by tar.bsc_indicator, tar.department order by dep.parent_department ASC
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_dict=True)
	return ind_list

def get_tar(ind,dep,year,total,filters):
	conditions = "  and bsc_indicator= '%s'" % ind.replace("'", "\\'")
	conditions += "  and fiscal_year= '%s'" % year.replace("'", "\\'")
	conditions += "  and department= '%s'" % dep.replace("'", "\\'")
	if total == 0:
		if filters.get("month"): conditions += "  and month in %(month)s"
	tar = frappe.db.sql("""SELECT IFNULL(sum(entry_number),0.0) FROM `tabBSC Ledger Entry` WHERE party_type='BSC Target' and entry_type='Targeted' %s""" % conditions,filters)
	ach = frappe.db.sql("""SELECT IFNULL(sum(entry_number),0.0) FROM `tabBSC Ledger Entry` WHERE party_type='BSC Target' and entry_type='Achieved' %s""" % conditions,filters)
	per = 0.0
	if tar:
		#frappe.msgprint("indicator=== {0} ".format(tar[0][0]))
		if flt(tar[0][0])>0.0:
			per = flt(((flt(ach[0][0])/flt(tar[0][0]))*100),2)
	return tar[0][0] if tar[0][0] else 0, ach[0][0] if ach[0][0] else 0, per if per else 0


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
			"fieldname": "bsc_target",
			"label": _("BSC Target"),
			"fieldtype": "Link",
			"options": "BSC Target",
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