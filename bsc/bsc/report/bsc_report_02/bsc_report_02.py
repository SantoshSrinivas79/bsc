# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import (flt,cstr)
from frappe import _, throw


def execute(filters=None):
	if not filters: filters = {}
	month= {}

	month["jan"] = []
	month["feb"] = []
	month["mar"] = []
	month["apr"] = []
	month["may"] = []
	month["jun"] = []
	month["jul"] = []
	month["aug"] = []
	month["sep"] = []
	month["oct"] = []
	month["nov"] = []
	month["dec"] = []


	if filters.get('department'):
		filters.department= frappe.parse_json(filters.get("department"))
	if filters.get('bsc_month'):
		filters.bsc_month= frappe.parse_json(filters.get("bsc_month"))

	columns = get_columns(filters)

	data = []
	ind_map = get_indicators(filters)
	#frappe.throw(_("ind_map = {0}").format(ind_map))

	labels = []
	datasets = []

	for ind in sorted(ind_map):
		ind_det = ind_map.get(ind)
		if not ind_det:
			continue
		row = [ind_det.department]
		row.extend([cstr(flt(ind_det.jan_/ind_det.jan*100.0,2))+"%" if ind_det.jan>0 else "",
			cstr(flt(ind_det.feb_/ind_det.feb*100.0,2))+"%" if ind_det.feb>0 else "",
			cstr(flt(ind_det.mar_/ind_det.mar*100.0,2))+"%" if ind_det.mar>0 else "",
			cstr(flt(ind_det.apr_/ind_det.apr*100.0,2))+"%" if ind_det.apr>0 else "",
			cstr(flt(ind_det.may_/ind_det.may*100.0,2))+"%" if ind_det.may>0 else "",
			cstr(flt(ind_det.jun_/ind_det.jun*100.0,2))+"%" if ind_det.jun>0 else "",
			cstr(flt(ind_det.jul_/ind_det.jul*100.0,2))+"%" if ind_det.jul>0 else "",
			cstr(flt(ind_det.aug_/ind_det.aug*100.0,2))+"%" if ind_det.aug>0 else "",
			cstr(flt(ind_det.sep_/ind_det.sep*100.0,2))+"%" if ind_det.sep>0 else "",
			cstr(flt(ind_det.oct_/ind_det.oct*100.0,2))+"%" if ind_det.oct>0 else "",
			cstr(flt(ind_det.nov_/ind_det.nov*100.0,2))+"%" if ind_det.nov>0 else "",
			cstr(flt(ind_det.dec_/ind_det.dec*100.0,2))+"%" if ind_det.dec>0 else "",
			filters.get("fiscal_year")])
		data.append(row)

		labels+=[ind_det.department]

		month["jan"].append(flt(ind_det.jan_/ind_det.jan*100.0,2) if ind_det.jan>0 else "")
		month["feb"].append(flt(ind_det.feb_/ind_det.feb*100.0,2) if ind_det.feb>0 else "")
		month["mar"].append(flt(ind_det.mar_/ind_det.mar*100.0,2) if ind_det.mar>0 else "")
		month["apr"].append(flt(ind_det.apr_/ind_det.apr*100.0,2) if ind_det.apr>0 else "")
		month["may"].append(flt(ind_det.may_/ind_det.may*100.0,2) if ind_det.may>0 else "")
		month["jun"].append(flt(ind_det.jun_/ind_det.jun*100.0,2) if ind_det.jun>0 else "")
		month["jul"].append(flt(ind_det.jul_/ind_det.jul*100.0,2) if ind_det.jul>0 else "")
		month["aug"].append(flt(ind_det.aug_/ind_det.aug*100.0,2) if ind_det.aug>0 else "")
		month["sep"].append(flt(ind_det.sep_/ind_det.sep*100.0,2) if ind_det.sep>0 else "")
		month["oct"].append(flt(ind_det.oct_/ind_det.oct*100.0,2) if ind_det.oct>0 else "")
		month["nov"].append(flt(ind_det.nov_/ind_det.nov*100.0,2) if ind_det.nov>0 else "")
		month["dec"].append(flt(ind_det.dec_/ind_det.dec*100.0,2) if ind_det.dec>0 else "")

	months = filters.get("bsc_month")
	if not months:
		months=[]
	if 'Jan' in months or months == []:
		datasets.append({
			'name':'Jan','values':month["jan"]
		})
	if 'Feb' in months or months == []:
		datasets.append({
			'name':'Feb','values':month["feb"]
		})
	if 'Mar' in months or months == []:
		datasets.append({
			'name':'Mar','values':month["mar"]
		})
	if 'Apr' in months or months == []:
		datasets.append({
			'name':'Apr','values':month["apr"]
		})
	if 'May' in months or months == []:
		datasets.append({
			'name':'May','values':month["may"]
		})
	if 'Jun' in months or months == []:
		datasets.append({
			'name':'Jun','values':month["jun"]
		})
	if 'Jul' in months or months == []:
		datasets.append({
			'name':'Jul','values':month["jul"]
		})
	if 'Aug' in months or months == []:
		datasets.append({
			'name':'Aug','values':month["aug"]
		})
	if 'Sep' in months or months == []:
		datasets.append({
			'name':'Sep','values':month["sep"]
		})
	if 'Oct' in months or months == []:
		datasets.append({
			'name':'Oct','values':month["oct"]
		})
	if 'Nov' in months or months == []:
		datasets.append({
			'name':'Nov','values':month["nov"]
		})
	if 'Dec' in months or months == []:
		datasets.append({
			'name':'Dec','values':month["dec"]
		})

    	chart = {
        	"data": {
            		'labels': labels,
            		'datasets': datasets
        	}
   	}
  	chart["type"] = "line"
    	##chart["height"] = "140"
    	chart["colors"] = ['red']
	#frappe.throw(_("chart = {0}").format(chart))

	return columns, data, None, chart


