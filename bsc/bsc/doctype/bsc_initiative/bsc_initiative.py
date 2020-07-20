# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.utils import flt, cint
from frappe.model.document import Document

class BSCInitiative(Document):
	def validate(self):
		self.validate_desc()
		self.validate_duplicate()
		self.validate_month_count()
		self.validate_target()

	def validate_desc(self):
		if not self.description:
			self.description=self.initiative_name

	def validate_duplicate(self):
		conditions = " where docstatus < 2 and department = '%s'" % self.department
		conditions += " and fiscal_year = '%s'" % self.fiscal_year
		conditions += " and bsc_target = '%s'" % self.bsc_target
		conditions += " and initiative_name = '%s'" % self.initiative_name
		if frappe.db.exists(self.doctype, self.name):
			conditions += " and name <> '%s'" % self.name
		sum_name = frappe.db.sql("""select count(name) from `tabBSC Initiative` %s"""% conditions)[0][0]
		if sum_name > 0:
			frappe.throw(_("Already exists with same Department and Indicator and Initiative Name"))

	def validate_target(self):
		conditions = " where bsc_target = '%s'" % self.bsc_target
		target_total = frappe.db.sql("""select IFNULL(sum(entry_number),0) from `tabBSC Ledger Entry` %s"""% conditions)[0][0]
		bsc_target_master=frappe.get_doc("BSC Target", self.bsc_target)
		if bsc_target_master.target-target_total < 0:
			allow = frappe.db.get_single_value('BSC Settings', 'allow_initiative_more_than_target')
			if allow==1:
				frappe.msgprint(_("Targets of the Indicator is {0}, other Initiatives have {1}, currenct Initiative Target can to be {2} or less".format(bsc_target_master.target,target_total,bsc_target_master.target-target_total)))
			else:
				frappe.throw(_("Targets of the Indicator is {0}, other Initiatives have {1}, currenct Initiative Target can to be only {2} or less".format(bsc_target_master.target,target_total,bsc_target_master.target-target_total)))


	def on_submit(self):
		self.create_logs()

	def validate_month_count(self):
		self.month_count=0
		'''if (self.jan>0 and self.jan_target<=0) or (self.jan<=0 and self.jan_target>0):
			frappe.throw(_("Jan Wrong"))
		if (self.feb>0 and self.feb_target<=0) or (self.feb<=0 and self.feb_target>0):
			frappe.throw(_("Feb Wrong"))
		if not self.jan: self.jan=0
		if not self.feb: self.feb=0
		if not self.mar: self.mar=0
		if not self.apr: self.apr=0
		if not self.may: self.may=0
		if not self.jun: self.jun=0
		if not self.jul: self.jul=0
		if not self.aug: self.aug=0
		if not self.sep: self.sep=0
		if not self.oct: self.oct=0
		if not self.nov: self.nov=0
		if not self.dec: self.dec=0'''

		if cint(self.jan)>0: self.month_count+=1
		if cint(self.feb)>0: self.month_count+=1
		if cint(self.mar)>0: self.month_count+=1
		if cint(self.apr)>0: self.month_count+=1
		if cint(self.may)>0: self.month_count+=1
		if cint(self.jun)>0: self.month_count+=1
		if cint(self.jul)>0: self.month_count+=1
		if cint(self.aug)>0: self.month_count+=1
		if cint(self.sep)>0: self.month_count+=1
		if cint(self.oct)>0: self.month_count+=1
		if cint(self.nov)>0: self.month_count+=1
		if cint(self.dec)>0: self.month_count+=1

		self.initiative_count=self.jan+self.feb+self.mar+self.apr+self.may+self.jun+self.jul+self.aug+self.sep+self.oct+self.nov+self.dec
		self.initiative_target=self.jan_target+self.feb_target+self.mar_target+self.apr_target+self.may_target+self.jun_target+self.jul_target+self.aug_target+self.sep_target+self.oct_target+self.nov_target+self.dec_target

	def create_logs(self):
		self.check_permission('write')
		bsc_target_master=frappe.get_doc("BSC Target", self.bsc_target)
		args = frappe._dict({
			"bsc_indicator": bsc_target_master.bsc_indicator,
			"bsc_initiative": self.name,
			"bsc_target": self.bsc_target,
			"department": self.department,
			"fiscal_year": self.fiscal_year,
			"employee": self.employee,
		})
		# since this method is called via frm.call this doc needs to be updated manually
		if self.jan>0 and self.jan_target>0.0:
			create_log(self.jan, self.jan_target, "Jan", args, publish_progress=True)
		if self.feb>0 and self.feb_target>0.0:
			create_log(self.feb, self.feb_target, "Feb", args, publish_progress=True)
		if self.mar>0 and self.mar_target>0.0:
			create_log(self.mar, self.mar_target, "Mar", args, publish_progress=True)
		if self.apr>0 and self.apr_target>0.0:
			create_log(self.apr, self.apr_target, "Apr", args, publish_progress=True)
		if self.may>0 and self.may_target>0.0:
			create_log(self.may, self.may_target, "May", args, publish_progress=True)
		if self.jun>0 and self.jun_target>0.0:
			create_log(self.jun, self.jun_target, "Jun", args, publish_progress=True)
		if self.jul>0 and self.jul_target>0.0:
			create_log(self.jul, self.jul_target, "Jul", args, publish_progress=True)
		if self.aug>0 and self.aug_target>0.0:
			create_log(self.aug, self.aug_target, "Aug", args, publish_progress=True)
		if self.sep>0 and self.sep_target>0.0:
			create_log(self.sep, self.sep_target, "Sep", args, publish_progress=True)
		if self.oct>0 and self.oct_target>0.0:
			create_log(self.oct, self.oct_target, "Oct", args, publish_progress=True)
		if self.nov>0 and self.nov_target>0.0:
			create_log(self.nov, self.nov_target, "Nov", args, publish_progress=True)
		if self.dec>0 and self.dec_target>0.0:
			create_log(self.dec, self.dec_target, "Dec", args, publish_progress=True)
		self.reload()

	def on_cancel(self):
		frappe.db.sql("""delete from `tabBSC Ledger Entry`
			where party_type= 'BSC Initiative' and party_name = %s """, self.name)
		frappe.db.sql("""delete from `tabBSC Ledger Entry`
			where party_type= 'BSC Target' and party_name = %s """, self.bsc_target)

