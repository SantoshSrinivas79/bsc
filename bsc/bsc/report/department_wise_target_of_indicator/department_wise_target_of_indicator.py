# Copyright (c) 2013, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import (flt)
from frappe import _, throw

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()
	data = []
	ind_map = get_indicators(filters)
	for ind in sorted(ind_map):
		ind_det = ind_map.get(ind)
		if not ind_det:
			continue
		row = [ind_det.bsc_perspective, ind_det.bsc_objective, ind_det.bsc_indicator, ind_det.full_name]
		ach_map = get_achieved(ind_det.name)
		jan=0
		feb=0
		mar=0
		apr=0
		may=0
		jun=0
		jul=0
		aug=0
		sep=0
		oct=0
		nov=0
		dec=0
		for ach in sorted(ach_map):
			ach_det = ach_map.get(ach)
			if not ach_det:
				continue
		        if ach_det.month == "Jan": jan=flt(ach_det.achieved)
			elif ach_det.month == "Feb": feb=flt(ach_det.achieved)
			elif ach_det.month == "Mar": mar=ach_det.achieved
			elif ach_det.month == "Apr": apr=ach_det.achieved
			elif ach_det.month == "May": may=ach_det.achieved
			elif ach_det.month == "Jun": jun=ach_det.achieved
			elif ach_det.month == "Jul": jul=ach_det.achieved
			elif ach_det.month == "Aug": aug=ach_det.achieved
			elif ach_det.month == "Sep": sep=ach_det.achieved
			elif ach_det.month == "Oct": oct=ach_det.achieved
			elif ach_det.month == "Nov": nov=ach_det.achieved
			elif ach_det.month == "Dec": dec=ach_det.achieved
		total=get_if_not(jan)+get_if_not(feb)+get_if_not(mar)+get_if_not(apr)+get_if_not(may)+get_if_not(jun)+get_if_not(jul)+get_if_not(aug)+get_if_not(sep)+get_if_not(oct)+get_if_not(nov)+get_if_not(dec)
		row.extend([total])
		row.extend([ind_det.target_total])
		if total==0:
			row.extend([0])
		else:
			row.extend([flt(ind_det.target/total)])
		row.extend([jan])
		row.extend([feb])
		row.extend([mar])
		row.extend([apr])
		row.extend([may])
		row.extend([jun])
		row.extend([jul])
		row.extend([aug])
		row.extend([sep])
		row.extend([oct])
		row.extend([nov])
		row.extend([dec])
		row.extend([ind_det.fiscal_year])
		data.append(row)
	return columns, data


def get_columns():
	return [
		_("BSC Perspective") + ":Link/BSC Perspective:50",
		_("BSC Objective") + ":Link/BSC Objective:50",
		_("BSC Indicator") + ":Link/BSC Indicator:50",
		_("BSC Indicator Name") + ":Data:200",
		_("Achieved") + ":Float:50",
		_("Targeted") + ":Float:50",
		_("Progress") + ":Percent:50",
		_("Jan") + ":Float:40",
		_("Feb") + ":Float:40",
		_("Mar") + ":Float:40",
		_("Apr") + ":Float:40",
		_("May") + ":Float:40",
		_("Jun") + ":Float:40",
		_("Jul") + ":Float:40",
		_("Aug") + ":Float:40",
		_("Sep") + ":Float:40",
		_("Oct") + ":Float:40",
		_("Nov") + ":Float:40",
		_("Dec") + ":Float:40",
		_("Year") + ":Link/Fiscal Year:20"
	]


def get_conditions(filters):
	conditions = ""
	if filters.get("department"): conditions += " and tar.department = '%s'" % \
		filters["department"]
	if filters.get("fiscal_year"): conditions += " and tar.fiscal_year = '%s'" % \
		filters["fiscal_year"]
	if filters.get("bsc_indicator"): conditions += "  and tar.bsc_indicator= '%s'" % \
		filters["bsc_indicator"].replace("'", "\\'")
	return conditions

def get_indicators(filters):
	conditions = get_conditions(filters)
	ind_map = frappe._dict()
	ind_list = frappe.db.sql("""SELECT tar.name, tar.uom, tar.target, tar.bsc_indicator, tar.fiscal_year, ind.full_name, ind.bsc_objective, obj.bsc_perspective \
		FROM `tabBSC Target` tar, `tabBSC Indicator` ind , `tabBSC Objective` obj \
		where tar.bsc_indicator=ind.name and ind.bsc_objective=obj.name %s""" % conditions, as_dict=1)
	for ind in ind_list:
		if ind:
			ind_map.setdefault(ind.name, ind)
	return ind_map

def get_targeted(bsc_target):
	tar_map = frappe._dict()
	tar_list = frappe.db.sql("""SELECT month, target
		FROM `tabBSC Target Month`
		where parent= %s""",bsc_target, as_dict=1)
	for tar in tar_list:
		if tar :
			tar_map.setdefault(tar.name, tar)
	return tar_map

def get_achieved(bsc_target):
	tar_map = frappe._dict()
	tar_list = frappe.db.sql("""SELECT name, month, achieved
		FROM `tabBSC Target Log`
		where bsc_target= %s""",bsc_target, as_dict=1)
	for tar in tar_list:
		if tar :
			tar_map.setdefault(tar.name, tar)
	return tar_map

def get_if_not(mon):
	if not mon:
		return flt(0)
	else:
		return mon