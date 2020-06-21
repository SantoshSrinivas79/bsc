# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.model.document import Document

class BSCIndicatorAssignment(Document):
	def validate(self):
		self.validate_duplicate()

	def validate_duplicate(self):
		conditions = ""
		conditions += " where docstatus < 2 and department = '%s'" % self.department
		conditions += " and bsc_indicator = '%s'" % self.bsc_indicator
		conditions += " and fiscal_year= '%s'" % self.fiscal_year
		if frappe.db.exists(self.doctype, self.name):
			conditions += " and name <> '%s'" % self.name
		sum_name = frappe.db.sql("""select count(name) from `tabBSC Indicator Assignment` %s"""% conditions)[0][0]
		if sum_name > 0:
			frappe.throw(_("Already exists with same Department and Indicator and Fiscal Year"))

