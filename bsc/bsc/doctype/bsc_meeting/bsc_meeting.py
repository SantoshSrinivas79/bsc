# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ahmed Mohammed Alkuhlani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class BSCMeeting(Document):
	pass

@frappe.whitelist()
def fetch_bsc_committee(source_name, target_doc=None):
	target_doc = get_mapped_doc("BSC Committee", source_name, {
		"BSC Committee": {
			"doctype": "BSC Meeting",
		},
		"BSC Committee Member": {
			"doctype": "BSC Meeting Attendance",
		}
	}, target_doc)

	return target_doc
