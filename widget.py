#!python3

'''
This widget script shows a single button and a label.
Tapping the button simulates a dice roll and shows the result in the label.
'''
import datetime

import appex
import ui

import order


orders = order.Order()
try:
	with open('orders.json', 'r') as f:
		orders.load_json(f)
	now = datetime.datetime.now()
	weekday = now.date().weekday()
	if weekday < len(orders.current) and now.hour < 14:
		day_label = 'Heute'
		day_status = orders.current[weekday]
	elif weekday + 1 < len(orders.current):
		day_label = order.WEEKDAYS[weekday + 1]
		day_status = orders.current[weekday + 1]
	else:
		day_label = order.WEEKDAYS[0]
		day_status = orders.next[0]
	day_message = 'Kantine' if day_status else 'keine Kantine'
	message = day_label + ' ' + day_message
		
except IOError as e:
	print(e)
	message = e.strerror


		
def button_action(sender):
	import webbrowser
	webbrowser.open('pythonista3://lunch/lunch?action=run')
	
v = ui.View(frame=(0, 0, 300, 110))

label = ui.Label(frame=(0, 0, 150, 110), flex='lwh', font=('<System>', 24), alignment=ui.ALIGN_CENTER, name='result_label')
label.text = message
v.add_subview(label)

if not orders.already_ordered:
	button = ui.Button(title='Bestellen', font=('<System>', 24), flex='rwh', action=button_action)
	button.frame = (200, 0, 150, 110)
	v.add_subview(button)

appex.set_widget_view(v)


