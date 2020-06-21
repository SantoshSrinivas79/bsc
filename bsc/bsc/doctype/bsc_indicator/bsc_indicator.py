# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.utils import (flt, cstr)
from frappe.model.document import Document
from collections import defaultdict

class BSCIndicator(Document):
	def validate(self):
		self.validate_percentage()

	def validate_percentage(self):
		#if flt(self.indicator_percentage) <= 0.0 :
		#	frappe.throw(_("The percentage % must to be > {0}").format(frappe.bold("0.0")))
		bsc_settings = frappe.db.get_single_value('BSC Settings', 'allow_more_ind')
		if bsc_settings:
			if bsc_settings == 0:
				bsc_settings == 0
			else:
				bsc_settings == 1
		else:
			bsc_settings == 1

		if not frappe.db.exists(self.doctype, self.name):
			sum_percentage = frappe.db.sql("""select sum(indicator_percentage) from `tabBSC Indicator` where bsc_objective = %s""",self.bsc_objective)[0][0]
			if sum_percentage == 100:
				if bsc_settings == 0:
					frappe.throw(_("You can't add this indicator, the total percentage % of others is 100%"))
				else:
					frappe.msgprint(_("You can't add this indicator, the total percentage % of others is 100%"))
		else :
			sum_percentage = frappe.db.sql("""select sum(indicator_percentage) from `tabBSC Indicator` where bsc_objective = %s and name <> %s""",(self.bsc_objective, self.name))[0][0]

			if (flt(flt(sum_percentage) + self.indicator_percentage)) > 100.0 :
				if bsc_settings == 0:
					frappe.throw(_("The percentage % must to be < {0}, total of others is {1}").format(frappe.bold(str(100 - flt(sum_percentage))), \
						frappe.bold(str(flt(sum_percentage))) ))
				else:
					frappe.msgprint(_("The percentage % must to be < {0}, total of others is {1}").format(frappe.bold(str(100 - flt(sum_percentage))), \
						frappe.bold(str(flt(sum_percentage))) ))

	def create_targets_and_initiatives_assignments(self):
		
		self.check_permission('write')
		dep_list = [d.department for d in get_departments_by_indicator(self.name)]
		if dep_list:
			args = frappe._dict({
				"fiscal_year": frappe.defaults.get_user_default("fiscal_year"),
				"bsc_indicator": self.name,
				"indicator_name": self.full_name,
				"uom": 'Numerical',
			})
			create_targets_for_departments(dep_list, args, publish_progress=True)
			args = frappe._dict({
				"fiscal_year": frappe.defaults.get_user_default("fiscal_year"),
				"bsc_indicator": self.name,
				"indicator_name": self.full_name,
			})
			create_initiatives_assignments_for_departments(dep_list, args, publish_progress=True)
		# since this method is called via frm.call this doc needs to be updated manually
		self.reload()

	def create_indicator_assignments(self):
		
		self.check_permission('write')
		dep_list = [d.department for d in get_departments_by_indicator(self.name)]
		if dep_list:
			args = frappe._dict({
				"fiscal_year": frappe.defaults.get_user_default("fiscal_year"),
				"bsc_indicator": self.name,
				"indicator_name": self.full_name,
			})
			create_indicator_assignments_for_departments(dep_list, args, publish_progress=True)
		# since this method is called via frm.call this doc needs to be updated manually
		self.reload()


def create_targets_for_departments(dep_list, args, publish_progress=True):
	targets_exists_for = get_existing_targets(dep_list,args)
	count=0
	for dep in dep_list:
		if dep not in targets_exists_for:
			args.update({
				"doctype": "BSC Target",
				"department": dep
			})
			ss = frappe.get_doc(args)
			ss.insert()
			count+=1
			if publish_progress:
				frappe.publish_progress(count*100/len(set(dep_list) - set(targets_exists_for)),
					title = _("Creating BSC Target for {0} Department...").format(dep))

	bsc_indicator= frappe.get_doc("BSC Indicator", args.bsc_indicator)
	bsc_indicator.db_set("create_count", bsc_indicator.create_count+1)
	bsc_indicator.notify_update()

def create_initiatives_assignments_for_departments(dep_list, args, publish_progress=True):
	initiatives_assignments_exists_for = get_existing_initiatives_assignments(dep_list,args)
	count=0
	for dep in dep_list:
		if dep not in initiatives_assignments_exists_for:
			args.update({
				"doctype": "BSC Initiative Assignment",
				"department": dep
			})
			ss = frappe.get_doc(args)
			ss.insert()
			count+=1
			if publish_progress:
				frappe.publish_progress(count*100/len(set(dep_list) - set(initiatives_assignments_exists_for)),
					title = _("Creating BSC Initiatives Assignments for {0} Department...").format(dep))

	bsc_indicator= frappe.get_doc("BSC Indicator", args.bsc_indicator)
	bsc_indicator.db_set("create_count", bsc_indicator.create_count+1)
	bsc_indicator.notify_update()

