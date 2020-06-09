# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import (flt,cstr)
from frappe import _, throw


def execute(filters=None):
	if not filters: filters = {}
	month_target= {}
	month_achieved= {}
	month_target["jan"] = 0.0
	month_target["feb"] = 0.0
	month_target["mar"] = 0.0
	month_target["apr"] = 0.0
	month_target["may"] = 0.0
	month_target["jun"] = 0.0
	month_target["jul"] = 0.0
	month_target["aug"] = 0.0
	month_target["sep"] = 0.0
	month_target["oct"] = 0.0
	month_target["nov"] = 0.0
	month_target["dec"] = 0.0
	month_achieved["jan"] = 0.0
	month_achieved["feb"] = 0.0
	month_achieved["mar"] = 0.0
	month_achieved["apr"] = 0.0
	month_achieved["may"] = 0.0
	month_achieved["jun"] = 0.0
	month_achieved["jul"] = 0.0
	month_achieved["aug"] = 0.0
	month_achieved["sep"] = 0.0
	month_achieved["oct"] = 0.0
	month_achieved["nov"] = 0.0
	month_achieved["dec"] = 0.0


	if filters.get('department'):
		filters.department= frappe.parse_json(filters.get("department"))
	if filters.get('bsc_indicator'):
		filters.bsc_indicator= frappe.parse_json(filters.get("bsc_indicator"))

	if filters.get('bsc_month'):
		filters.bsc_month= frappe.parse_json(filters.get("bsc_month"))
	columns = get_columns(filters)
	#chart = get_chart(filters)
	data = []
	ind_map = get_indicators(filters)
	total=0.0
	total_target=0.0
	labels = []
	datasets = []
	chart_values_target = []			
	chart_values_achieved= []


	for ind in sorted(ind_map):
		ind_det = ind_map.get(ind)
		if not ind_det:
			continue
		row = [ind_det.bsc_perspective, ind_det.bsc_objective, ind_det.bsc_indicator, ind_det.full_name, ind_det.department]
		months = filters.get("bsc_month")
		if months:
			#chart_values = []			
			#labels = months
			for d in months:
				#month_total=0.0
				if d=='Jan':
					total+=ind_det.jan_
					total_target+=ind_det.jan
					row.extend([cstr(flt(ind_det.jan_/ind_det.jan*100.0,2))+"%"] if ind_det.jan>0.0 else [""])
					month_total = flt(ind_det.jan_/ind_det.jan*100.0,2) if ind_det.jan>0.0 else 0.0
					month_target["jan"] += ind_det.jan if ind_det.jan>0.0 else 0.0
					month_achieved["jan"] += ind_det.jan_ if ind_det.jan_>0.0 else 0.0
				elif d=='Feb': 
					total+=ind_det.feb_
					total_target+=ind_det.feb
					row.extend([cstr(flt(ind_det.feb_/ind_det.feb*100.0,2))+"%"] if ind_det.feb>0.0 else [""])
					month_total = flt(ind_det.feb_/ind_det.feb*100.0,2) if ind_det.feb>0.0 else 0.0
					month_target["feb"] += ind_det.feb if ind_det.feb>0.0 else 0.0
					month_achieved["feb"] += ind_det.feb_ if ind_det.feb_>0.0 else 0.0
				elif d=='Mar': 
					total+=ind_det.mar_
					total_target+=ind_det.mar
					row.extend([cstr(flt(ind_det.mar_/ind_det.mar*100.0,2))+"%"] if ind_det.mar>0.0 else [""])
					month_total = flt(ind_det.mar_/ind_det.mar*100.0,2) if ind_det.mar>0.0 else 0.0
					month_target["mar"] += ind_det.mar if ind_det.mar>0.0 else 0.0
					month_achieved["mar"] += ind_det.mar_ if ind_det.mar_>0.0 else 0.0
				elif d=='Apr': 
					total+=ind_det.apr_
					total_target+=ind_det.apr
					row.extend([cstr(flt(ind_det.apr_/ind_det.apr*100.0,2))+"%"] if ind_det.apr>0.0 else [""])
					month_total = flt(ind_det.apr_/ind_det.apr*100.0,2) if ind_det.apr>0.0 else 0.0
					month_target["apr"] += ind_det.apr if ind_det.apr>0.0 else 0.0
					month_achieved["apr"] += ind_det.apr_ if ind_det.apr_>0.0 else 0.0
				elif d=='May': 
					total+=ind_det.may_
					total_target+=ind_det.may
					row.extend([cstr(flt(ind_det.may_/ind_det.may*100.0,2))+"%"] if ind_det.may>0.0 else [""])
					month_total = flt(ind_det.may_/ind_det.may*100.0,2) if ind_det.may>0.0 else 0.0
					month_target["may"] += ind_det.may if ind_det.may>0.0 else 0.0
					month_achieved["may"] += ind_det.may_ if ind_det.may_>0.0 else 0.0
				elif d=='Jun': 
					total+=ind_det.jun_
					total_target+=ind_det.jun
					row.extend([cstr(flt(ind_det.jun_/ind_det.jun*100.0,2))+"%"] if ind_det.jun>0.0 else [""])
					month_total = flt(ind_det.jun_/ind_det.jun*100.0,2) if ind_det.jun>0.0 else 0.0
					month_target["jun"] += ind_det.jun if ind_det.jun>0.0 else 0.0
					month_achieved["jun"] += ind_det.jun_ if ind_det.jun_>0.0 else 0.0
				elif d=='Jul': 
					total+=ind_det.jul_
					total_target+=ind_det.jul
					row.extend([cstr(flt(ind_det.jul_/ind_det.jul*100.0,2))+"%"] if ind_det.jul>0.0 else [""])
					month_total = flt(ind_det.jul_/ind_det.jul*100.0,2) if ind_det.jul>0.0 else 0.0
					month_target["jul"] += ind_det.jul if ind_det.jul>0.0 else 0.0
					month_achieved["jul"] += ind_det.jul_ if ind_det.jul_>0.0 else 0.0
				elif d=='Aug': 
					total+=ind_det.aug_
					total_target+=ind_det.aug
					row.extend([cstr(flt(ind_det.aug_/ind_det.aug*100.0,2))+"%"] if ind_det.aug>0.0 else [""])
					month_total = flt(ind_det.aug_/ind_det.aug*100.0,2)if ind_det.aug>0.0 else 0.0
					month_target["aug"] += ind_det.aug if ind_det.aug>0.0 else 0.0
					month_achieved["aug"] += ind_det.aug_ if ind_det.aug_>0.0 else 0.0
				elif d=='Sep': 
					total+=ind_det.sep_
					total_target+=ind_det.sep
					row.extend([cstr(flt(ind_det.sep_/ind_det.sep*100.0,2))+"%"] if ind_det.sep>0.0 else [""])
					month_total = flt(ind_det.sep_/ind_det.sep*100.0,2) if ind_det.sep>0.0 else 0.0
					month_target["sep"] += ind_det.sep if ind_det.sep>0.0 else 0.0
					month_achieved["sep"] += ind_det.sep_ if ind_det.sep_>0.0 else 0.0
				elif d=='Oct': 
					total+=ind_det.oct_
					total_target+=ind_det.oct
					row.extend([cstr(flt(ind_det.oct_/ind_det.oct*100.0,2))+"%"] if ind_det.oct>0.0 else [""])
					month_total = flt(ind_det.oct_/ind_det.oct*100.0,2) if ind_det.oct>0.0 else 0.0
					month_target["oct"] += ind_det.oct if ind_det.oct>0.0 else 0.0
					month_achieved["oct"] += ind_det.oct_ if ind_det.oct_>0.0 else 0.0
				elif d=='Nov': 
					total+=ind_det.nov_
					total_target+=ind_det.nov
					row.extend([cstr(flt(ind_det.nov_/ind_det.nov*100.0,2))+"%"] if ind_det.nov>0.0 else [""])
					month_total = flt(ind_det.nov_/ind_det.nov*100.0,2) if ind_det.nov>0.0 else 0.0
					month_target["nov"] += ind_det.nov if ind_det.nov>0.0 else 0.0
					month_achieved["nov"] += ind_det.nov_ if ind_det.nov_>0.0 else 0.0
				elif d=='Dec': 
					total+=ind_det.dec_
					total_target+=ind_det.dec
					row.extend([cstr(flt(ind_det.dec_/ind_det.dec*100.0,2))+"%"] if ind_det.dec>0.0 else [""])
					month_total = flt(ind_det.dec_/ind_det.dec*100.0,2) if ind_det.dec>0.0 else 0.0
					month_target["dec"] += ind_det.dec if ind_det.dec>0.0 else 0.0
					month_achieved["dec"] += ind_det.dec_ if ind_det.dec_>0.0 else 0.0
				#chart_values.append(month_total)
			#datasets.append({
			#	'name':ind_det.name,'values':chart_values
			#})
		else:
			total+=ind_det.jan_+ind_det.feb_+ind_det.mar_+ind_det.apr_+ind_det.may_+ind_det.jun_+ind_det.jul_+ind_det.aug_+ind_det.sep_+ind_det.oct_+ind_det.nov_+ind_det.dec_
			total_target+=ind_det.jan+ind_det.feb+ind_det.mar+ind_det.apr+ind_det.may+ind_det.jun+ind_det.jul+ind_det.aug+ind_det.sep+ind_det.oct+ind_det.nov+ind_det.dec
			row.extend([cstr(flt(ind_det.jan_/ind_det.jan*100.0,2))+"%"] if ind_det.jan>0.0 else [""])
			row.extend([cstr(flt(ind_det.feb_/ind_det.feb*100.0,2))+"%"] if ind_det.feb>0.0 else [""])
			row.extend([cstr(flt(ind_det.mar_/ind_det.mar*100.0,2))+"%"] if ind_det.mar>0.0 else [""])
			row.extend([cstr(flt(ind_det.apr_/ind_det.apr*100.0,2))+"%"] if ind_det.apr>0.0 else [""])
			row.extend([cstr(flt(ind_det.may_/ind_det.may*100.0,2))+"%"] if ind_det.may>0.0 else [""])
			row.extend([cstr(flt(ind_det.jun_/ind_det.jun*100.0,2))+"%"] if ind_det.jun>0.0 else [""])
			row.extend([cstr(flt(ind_det.jul_/ind_det.jul*100.0,2))+"%"] if ind_det.jul>0.0 else [""])
			row.extend([cstr(flt(ind_det.aug_/ind_det.aug*100.0,2))+"%"] if ind_det.aug>0.0 else [""])
			row.extend([cstr(flt(ind_det.sep_/ind_det.sep*100.0,2))+"%"] if ind_det.sep>0.0 else [""])
			row.extend([cstr(flt(ind_det.oct_/ind_det.oct*100.0,2))+"%"] if ind_det.oct>0.0 else [""])
			row.extend([cstr(flt(ind_det.nov_/ind_det.nov*100.0,2))+"%"] if ind_det.nov>0.0 else [""])
			row.extend([cstr(flt(ind_det.dec_/ind_det.dec*100.0,2))+"%"] if ind_det.dec>0.0 else [""])
		month_target["jan"] += ind_det.jan if ind_det.jan>0.0 else 0.0
		month_achieved["jan"] += ind_det.jan_ if ind_det.jan_>0.0 else 0.0
		month_target["feb"] += ind_det.feb if ind_det.feb>0.0 else 0.0
		month_achieved["feb"] += ind_det.feb_ if ind_det.feb_>0.0 else 0.0
		month_target["mar"] += ind_det.mar if ind_det.mar>0.0 else 0.0
		month_achieved["mar"] += ind_det.mar_ if ind_det.mar_>0.0 else 0.0
		month_target["apr"] += ind_det.apr if ind_det.apr>0.0 else 0.0
		month_achieved["apr"] += ind_det.apr_ if ind_det.apr_>0.0 else 0.0
		month_target["may"] += ind_det.may if ind_det.may>0.0 else 0.0
		month_achieved["may"] += ind_det.may_ if ind_det.may_>0.0 else 0.0
		month_target["jun"] += ind_det.jun if ind_det.jun>0.0 else 0.0
		month_achieved["jun"] += ind_det.jun_ if ind_det.jun_>0.0 else 0.0
		month_target["jul"] += ind_det.jul if ind_det.jul>0.0 else 0.0
		month_achieved["jul"] += ind_det.jul_ if ind_det.jul_>0.0 else 0.0
		month_target["aug"] += ind_det.aug if ind_det.aug>0.0 else 0.0
		month_achieved["aug"] += ind_det.aug_ if ind_det.aug_>0.0 else 0.0
		month_target["sep"] += ind_det.sep if ind_det.sep>0.0 else 0.0
		month_achieved["sep"] += ind_det.sep_ if ind_det.sep_>0.0 else 0.0
		month_target["oct"] += ind_det.oct if ind_det.oct>0.0 else 0.0
		month_achieved["oct"] += ind_det.oct_ if ind_det.oct_>0.0 else 0.0
		month_target["nov"] += ind_det.nov if ind_det.nov>0.0 else 0.0
		month_achieved["nov"] += ind_det.nov_ if ind_det.nov_>0.0 else 0.0
		month_target["dec"] += ind_det.jan if ind_det.dec>0.0 else 0.0
		month_achieved["dec"] += ind_det.jan_ if ind_det.dec_>0.0 else 0.0		

			#labels=["Jan","Feb","Mar","Apr","May","Jun","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
			#datasets.append({
			#	'name':ind_det.name,'values':[flt(ind_det.jan_/ind_det.jan*100.0,2) if ind_det.jan>0.0 else 0.0,
			#		flt(ind_det.feb_/ind_det.feb*100.0,2) if ind_det.feb>0.0 else 0.0,
			#		flt(ind_det.mar_/ind_det.mar*100.0,2) if ind_det.mar>0.0 else 0.0,
			#		flt(ind_det.apr_/ind_det.apr*100.0,2) if ind_det.apr>0.0 else 0.0,
			#		flt(ind_det.may_/ind_det.may*100.0,2) if ind_det.may>0.0 else 0.0,
			#		flt(ind_det.jun_/ind_det.jun*100.0,2) if ind_det.jun>0.0 else 0.0,
			#		flt(ind_det.jul_/ind_det.jul*100.0,2) if ind_det.jul>0.0 else 0.0,
			#		flt(ind_det.aug_/ind_det.aug*100.0,2) if ind_det.aug>0.0 else 0.0,
			#		flt(ind_det.sep_/ind_det.sep*100.0,2) if ind_det.sep>0.0 else 0.0,
			#		flt(ind_det.oct_/ind_det.oct*100.0,2) if ind_det.oct>0.0 else 0.0,
			#		flt(ind_det.nov_/ind_det.nov*100.0,2) if ind_det.nov>0.0 else 0.0,
			#		flt(ind_det.dec_/ind_det.dec*100.0,2) if ind_det.dec>0.0 else 0.0]
			#})

		
		row.extend([flt(total,2)])
		row.extend([flt(total_target,2)])
		if total==0:
			row.extend([0])
		else:
			row.extend([flt(total/ind_det.target*100.0,2)])
		row.extend([ind_det.fiscal_year])
		data.append(row)
	if months:
		chart_values_target = []			
		chart_values_achieved= []			
		labels = []
		for d in months:
			if d=='Jan':
				chart_values_target.append(month_target["jan"])
				chart_values_achieved.append(month_achieved["jan"])
				labels.append('Jan')
			elif d=='Feb':
				chart_values_target.append(month_target["feb"])
				chart_values_achieved.append(month_achieved["feb"])
				labels.append('Feb')
			elif d=='Mar':
				chart_values_target.append(month_target["mar"])
				chart_values_achieved.append(month_achieved["mar"])
				labels.append('Mar')
			elif d=='Apr':
				chart_values_target.append(month_target["apr"])
				chart_values_achieved.append(month_achieved["apr"])
				labels.append('Apr')
			elif d=='May':
				chart_values_target.append(month_target["may"])
				chart_values_achieved.append(month_achieved["may"])
				labels.append('May')
			elif d=='Jun':
				chart_values_target.append(month_target["jun"])
				chart_values_achieved.append(month_achieved["jun"])
				labels.append('Jun')
			elif d=='Jul':
				chart_values_target.append(month_target["jul"])
				chart_values_achieved.append(month_achieved["jul"])
				labels.append('Jul')
			elif d=='Aug':
				chart_values_target.append(month_target["aug"])
				chart_values_achieved.append(month_achieved["aug"])
				labels.append('Aug')
			elif d=='Sep':
				chart_values_target.append(month_target["sep"])
				chart_values_achieved.append(month_achieved["sep"])
				labels.append('Sep')
			elif d=='Oct':
				chart_values_target.append(month_target["oct"])
				chart_values_achieved.append(month_achieved["oct"])
				labels.append('Oct')
			elif d=='Nov':
				chart_values_target.append(month_target["nov"])
				chart_values_achieved.append(month_achieved["nov"])
				labels.append('Nov')
			elif d=='Dec':
				chart_values_target.append(month_target["dec"])
				chart_values_achieved.append(month_achieved["dec"])
				labels.append('Dec')
		datasets.append({
			'name':'Target','values':chart_values_target
		})
		datasets.append({
			'name':'Achieved','values':chart_values_target_achieved
		})

	else:
		labels=["Jan","Feb","Mar","Apr","May","Jun","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
		datasets.append({
			'name':'Target','values':[month_target["jan"],
				month_target["feb"],
				month_target["mar"],
				month_target["apr"],
				month_target["may"],
				month_target["jun"],
				month_target["jul"],
				month_target["aug"],
				month_target["sep"],
				month_target["oct"],
				month_target["nov"],
				month_target["dec"]]
		})
		datasets.append({
			'name':'Achieved','values':[month_achieved["jan"],
				month_achieved["feb"],
				month_achieved["mar"],
				month_achieved["apr"],
				month_achieved["may"],
				month_achieved["jun"],
				month_achieved["jul"],
				month_achieved["aug"],
				month_achieved["sep"],
				month_achieved["oct"],
				month_achieved["nov"],
				month_achieved["dec"]]
		})

    	chart = {
        	"data": {
            		'labels': labels,
            		'datasets': datasets
        	}
   	}

    	chart["type"] = "bar"
    	##chart["height"] = "140"
    	chart["colors"] = ['green','red']

	return columns, data, None, chart


def get_columns(filters):
	columns = [
		_("BSC Perspective") + ":Link/BSC Perspective:50",
		_("BSC Objective") + ":Link/BSC Objective:50",
		_("BSC Indicator") + ":Link/BSC Indicator:50",
		_("BSC Indicator Name") + ":Data:200",
		_("Department") + ":Link/Department:50"
	]
	months = filters.get("bsc_month")
	if months:
		for d in months:
			columns.append(cstr(d) +":Data:50")
	else:
		columns+=[_("Jan") + ":Data:50"]
		columns+=[_("Feb") + ":Data:50"]
		columns+=[_("Mar") + ":Data:50"]
		columns+=[_("Apr") + ":Data:50"]
		columns+=[_("May") + ":Data:50"]
		columns+=[_("Jun") + ":Data:50"]
		columns+=[_("Jul") + ":Data:50"]
		columns+=[_("Aug") + ":Data:50"]
		columns+=[_("Sep") + ":Data:50"]
		columns+=[_("Oct") + ":Data:50"]
		columns+=[_("Nov") + ":Data:50"]
		columns+=[_("Dec") + ":Data:50"]
	columns+=[_("Achieved") + ":Float:50", _("Targeted") + ":Float:50", _("Progress") + ":Percent:50", _("Year") + ":Link/Fiscal Year:40"]
	return columns


def get_conditions(filters):
	conditions = []
	conditions.append("ind.bsc_objective=obj.name")
	conditions.append("tar.docstatus=1")
	if filters.get("department"): conditions.append("tar.department in %(department)s")
	if filters.get("fiscal_year"): conditions.append("tar.fiscal_year = %(fiscal_year)s")
	if filters.get("bsc_indicator"): conditions.append("tar.bsc_indicator in %(bsc_indicator)s")
	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_indicators(filters):
	ind_map = frappe._dict()
	ind_list = frappe.db.sql("""SELECT tar.name, tar.uom, tar.target, tar.bsc_indicator, tar.department, tar.fiscal_year, ind.full_name, ind.bsc_objective, obj.bsc_perspective, \
		tar.jan, tar.feb, tar.mar, tar.apr, tar.may, tar.jun, tar.jul, tar.aug, tar.sep, tar.oct, tar.nov, tar.dec, \
		ifnull((select achieved from `tabBSC Target Log` where month='Jan' and bsc_target=tar.name and docstatus=1),0.0) as jan_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Feb' and bsc_target=tar.name and docstatus=1),0.0) as feb_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Mar' and bsc_target=tar.name and docstatus=1),0.0) as mar_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Apr' and bsc_target=tar.name and docstatus=1),0.0) as apr_, \
		ifnull((select achieved from `tabBSC Target Log` where month='May' and bsc_target=tar.name and docstatus=1),0.0) as may_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Jun' and bsc_target=tar.name and docstatus=1),0.0) as jun_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Jul' and bsc_target=tar.name and docstatus=1),0.0) as jul_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Aug' and bsc_target=tar.name and docstatus=1),0.0) as aug_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Sep' and bsc_target=tar.name and docstatus=1),0.0) as sep_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Oct' and bsc_target=tar.name and docstatus=1),0.0) as oct_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Nov' and bsc_target=tar.name and docstatus=1),0.0) as nov_, \
		ifnull((select achieved from `tabBSC Target Log` where month='Dec' and bsc_target=tar.name and docstatus=1),0.0) as dec_  \
		FROM `tabBSC Target` tar, `tabBSC Indicator` ind , `tabBSC Objective` obj \
		where tar.bsc_indicator=ind.name {conditions} \
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_dict=1)
	for ind in ind_list:
		if ind:
			ind_map.setdefault(ind.name, ind)

	return ind_map

def get_chart(filters):
	ind_map = frappe._dict()
	ind_list = frappe.db.sql("""SELECT sum(tar.jan), sum(tar.feb), sum(tar.mar), 
		sum(tar.apr), sum(tar.may), sum(tar.jun), sum(tar.jul), sum(tar.aug), sum(tar.sep), sum(tar.oct), sum(tar.nov), sum(tar.dec), \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Jan' and bsc_target=tar.name),0.0) as jan_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Feb' and bsc_target=tar.name),0.0) as feb_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Mar' and bsc_target=tar.name),0.0) as mar_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Apr' and bsc_target=tar.name),0.0) as apr_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='May' and bsc_target=tar.name),0.0) as may_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Jun' and bsc_target=tar.name),0.0) as jun_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Jul' and bsc_target=tar.name),0.0) as jul_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Aug' and bsc_target=tar.name),0.0) as aug_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Sep' and bsc_target=tar.name),0.0) as sep_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Oct' and bsc_target=tar.name),0.0) as oct_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Nov' and bsc_target=tar.name),0.0) as nov_, \
		ifnull((select sum(achieved) from `tabBSC Target Log` where month='Dec' and bsc_target=tar.name),0.0) as dec_  \
		FROM `tabBSC Target` tar, `tabBSC Indicator` ind , `tabBSC Objective` obj \
		where tar.bsc_indicator=ind.name {conditions} \
		""".format(
			conditions=get_conditions(filters),
		),
		filters, as_dict=1)
	labels = []
	datasets = []

	for ind in ind_list:
		if ind:
			months = filters.get("bsc_month")
			if months:
				chart_values_target = []			
				chart_values_achieved= []			
				labels = months

				for d in months:
					month_target=0.0
					month_achieved=0.0

					if d=='Jan':
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Feb': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Mar': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Apr': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='May': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Jun':
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Jul': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Aug': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Sep': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Oct': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Nov': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					elif d=='Dec': 
						month_target=flt(ind.jan,2) if ind.jan>0.0 else 0.0
						month_achieved=flt(ind.jan_,2) if ind.jan_>0.0 else 0.0
					chart_values_target.append(month_target)
					chart_values_achieved.append(month_achieved)
				datasets.append({
					'name':'Target','values':chart_values_target
				})
				datasets.append({
					'name':'Achieved','values':chart_values_achieved
				})


			else:
				labels=["Jan","Feb","Mar","Apr","May","Jun","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
				datasets.append({
					'name':'Target','values':[flt(ind.jan,2) if ind.jan>0.0 else 0.0,
						flt(ind.feb,2) if ind.feb>0.0 else 0.0,
						flt(ind.mar,2) if ind.mar>0.0 else 0.0,
						flt(ind.apr,2) if ind.apr>0.0 else 0.0,
						flt(ind.may,2) if ind.may>0.0 else 0.0,
						flt(ind.jun,2) if ind.jun>0.0 else 0.0,
						flt(ind.jul,2) if ind.jul>0.0 else 0.0,
						flt(ind.aug,2) if ind.aug>0.0 else 0.0,
						flt(ind.sep,2) if ind.sep>0.0 else 0.0,
						flt(ind.oct,2) if ind.oct>0.0 else 0.0,
						flt(ind.nov,2) if ind.nov>0.0 else 0.0,
						flt(ind.dec,2) if ind.dec>0.0 else 0.0,]
				})
				datasets.append({
					'name':'Achieved','values':[flt(ind.jan_,2) if ind.jan_>0.0 else 0.0,
						flt(ind.feb_,2) if ind.feb_>0.0 else 0.0,
						flt(ind.mar_,2) if ind.mar_>0.0 else 0.0,
						flt(ind.apr_,2) if ind.apr_>0.0 else 0.0,
						flt(ind.may_,2) if ind.may_>0.0 else 0.0,
						flt(ind.jun_,2) if ind.jun_>0.0 else 0.0,
						flt(ind.jul_,2) if ind.jul_>0.0 else 0.0,
						flt(ind.aug_,2) if ind.aug_>0.0 else 0.0,
						flt(ind.sep_,2) if ind.sep_>0.0 else 0.0,
						flt(ind.oct_,2) if ind.oct_>0.0 else 0.0,
						flt(ind.nov_,2) if ind.nov_>0.0 else 0.0,
						flt(ind.dec_,2) if ind.dec_>0.0 else 0.0,]
				})


			ind_map.setdefault(ind.name, ind)
    	chart = {
        	"data": {
            		'labels': labels,
            		'datasets': datasets
        	}
   	}
    	chart["type"] = "bar"


	return chart