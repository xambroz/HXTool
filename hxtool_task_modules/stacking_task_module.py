#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import hxtool_global
from .task_module import *
from hxtool_data_models import *
from hx_audit import *

class stacking_task_module(task_module):
	def __init__(self, parent_task):
		super(type(self), self).__init__(parent_task)
		self.logger = parent_task.logger
	
	def run(self, bulk_download_id, hostname, bulk_download_path = None, delete_bulk_download = False):
		try:
			if bulk_download_path:
				stack_job = hxtool_global.hxtool_db.stackJobGet(self.parent_task.profile_id, bulk_download_id)
				stack_model = hxtool_data_models(stack_job['stack_type']).stack_type
				audit_pkg = AuditPackage(bulk_download_path)
				audit_data = audit_pkg.get_audit(generator=stack_model['audit_module'])
				if audit_data:
					records = get_audit_records(audit_data, stack_model['audit_module'], stack_model['item_name'], fields=stack_model['fields'], post_process=stack_model['post_process'], hostname=hostname)
					if records:
						hxtool_global.hxtool_db.stackJobAddResult(self.parent_task.profile_id, bulk_download_id, hostname, records)
						self.logger.debug("Stacking records added to the database for bulk job {0} host {1}".format(bulk_download_id, hostname))
						if delete_bulk_download:
							os.remove(os.path.realpath(bulk_download_path))
						return(True, None)
				else:
					print("Stacking: No audit data for {} from bulk acquisition {}".format(hostname, bulk_download_id))
			else:
				print("bulk_download_path is empty!")
				return(False, None)
		except:
			raise
			return(False, None)