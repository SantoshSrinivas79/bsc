# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.model.document import Document

class BSCTarget(Document):

	def validate(self):
		self.validate_duplicate()

	def validate_duplicate(self):
		conditions = ""
		conditions += " where docstatus < 2 and department = '%s'" % self.department
		conditions += " and bsc_indicator = '%s'" % self.bsc_indicator
		if frappe.db.exists(self.doctype, self.name):
			conditions += " and name <> '%s'" % self.name
		sum_name = frappe.db.sql("""select count(name) from `tabBSC Target` %s"""% conditions)[0][0]
		if sum_name > 0:
			frappe.throw(_("Already exists with same Department and Indicator"))

	def on_submit(self):
		self.create_target_log()

	def create_target_log(self):
		self.check_permission('write')
		args = frappe._dict({
			"department": self.department,
			"bsc_indicator": self.bsc_indicator,
			"bsc_target": self.name
		})
		# since this method is called via frm.call this doc needs to be updated manually
		if self.jan>0: create_target_log("Jan", self.jan, args, publish_progress=True)
		if self.feb>0: create_target_log("Feb", self.feb, args, publish_progress=True)
		if self.mar>0: create_target_log("Mar", self.mar, args, publish_progress=True)
		if self.apr>0: create_target_log("Apr", self.apr, args, publish_progress=True)
		if self.may>0: create_target_log("May", self.may, args, publish_progress=True)
		if self.jun>0: create_target_log("Jun", self.jun, args, publish_progress=True)
		if self.jul>0: create_target_log("Jul", self.jul, args, publish_progress=True)
		if self.aug>0: create_target_log("Aug", self.aug, args, publish_progress=True)
		if self.sep>0: create_target_log("Sep", self.sep, args, publish_progress=True)
		if self.oct>0: create_target_log("Oct", self.oct, args, publish_progress=True)
		if self.nov>0: create_target_log("Nov", self.nov, args, publish_progress=True)
		if self.dec>0: create_target_log("Dec", self.dec, args, publish_progress=True)		
		self.reload()


def create_target_log(month , target, args, publish_progress=True):
	if frappe.db.sql("""select count(name) from `tabBSC Target Log` where  
		bsc_target = %s and month = %s""", (args.bsc_target,month))[0][0]==0:		
		args.update({
			"doctype": "BSC Target Log",
			"month": month,
			"achieved": 0.0,
			"target": target
		})
		ss = frappe.get_doc(args)
		ss.insert()
		if publish_progress:
			frappe.publish_progress(100,title = _("Creating BSC Target Log for {0}...").format(month))

	bsc_target = frappe.get_doc("BSC Target", args.bsc_target)
	bsc_target.db_set("target_logs_created", 1)
	bsc_target.notify_update()