def create_indicator_assignments_for_departments(dep_list, args, publish_progress=True):
	indicator_assignments_exists_for = get_existing_indicator_assignments(dep_list,args)
	count=0
	for dep in dep_list:
		if dep not in indicator_assignments_exists_for:
			args.update({
				"doctype": "BSC Indicator Assignment",
				"department": dep
			})
			ss = frappe.get_doc(args)
			ss.insert()
			count+=1
			if publish_progress:
				frappe.publish_progress(count*100/len(set(dep_list) - set(indicator_assignments_exists_for)),
					title = _("Creating BSC Indicator Assignments for {0} Department...").format(dep))

	bsc_indicator= frappe.get_doc("BSC Indicator", args.bsc_indicator)
	bsc_indicator.db_set("create_count", bsc_indicator.create_count+1)
	bsc_indicator.notify_update()


def get_existing_targets(dep_list, args):
	return frappe.db.sql_list("""
		select distinct department from `tabBSC Target`
		where docstatus!= 2 and bsc_indicator=%s and fiscal_year=%s and department in (%s)
	""" % ('%s', '%s', ', '.join(['%s']*len(dep_list))),
		[args.bsc_indicator, args.fiscal_year] + dep_list)

def get_existing_initiatives_assignments(dep_list, args):
	return frappe.db.sql_list("""
		select distinct department from `tabBSC Initiative Assignment`
		where docstatus!= 2 and bsc_indicator=%s and fiscal_year=%s and department in (%s)
	""" % ('%s', '%s', ', '.join(['%s']*len(dep_list))),
		[args.bsc_indicator, args.fiscal_year] + dep_list)

def get_existing_indicator_assignments(dep_list, args):
	return frappe.db.sql_list("""
		select distinct department from `tabBSC Indicator Assignment`
		where docstatus!= 2 and bsc_indicator=%s and fiscal_year=%s and department in (%s)
	""" % ('%s', '%s', ', '.join(['%s']*len(dep_list))),
		[args.bsc_indicator, args.fiscal_year] + dep_list)


def get_departments_by_indicator(indicator):
	departments = []
	departments = frappe.db.sql("""select dep.department as department from `tabBSC Indicator Department` dep where
		dep.parent = %s and dep.parentfield = 'departments' """,indicator, as_dict=True)
	
	return departments

@frappe.whitelist()
def get_indicator_by_department(doctype, txt, searchfield, start, page_len, filters):

	if not filters.get("department"):
		frappe.throw(_("Please select Department Record first."))

	indicators = []
	indicators = frappe.db.sql("""select ind.name, ind.full_name, ind.bsc_objective from
		`tabBSC Indicator Department` dep, `tabBSC Indicator` ind where
		dep.parent = ind.name
		and dep.department = %s""",filters.get("department"), as_list=True)

	return indicators 

@frappe.whitelist()
def get_month_by_indicator(department,bsc_indicator,doctype,bsc_initiative):
			
	if not department:
		frappe.throw(_("Please select Department Record first."))
	if not bsc_indicator:
		frappe.throw(_("Please select Indicator Record first."))
	months = []
	if doctype == "BSC Initiative Log":
		parentfield = "initiative_months"
		if not bsc_initiative:
			frappe.throw(_("Please select Initiative Record first."))
		months = frappe.db.sql("""select mon.month from `tabBSC Target Month` mon where mon.target>0 and mon.parentfield = %s and mon.parent = \
			%s""",(parentfield,bsc_initiative), as_list=True)
	else:
		parentfield = "target_months"	
		months = frappe.db.sql("""select mon.month from `tabBSC Target Month` mon where mon.target>0 and mon.parentfield = %s and mon.parent = \
			(select tar.name from `tabBSC Target` tar where tar.department = %s and \
			tar.bsc_indicator = %s)""",(parentfield,department,bsc_indicator), as_list=True)
	if not months:
		frappe.throw(_("No Months."))
	months_sorted = [['Jan'], ['Feb'], ['Mar'], ['Apr'], ['May'], ['Jun'], ['Jul'], ['Aug'], ['Sep'], ['Oct'], ['Nov'],['Dec']]
	#frappe.throw(_("months {0} ,months_sorted {1}").format(months,months_sorted))

	sortedd=sorted(months, key=lambda x: months_sorted.index(x))	
	return sortedd
