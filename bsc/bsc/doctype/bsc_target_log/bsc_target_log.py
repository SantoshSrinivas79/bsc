# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.model.document import Document
from frappe.utils import (flt, getdate, get_last_day)

class BSCTargetLog(Document):

	def validate(self):
		self.validate_duplicate()
		if self.achieved and self.target:
			self.target_log_percent = flt(flt(self.achieved) / flt(self.target) * 100)
			#frappe.throw(_("ach {0} tar {1} per {2} real {3} withoutlt {4}").format(self.achieved,self.target,self.target_log_percent,flt(self.achieved / self.target),self.achieved / self.target))
		self.validate_dates()


	def validate_duplicate(self):
		conditions = ""
		conditions += " where department = '%s'" % self.department
		conditions += " and bsc_target = '%s'" % self.bsc_target
		conditions += " and month = '%s'" % self.month
		if frappe.db.exists(self.doctype, self.name):
			conditions += " and name <> '%s'" % self.name
		sum_name = frappe.db.sql("""select count(name) from `tabBSC Target Log` %s"""% conditions)[0][0]
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