def get_columns(filters):
	columns = [
		_("Department") + ":Link/Department:200"
	]
	months = filters.get("bsc_month")
	if months:
		months = []
	if 'Jan' in months or months == []:columns+=[_("Jan") + ":Data:60"]
	if 'Feb' in months or months == []:columns+=[_("Feb") + ":Data:60"]
	if 'Mar' in months or months == []:columns+=[_("Mar") + ":Data:60"]
	if 'Apr' in months or months == []:columns+=[_("Apr") + ":Data:60"]
	if 'May' in months or months == []:columns+=[_("May") + ":Data:60"]
	if 'Jun' in months or months == []:columns+=[_("Jun") + ":Data:60"]
	if 'Jul' in months or months == []:columns+=[_("Jul") + ":Data:60"]
	if 'Aug' in months or months == []:columns+=[_("Aug") + ":Data:60"]
	if 'Sep' in months or months == []:columns+=[_("Sep") + ":Data:60"]
	if 'Oct' in months or months == []:columns+=[_("Oct") + ":Data:60"]
	if 'Nov' in months or months == []:columns+=[_("Nov") + ":Data:60"]
	if 'Dec' in months or months == []:columns+=[_("Dec") + ":Data:60"]
	columns+=[_("Year") + ":Link/Fiscal Year:70"]
	return columns



def get_conditions(filters):
	conditions = []
	#if filters.get("department"): conditions.append("dep.name in (select t.department from `tabBSC Target` t group by t.department)")
	if filters.get("department"): 
		conditions.append("dep.name in %(department)s")
	else:
		conditions.append(" dep.name in (select t.department from `tabBSC Target` t group by t.department)")

	#if filters.get("department"): conditions.append("dep.name in %(department)s")
	#if filters.get("fiscal_year"): conditions.append("tar.fiscal_year = %(fiscal_year)s")
	return "where {}".format(" and ".join(conditions)) if conditions else ""

def get_indicators(filters):
	ind_map = frappe._dict()
	ind_list = frappe.db.sql("""SELECT dep.name as department,
		ifnull((select sum(tar.jan) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as jan, \
		ifnull((select sum(tar.feb) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as feb, \
		ifnull((select sum(tar.mar) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as mar, \
		ifnull((select sum(tar.apr) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as apr, \
		ifnull((select sum(tar.may) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as may, \
		ifnull((select sum(tar.jun) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as jun, \
		ifnull((select sum(tar.jul) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as jul, \
		ifnull((select sum(tar.aug) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as aug, \
		ifnull((select sum(tar.sep) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as sep, \
		ifnull((select sum(tar.oct) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as oct, \
		ifnull((select sum(tar.nov) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as nov, \
		ifnull((select sum(tar.dec) from `tabBSC Target` tar where tar.department=dep.name and tar.docstatus=1 and tar.fiscal_year=%(fiscal_year)s),0.0) as `dec`, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Jan' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as jan_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Feb' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as feb_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Mar' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as mar_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Apr' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as apr_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='May' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as may_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Jun' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as jun_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Jul' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as jul_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Aug' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as aug_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Sep' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as sep_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Oct' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as oct_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Nov' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as nov_, \
		ifnull((select sum(tar.achieved) from `tabBSC Target Log` tar where tar.month='Dec' and tar.docstatus=1 and tar.department=dep.name and tar.fiscal_year=%(fiscal_year)s),0.0) as dec_ \

		FROM `tabDepartment` dep {conditions} 
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_dict=1)
	for ind in ind_list:
		if ind:
			ind_map.setdefault(ind.department, ind)

	return ind_map