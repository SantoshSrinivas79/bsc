# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.model.document import Document

class BSCInitiative(Document):
	def validate(self):
		self.validate_desc()
		self.validate_duplicate()
		self.validate_month_count()

	def validate_desc(self):
		if not self.description:
			self.description=self.initiative_name

	def validate_duplicate(self):
		conditions = ""
		conditions += " where docstatus < 2 and department = '%s'" % self.department
		conditions += " and bsc_indicator = '%s'" % self.bsc_indicator
		conditions += " and initiative_name = '%s'" % self.initiative_name
		sum_name = frappe.db.sql("""select count(name) from `tabBSC Initiative` %s"""% conditions)[0][0]
		if sum_name > 1:
			frappe.throw(_("Already exists with same Department and Indicator"))

	def on_submit(self):
		self.create_initiative_log()

	def validate_month_count(self):
		self.month_count=0
		if self.jan>0: self.month_count+=1
		if self.feb>0: self.month_count+=1
		if self.mar>0: self.month_count+=1
		if self.apr>0: self.month_count+=1
		if self.may>0: self.month_count+=1
		if self.jun>0: self.month_count+=1
		if self.jul>0: self.month_count+=1
		if self.aug>0: self.month_count+=1
		if self.sep>0: self.month_count+=1
		if self.oct>0: self.month_count+=1
		if self.nov>0: self.month_count+=1
		if self.dec>0: self.month_count+=1		

	def create_initiative_log(self):
		self.check_permission('write')
		args = frappe._dict({
			"department": self.department,
			"bsc_indicator": self.bsc_indicator,
			"bsc_initiative": self.name,
			"initiative_name": self.initiative_name,
			"is_achieved": 'No',
		})
		# since this method is called via frm.call this doc needs to be updated manually
		if self.jan>0: create_initiative_log("Jan", self.jan, args, publish_progress=True)
		if self.feb>0: create_initiative_log("Feb", self.feb, args, publish_progress=True)
		if self.mar>0: create_initiative_log("Mar", self.mar, args, publish_progress=True)
		if self.apr>0: create_initiative_log("Apr", self.apr, args, publish_progress=True)
		if self.may>0: create_initiative_log("May", self.may, args, publish_progress=True)
		if self.jun>0: create_initiative_log("Jun", self.jun, args, publish_progress=True)
		if self.jul>0: create_initiative_log("Jul", self.jul, args, publish_progress=True)
		if self.aug>0: create_initiative_log("Aug", self.aug, args, publish_progress=True)
		if self.sep>0: create_initiative_log("Sep", self.sep, args, publish_progress=True)
		if self.oct>0: create_initiative_log("Oct", self.oct, args, publish_progress=True)
		if self.nov>0: create_initiative_log("Nov", self.nov, args, publish_progress=True)
		if self.dec>0: create_initiative_log("Dec", self.dec, args, publish_progress=True)		
		self.reload()


def create_initiative_log(month , target, args, publish_progress=True):
	if frappe.db.sql("""select count(name) from `tabBSC Initiative Log` where docstatus < 2  
		and month = %s and bsc_initiative = %s""", (month,args.bsc_initiative))[0][0]==0:		
		args.update({
			"doctype": "BSC Initiative Log",
			"month": month,
			"target": target
		})
		ss = frappe.get_doc(args)
		ss.insert()
		if publish_progress:
			frappe.publish_progress(100,title = _("Creating BSC Initiative Log for {0}...").format(month))
	bsc_initiative= frappe.get_doc("BSC Initiative", args.bsc_initiative)
	bsc_initiative.db_set("initiative_logs_created", 1)
	bsc_initiative.notify_update()

@frappe.whitelist()
def get_graph_data(title, test):
    	chart = {
        	'data': {
			'labels': ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
			'datasets': [
				{ 'name': "Dataset 1", 'values': [18, 40, 30, 35, 8, 52, 17, -4] },
				{ 'name': "Dataset 2", 'values': [30, 50, -10, 15, 18, 32, 27, 14] }
			]
		}
   	}
	return chart