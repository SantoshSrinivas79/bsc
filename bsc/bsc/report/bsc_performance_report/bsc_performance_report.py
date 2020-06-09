# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import (flt,cstr)
from frappe import _, throw

def execute(filters=None):
	if not filters: filters = {}
	if filters.get('month'):
		filters.month= frappe.parse_json(filters.get("month"))

	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_columns():
	return [
		{
			"fieldname": "account",
			"label": _("indicator"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "parent_account",
			"label": _("parent_indicator"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "perc",
			"label": _("perc"),
			"fieldtype": "Data",
			"width": 300
		}
	]


def get_conditions(filters):
	conditions = []
	#if filters.get("department"): conditions.append("log.department = %(department)s")
	#if filters.get("month"): conditions.append("log.month in %(month)s")
	#if filters.get("fiscal_year"): conditions.append("log.fiscal_year = %(fiscal_year)s")
	#if filters.get("bsc_indicator"): conditions.append("ini.bsc_indicator = %(bsc_indicator)s")
	return "{}".format(" and ".join(conditions)) if conditions else ""


def get_indicator(filters):
	ind_map = frappe._dict()
	ind_list = frappe.db.sql("""SELECT ind.name, ind.name as indicator, ind.full_name as indicator_name, 
		ind.bsc_objective as objective, ind.bsc_objective as parent, obj.full_name as objective_name,
		obj.bsc_perspective as perspective, per.full_name as perspective_name FROM `tabBSC Indicator` ind 
		INNER JOIN `tabBSC Objective` obj ON obj.name = ind.bsc_objective
		INNER JOIN `tabBSC Perspective` per ON per.name = obj.bsc_perspective
		{conditions} 
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_dict=True)
	for ind in ind_list:
		if ind:
			ind_map.setdefault(ind.indicator, ind)
	return ind_map


def get_data(filters):
	indicators=get_indicator(filters)
	indicators, indicators_by_name, parent_children_map = filter_indicators(indicators)
	data = prepare_data(indicators, filters, parent_children_map, indicators_by_name)
	return data

def filter_indicators(indicators, depth=10):
	#frappe.throw(_("indicators={0}").format(indicators))

	parent_children_map = {}
	indicators_by_name = {}
	for d in sorted(indicators):
		ind_det = indicators.get(d)
		#frappe.throw(_("ind_det={0}").format(ind_det))

		#d.setdefault(d.indicator or None, [])	
			
		indicators_by_name[ind_det.indicator] = ind_det
		type = indicators_by_name[ind_det.indicator].get("type",None)
		if not type:
			indicators_by_name[ind_det.indicator]["type"]='ind'
			indicators_by_name[ind_det.indicator]["display"] = ind_det.indicator_name
		type = indicators_by_name[ind_det.indicator].get("type",None)

		if type == 'ind':		
			parent_children_map.setdefault(ind_det.objective or None, []).append(d)		
		elif type == 'obj':		
			parent_children_map.setdefault(ind_det.perspective or None, []).append(d)		
		elif type == 'per':		
			parent_children_map.setdefault(None, []).append(d)

		indicators_by_name[ind_det.indicator]['ini_target'] = flt(frappe.db.sql("""SELECT IFNULL(count(ini.month_count),0.0) as ini_target
			FROM `tabBSC Initiative` ini 
			where ini.bsc_indicator=%(indicator)s and ini.docstatus=1
			""",{'indicator':ind_det.indicator})[0][0])
		indicators_by_name[ind_det.indicator]['ini_achieved'] = flt(frappe.db.sql("""SELECT IFNULL(count(log.name),0.0) as ini_achieved
			FROM `tabBSC Initiative Log` log 
			INNER JOIN `tabBSC Initiative` ini ON ini.name = log.bsc_initiative 
			where ini.bsc_indicator=%(indicator)s and log.docstatus=1 and log.is_achieved='Yes'
			""",{'indicator':ind_det.indicator})[0][0])
		indicators_by_name[ind_det.indicator]['tar_target'] = flt(frappe.db.sql("""SELECT sum(tar.target) as tar_target
			FROM `tabBSC Target` tar 
			where tar.bsc_indicator=%(indicator)s and tar.docstatus=1
			""",{'indicator':ind_det.indicator})[0][0])
		indicators_by_name[ind_det.indicator]['tar_achieved'] = flt(frappe.db.sql("""SELECT sum(log.achieved) as tar_achieved
			FROM `tabBSC Target Log` log 
			INNER JOIN `tabBSC Target` tar ON tar.name = log.bsc_Target 
			where tar.bsc_indicator=%(indicator)s and log.docstatus=1
			""",{'indicator':ind_det.indicator})[0][0])
		if indicators_by_name[ind_det.indicator].get("ini_target",0.0) == 0.0 :
			indicators_by_name[ind_det.indicator]['ini'] = 0.0
		else:
			indicators_by_name[ind_det.indicator]['ini'] = \
				indicators_by_name[ind_det.indicator].get("ini_achieved",0.0) / indicators_by_name[ind_det.indicator].get("ini_target",0.0) * 100
		if indicators_by_name[ind_det.indicator].get("tar_target",0.0) == 0.0:
			indicators_by_name[ind_det.indicator]['tar']= 0.0
		else:
			indicators_by_name[ind_det.indicator]['tar'] = \
				indicators_by_name[ind_det.indicator].get("tar_achieved",0.0) / indicators_by_name[ind_det.indicator].get("tar_target",0.0) * 100
		if indicators_by_name[ind_det.indicator].get("tar",0.0) == 0.0:
			indicators_by_name[ind_det.indicator]['all'] = 0.0
		else:
			indicators_by_name[ind_det.indicator]['all'] = \
				(indicators_by_name[ind_det.indicator].get("ini",0.0) + indicators_by_name[ind_det.indicator].get("tar",0.0)) / 2

		obj=indicators.get(ind_det.objective)
		if not obj:
			#frappe.msgprint("in not obj {0}".format(ind_det.objective))
			indicators[ind_det.objective]={}
			indicators[ind_det.objective]["indicator"]=ind_det.objective
			indicators[ind_det.objective]["parent"]=ind_det.perspective
			indicators[ind_det.objective].setdefault(ind_det.objective or None, [])
			parent_children_map.setdefault(ind_det.perspective or None, []).append(indicators[ind_det.objective])
			indicators_by_name[ind_det.objective] = indicators[ind_det.objective]
			#indicators_by_name[ind_det.objective]["indicator"]=indicators[ind_det.objective]
			indicators_by_name[ind_det.objective]["type"]='obj'
			indicators_by_name[ind_det.objective]["display"] = ind_det.objective_name
			indicators_by_name[ind_det.objective]["ini_target"]=indicators_by_name[ind_det.indicator].get("ini_target",0.0)
			indicators_by_name[ind_det.objective]["tar_target"]=indicators_by_name[ind_det.indicator].get("tar_target",0.0)
		indicators_by_name[ind_det.objective]['ini'] = (indicators_by_name[ind_det.objective].get("ini",0.0)+indicators_by_name[ind_det.indicator]['ini'])
		indicators_by_name[ind_det.objective]['tar'] = (indicators_by_name[ind_det.objective].get("tar",0.0)+indicators_by_name[ind_det.indicator]['tar'])
		indicators_by_name[ind_det.objective]['all'] = (indicators_by_name[ind_det.objective].get("all",0.0)+indicators_by_name[ind_det.indicator]['all'])
		
		per=indicators.get(ind_det.perspective)
		if not per:
			#frappe.msgprint("in not per {0}".format(ind_det.perspective))
			indicators[ind_det.perspective]={}
			indicators[ind_det.perspective]["indicator"]=ind_det.perspective
			indicators[ind_det.perspective]["parent"]=None
			indicators[ind_det.perspective].setdefault(ind_det.perspective or None, [])
			parent_children_map.setdefault(ind_det.perspective or None, []).append(indicators[ind_det.perspective])
			indicators_by_name[ind_det.perspective] = indicators[ind_det.perspective]
			#indicators_by_name[ind_det.perspective]["indicator"]=indicators[ind_det.perspective]
			indicators_by_name[ind_det.perspective]["type"]='per'
			indicators_by_name[ind_det.perspective]["display"] = ind_det.perspective_name
			indicators_by_name[ind_det.perspective]["ini_target"]=indicators_by_name[ind_det.indicator].get("ini_target",0.0)
			indicators_by_name[ind_det.perspective]["tar_target"]=indicators_by_name[ind_det.indicator].get("tar_target",0.0)
		indicators_by_name[ind_det.perspective]['ini'] = (indicators_by_name[ind_det.perspective].get("ini",0.0)+indicators_by_name[ind_det.indicator]['ini'])
		indicators_by_name[ind_det.perspective]['tar'] = (indicators_by_name[ind_det.perspective].get("tar",0.0)+indicators_by_name[ind_det.indicator]['tar'])
		indicators_by_name[ind_det.perspective]['all'] = (indicators_by_name[ind_det.perspective].get("all",0.0)+indicators_by_name[ind_det.indicator]['all'])

	return indicators, indicators_by_name, parent_children_map


def prepare_data(indicators, filters, parent_children_map,indicators_by_name):
	indicators2 = {}
	count=100000
	#indicators=sorted(indicators)
	for d in sorted(indicators):
		count-=1
		ind_det = indicators.get(d)
		indicators2.setdefault(count,ind_det)
		#frappe.msgprint("count {0} and d={1}={2}".format(count,d,ind_det))
		#
		#frappe.msgprint("ccccccccount {0} and d={1}={2}".format(count,d,indicators_by_name[d]))

	#frappe.throw(_("indicators={0}"))
	data = []
	for d in sorted(indicators2):
		count+=1
		ind_det = indicators2.get(d)
		frappe.msgprint("d== {0} and === {1}".format(d,ind_det))

		dd=indicators2[d].get("indicator",None)
		frappe.msgprint("indicator=== {0} ".format(dd))

		#if not dd:
		#	frappe.throw(_("heeeeer={0}").format(d))
		#if count ==7:
		#	frappe.msgprint("count {0} and d={1}={2}".format(count,d,ind_det))
		#else:
		#	frappe.msgprint("count {0} and d={1}={2}".format(count,d,ind_det))

		#if indicators_by_name[dd].get("ini_target",0.0) > 0.0 \
		#and indicators_by_name[dd].get("tar_target",0.0) > 0.0 :
		type=indicators_by_name[dd].get("type",'ind')
		ndent=0
		if type:
			if type == 'ind': indent=2
			elif type == 'obj': indent=1
			elif type == 'per': indent=0

		row = {
			"account": indicators_by_name[dd]["indicator"],
			"account_name": indicators_by_name[dd]["display"],
			"parent_account": indicators_by_name[dd]["parent"],
			"indent": indent,
			"perc": flt(indicators_by_name[dd]["all"])
		}
		data.append(row)
		xx=indicators_by_name[dd]["indicator"]
		yy=indicators_by_name[dd]["display"]
		frappe.msgprint("1=== {0} ".format(xx))
		frappe.msgprint("2=== {0} ".format(yy))
		frappe.msgprint("3=== {0} ".format(indicators_by_name[dd]["parent"]))
		frappe.msgprint("4=== {0} ".format(flt(indicators_by_name[dd]["all"],2)))
			
		frappe.msgprint("row={0}".format(row))

		#frappe.throw(_("ind_det={0}").format(d))

	data.extend([{}])

	return data
