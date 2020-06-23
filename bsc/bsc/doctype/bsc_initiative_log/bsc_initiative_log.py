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
		self.update_master(True)
		# create the BSC Ledger Entry #
		ble = frappe.get_doc(frappe._dict({
			"party_type": "BSC Initiative",
			"party_name": self.bsc_initiative,
			"entry_type": "Achieved",
			"month": self.month,
			"entry_number": 1 if self.is_achieved=='Yes' else 0,
			"department": self.department,
			"doctype": "BSC Ledger Entry"
		}))
		ble.insert()
		#


	def on_cancel(self):
		self.update_master(False)
		frappe.db.sql("""delete from `tabBSC Ledger Entry`
			where party_type= 'BSC Initiative' and party_name = %s and month = %s and entry_type='Achieved'""", (self.bsc_initiative,self.month))


	def update_master(self, increase = True):
		if self.is_achieved == 'Yes':
			master = frappe.get_doc("BSC Initiative", self.bsc_initiative)
			new_achieved = (master.achieved + self.target) if increase == True else (master.achieved - self.target)
			master.db_set("achieved", new_achieved)
			master.db_set("per_initiative", ( flt(new_achieved) / flt(master.time_total) * 100.0 ) )
