# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.model.document import Document
from frappe.utils import (flt, getdate, get_last_day)

class BSCInitiativeLog(Document):

	def validate(self):
		self.validate_duplicate()
		self.validate_dates()
		self.validate_month()
		self.validate_mandatories()

	def validate_month(self):
		if self.log_target==0:
			res = frappe.db.sql("""SELECT count(entry_number) FROM `tabBSC Ledger Entry` 
				WHERE party_type='BSC Initiative' and entry_type='Targeted' and party_name = %s and month = %s""", (self.bsc_initiative,self.month))
			if res[0][0]==0:
				allow_create= frappe.db.get_single_value('BSC Settings', 'allow_without_target')
				if allow_create==1:
					self.target_progress=0
					frappe.msgprint(_("There is no Target for current month {0}".format(self.month)))
				else:
					frappe.throw(_("There is no Target for current month {0}".format(self.month)))
		else:
			self.target_progress=flt(self.target_achieved)/flt(self.log_target)*100


	def validate_mandatories(self):
		if self.is_achieved=='No':
			if not self.weakness_reasons:
				frappe.msgprint(_("There is no Weakness Reasons"))
			if not self.suggested_solutions:
				frappe.msgprint(_("There is no Suggested Solutions"))
		if self.is_achieved=='Yes':
			if not self.evidence_attachment:
				frappe.msgprint(_("There is no Evidence Attachment"))

	def validate_duplicate(self):
		conditions = ""
		conditions += " where docstatus < 2 "
		conditions += " and bsc_initiative = '%s'" % self.bsc_initiative 
		conditions += " and month = '%s'" % self.month
		if frappe.db.exists(self.doctype, self.name):
			conditions += " and name <> '%s'" % self.name
		sum_name = frappe.db.sql("""select count(name) from `tabBSC Initiative Log` %s"""% conditions)[0][0]
		if sum_name > 0:
			frappe.throw(_("Already exists with same Department, Indicator, and Month"))

	def validate_dates(self):
		if self.month and self.fiscal_year and (not self.start_date or not self.last_date):
			if self.month == 'Jan':
				self.start_date=getdate(self.fiscal_year+'-01-01')
			if self.month == 'Feb':
				self.start_date=getdate(self.fiscal_year+'-02-01')
			if self.month == 'Mar':
				self.start_date=getdate(self.fiscal_year+'-03-01')
			if self.month == 'Apr':
				self.start_date=getdate(self.fiscal_year+'-04-01')
			if self.month == 'May':
				self.start_date=getdate(self.fiscal_year+'-05-01')
			if self.month == 'Jun':
				self.start_date=getdate(self.fiscal_year+'-06-01')
			if self.month == 'Jul':
				self.start_date=getdate(self.fiscal_year+'-07-01')
			if self.month == 'Aug':
				self.start_date=getdate(self.fiscal_year+'-08-01')
			if self.month == 'Sep':
				self.start_date=getdate(self.fiscal_year+'-09-01')
			if self.month == 'Oct':
				self.start_date=getdate(self.fiscal_year+'-10-01')
			if self.month == 'Nov':
				self.start_date=getdate(self.fiscal_year+'-11-01')
			if self.month == 'Dec':
				self.start_date=getdate(self.fiscal_year+'-12-01')
			self.last_date=get_last_day(self.start_date)

	def on_submit(self):
		bsc_target_master=frappe.get_doc("BSC Target", self.bsc_target)
		self.update_master(True)
		# create the BSC Ledger Entry #
		ble = frappe.get_doc(frappe._dict({
			"bsc_indicator" : bsc_target_master.bsc_indicator,
			"bsc_target": self.bsc_target,
			"bsc_initiative": self.bsc_initiative,
			"bsc_initiative_log": self.name,
			"entry_type": "Achieved",
			"entry_number": self.target_achieved,
			"entry_count": self.log_count if self.is_achieved=='Yes' else 0,
			"department": self.department,
			"fiscal_year": self.fiscal_year,
			"month": self.month,
			"doctype": "BSC Ledger Entry",
		}))
		ble.insert()

	def on_cancel(self):
		self.update_master(False)
		frappe.db.sql("""delete from `tabBSC Ledger Entry`
			where party_type= 'BSC Initiative' and party_name = %s and month = %s and entry_type='Achieved'""", (self.bsc_initiative,self.month))


	def update_master(self, increase = True):
		master = frappe.get_doc("BSC Initiative", self.bsc_initiative)
		new_target_achieved = (self.target_achieved + master.target_achieved) if increase == True else (master.target_achieved - self.target_achieved)
		master.db_set("target_achieved", new_target_achieved)
		master.db_set("target_progress", ( flt(new_target_achieved) / flt(master.initiative_target) * 100.0 )) if master.initiative_target else 0
		new_count_achieved = (self.log_count if self.is_achieved=='Yes' else 0 + master.count_achieved) if increase == True else (self.log_count if self.is_achieved=='Yes' else 0 + master.count_achieved)
		master.db_set("count_achieved", new_count_achieved)
		master.db_set("count_progress", ( flt(new_count_achieved) / flt(master.initiative_count) * 100.0 )) if master.initiative_count else 0
		master_target = frappe.get_doc("BSC Target", self.bsc_target)
		new_achieved= (self.target_achieved + master_target.achieved) if increase == True else (master_target.achieved - self.target_achieved)
		master_target.db_set("achieved", new_achieved)
		master_target.db_set("progress", ( flt(new_achieved) / flt(master_target.target) * 100.0 )) if master_target.target else 0





