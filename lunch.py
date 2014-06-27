# coding: utf-8

import functools
import order
import ui

WOCHENTAGE = 'Montag Dienstag Mittwoch Donnerstag Freitag'.split()

class MyTableViewDataSource (object):
	
	def __init__(self):
		self.orders = order.Order()
		try:
			with open('orders.json', 'rb') as f:
				self.orders.load_json(f)
		except IOError, e:
			print e
					
	def save(self):
		with open('orders.json', 'wb') as f:
			self.orders.dump_json(f)
			
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 2

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return 5

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		switch = ui.Switch(name='switch')
		switch.flex = 'L'
		switch.x = cell.width - switch.width - 6
		switch.y = (cell.height - switch.height) / 2
		
		if section == 0:
			switch.enabled = False 
			switch.value = self.orders.current[row]
		else:
			switch.enabled = not self.orders.already_ordered
			switch.value = self.orders.next[row]
			switch.action = functools.partial(self.switch_toggled, row=row)
			
		cell.content_view.add_subview(switch)
		cell.text_label.text = WOCHENTAGE[row]
		return cell

	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		return ['Aktuelle Woche', 'Nächste Woche'][section]

	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return False 

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return False 

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		pass

	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		pass
		
	def switch_toggled(self, sender, row):
		print row, sender.value
		self.orders.next[row] = sender.value
		self.save()
	
	def commit(self, sender, tableview):
		finalize = not self.orders.already_ordered
		if finalize:
			pass
		self.orders.already_ordered = finalize 
		self.save()
		tableview.reload_data()
		self.configure_commit_button(sender)
		
	def configure_commit_button(self, button):
		if self.orders.already_ordered:
			button.title = 'Rückgängig'
		else:
			button.title = 'Abschicken'
		

v = ui.load_view('lunch')
tableview = v['table']
commit_button = v['commit']

data_source = MyTableViewDataSource()

tableview.data_source = data_source
commit_button.action = functools.partial(data_source.commit, tableview=tableview)
data_source.configure_commit_button(commit_button)

v.present(style='popover')