def create_log(initiative_count, initiative_target, month, args, publish_progress=True):
	if frappe.db.sql("""select count(name) from `tabBSC Initiative Log` where docstatus < 2  
	and month = %s and bsc_initiative = %s""", (month,args.bsc_initiative))[0][0]==0:		
		log_args = frappe._dict({
			"doctype": "BSC Initiative Log",
			"bsc_initiative": args.bsc_initiative,
			"bsc_target": args.bsc_target,
			"department": args.department,
			"fiscal_year": args.fiscal_year,
			"month": month,
			"log_target": initiative_target,
			"log_count": initiative_count,
			"employee": args.employee,
		})
		il = frappe.get_doc(log_args)
		il.insert()

	# create the BSC Ledger Entry#
	ble = frappe.get_doc(frappe._dict({
		"bsc_indicator": args.bsc_indicator,
		"bsc_target": args.bsc_target,
		"bsc_initiative": args.bsc_initiative,
		"entry_type": "Targeted",
		"month": month,
		"entry_number": initiative_target,
		"entry_count": initiative_count,
		"department": args.department,
		"fiscal_year": args.fiscal_year,
		"doctype": "BSC Ledger Entry"
	}))
	ble.insert()
	#

	if publish_progress:
		frappe.publish_progress(100,title = _("Creating BSC Initiative Log for {0}...").format(month))
	bsc_initiative= frappe.get_doc("BSC Initiative", args.bsc_initiative)
	bsc_initiative.db_set("initiative_logs_created", 1)
	bsc_initiative.notify_update()