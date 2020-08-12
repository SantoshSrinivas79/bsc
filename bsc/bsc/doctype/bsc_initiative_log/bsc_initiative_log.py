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
		self.validate_target()
		self.validate_mandatories()
		self.validate_initiative()

	def validate_initiative(self):
		bsc_initiative= frappe.get_doc("BSC Initiative", self.bsc_initiative)
		if bsc_initiative.docstatus!=1:
			frappe.throw(_("BSC Initiative must to be submitted"))
		allow_create= frappe.db.get_single_value('BSC Settings', 'allow_without_target')

	def validate_month(self):
		bsc_initiative= frappe.get_doc("BSC Initiative", self.bsc_initiative)
		bsc_target= frappe.get_doc("BSC Target", self.bsc_target)
		res = frappe.db.sql("""SELECT count(*) FROM `tabBSC Ledger Entry` 
			WHERE bsc_initiative=%s and month = %s""", (self.bsc_initiative,self.month))
		if res[0][0]==0:
			if not bsc_initiative.based_last_month and bsc_target.based_last_month:
				return
			allow_create= frappe.db.get_single_value('BSC Settings', 'allow_create_log_for_not_mentioned_month')
			if allow_create==0:
				frappe.msgprint(_("There is no Target for current month {0}".format(self.month)))
			else:
				frappe.throw(_("There is no Target for current month {0}".format(self.month)))

	def validate_target(self):
		bsc_initiative= frappe.get_doc("BSC Initiative", self.bsc_initiative)
		bsc_target= frappe.get_doc("BSC Target", self.bsc_target)
		if self.log_target==0:
			if not bsc_initiative.based_last_month and bsc_target.based_last_month:
				return
			res = frappe.db.sql("""SELECT count(*) FROM `tabBSC Ledger Entry` 
				WHERE entry_type='Targeted' and bsc_initiative = %s and month = %s""", (self.bsc_initiative,self.month))
			if res[0][0]==0:
				allow_create= frappe.db.get_single_value('BSC Settings', 'allow_without_target')
				if allow_create==1:
					self.target_progress=0
					frappe.msgprint(_("There is no Target for current month {0}".format(self.month)))
				else:
					frappe.throw(_("There is no Target for current month {0}".format(self.month)))
		else:
			self.target_progress=flt(self.target_achieved)/flt(self.log_target)*100 if self.target_achieved>0.0 else 0.0

	def validate_mandatories(self):
		if not frappe.db.exists(self.doctype, self.name):
			return
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
		months = {
			"Jan": '01',
			"Feb": '02',
			"Mar": '03',
			"Apr": '04',
			"May": '05',
			"Jun": '06',
			"Jul": '07',
			"Aug": '08',
			"Sep": '09',
			"Oct": '10',
			"Nov": '11',
			"Dec": '12'
		}
		if self.month and self.fiscal_year:
			self.start_date=getdate(self.fiscal_year+'-'+months[self.month]+'-01')
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
		frappe.db.sql("""delete from `tabBSC Ledger Entry`
			where bsc_initiative_log = %s """, self.name)
		self.update_master(False)

	def update_master(self, increase = True):
		ble_map = frappe._dict()
		self.target_progress=(flt(self.target_achieved)/flt(self.log_target)*100) if flt(self.log_target)!=0 else 0
		
		master = frappe.get_doc("BSC Initiative", self.bsc_initiative)
		master_target = frappe.get_doc("BSC Target", self.bsc_target)
		if master.based_last_month:
			months = {
				"Jan": '01', "Feb": '02', "Mar": '03',"Apr": '04', "May": '05', "Jun": '06',\
				"Jul": '07', "Aug": '08', "Sep": '09', "Oct": '10', "Nov": '11', "Dec": '12'\
				}
			max_month=[]
			all_ble = {}
			ble_list = frappe.db.sql("""SELECT entry_number,month FROM `tabBSC Ledger Entry` 
				WHERE entry_type='Achieved' and bsc_initiative=%s """, self.bsc_initiative, as_dict=True)
			new_target_achieved=0.0

			if ble_list:
				for ble in ble_list:
					if ble:
						if increase!=True:
							if months[ble.month]!=months[self.month]:
								all_ble[months[ble.month]] = {}
								all_ble[months[ble.month]]['entry_number']=ble.entry_number
								max_month.append(months[ble.month])
						else:
							max_month.append(months[ble.month])
							all_ble[months[ble.month]] = {}
							all_ble[months[ble.month]]['entry_number']=ble.entry_number


			if increase==True:
				all_ble[months[self.month]] = {}
				all_ble[months[self.month]]['entry_number']=self.target_achieved
				max_month.append(months[self.month])

			new_target_achieved=all_ble[max(max_month)].get('entry_number',0.0)
			master.db_set("target_achieved", new_target_achieved)
			master.db_set("target_progress", ( flt(new_target_achieved) / flt(master.initiative_target) * 100.0 ))
			master_target.db_set("achieved",new_target_achieved)
			master_target.db_set("progress",flt(new_target_achieved)/flt(master_target.target)*100.0)
			new_count_achieved = (self.log_count if self.is_achieved=='Yes' else 0 + master.count_achieved) if increase == True else (self.log_count if self.is_achieved=='Yes' else 0 + master.count_achieved)
			master.db_set("count_achieved", new_count_achieved)
			master.db_set("count_progress", ( flt(new_count_achieved) / flt(master.initiative_count) * 100.0 )) if master.initiative_count else 0
	
			return
			
		new_target_achieved = (self.target_achieved + master.target_achieved) if increase == True else (master.target_achieved - self.target_achieved)
		master.db_set("target_achieved", new_target_achieved)
		master.db_set("target_progress", ( flt(new_target_achieved) / flt(master.initiative_target) * 100.0 )) if master.initiative_target else 0
		new_count_achieved = (self.log_count if self.is_achieved=='Yes' else 0 + master.count_achieved) if increase == True else (self.log_count if self.is_achieved=='Yes' else 0 + master.count_achieved)
		master.db_set("count_achieved", new_count_achieved)
		master.db_set("count_progress", ( flt(new_count_achieved) / flt(master.initiative_count) * 100.0 )) if master.initiative_count else 0		
		if self.bsc_target:
			if master_target.calculation_method=='Numerical':
				new_achieved=(flt(master_target.achieved)+flt(self.target_achieved)) if increase == True else (flt(master_target.achieved)-flt(self.target_achieved))
				master_target.db_set("achieved",new_achieved)
				master_target.db_set("progress",flt(new_achieved)/flt(master_target.target)*100.0)
			elif master_target.calculation_method=='Percentage':
				master_target.db_set("progress",(flt(master_target.progress)+flt(self.target_achieved)) if increase == True else (flt(master_target.progress)-flt(self.target_achieved)))
			elif master_target.calculation_method=='Cumulative':
				conditions = " where name <> '%s'" % self.bsc_initiative 
				conditions += " and bsc_target = '%s'" % self.bsc_target 
				sum_initiative = frappe.db.sql("""select IFNULL(sum(initiative_target),0.0), IFNULL(sum(target_achieved),0.0) from `tabBSC Initiative` %s"""% conditions)
				master_target.db_set("progress",flt((sum_initiative[0][1]+(new_target_achieved))/(sum_initiative[0][0]+(master.initiative_target))*100))

