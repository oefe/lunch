# coding: utf-8

import datetime
import itertools
import urllib
import urlparse
import webbrowser

TO_ADDRESS = 'somebody@example.com'
WOCHENTAGE = 'Montag Dienstag Mittwoch Donnerstag Freitag'.split()
SUBJECT_FORMAT = 'Essen KW%d'
BODY_FORMAT = '''Hallo Schatz,

Ich habe nächste Woche %s bestellt.

Ich liebe Dich'''
DAYS_NONE = 'nichts'
DAYS_ALL = 'jeden Tag'

def format_days(order):
		if not any(order.next):
			return DAYS_NONE
		elif all(order.next):
			return DAYS_ALL
		else: 
			days = itertools.compress(WOCHENTAGE, order.next)
			return ', '.join(days)

def mail_url(order):
		this_monday = order.first_day()
		next_monday = this_monday + datetime.timedelta(days=7)
		next_week = next_monday.isocalendar()[1]
		subject = SUBJECT_FORMAT % next_week
		body = BODY_FORMAT % format_days(order)
		#query = urllib.urlencode({'subject': subject, 'body': body})
		query = 'subject=%s&body=%s' % (urllib.quote(subject), urllib.quote(body))
		parts = ('mailto', TO_ADDRESS, '', '', query, '')
		url = urlparse.urlunparse(parts)
		return url
		
def send(order):
		webbrowser.open(mail_url(order))
		
if __name__ == '__main__':
	import order
	import unittest
	
	class TestOrderMail(unittest.TestCase):
		
		def test_simple(self):
			self.now = datetime.datetime(2014, 6, 24, 12, 30)
			a = order.Order(clock=self.clock)
			a.next[0] = True
			url = mail_url(a)
			parts = urlparse.urlparse(url)
			self.assertEqual(parts.scheme, 'mailto')
			self.assertEqual(parts.netloc, TO_ADDRESS)
			self.assertEqual(parts.path, '')
			self.assertEqual(parts.params, '')
			query = urlparse.parse_qs(parts.query, 
			                          keep_blank_values=True, 
			                          strict_parsing=True)
			self.assertEqual(parts.fragment, '')
			self.assertEqual(query['subject'][0], 'Essen KW27')
			ordered = [w in query['body'][0] for w in WOCHENTAGE]
			self.assertSequenceEqual(ordered, [True, False, False, False, False])

		def test_format_days(self):
			self.helper_test_format_days_some(True, False, True, False, False)
			self.helper_test_format_days_some(True, False, False, False, False)			
			self.helper_test_format_days_some(False, True, True, True, True)
			self.helper_test_format_days_special(DAYS_NONE, [False] * 5)
			self.helper_test_format_days_special(DAYS_ALL, [True] * 5)
						
		def helper_test_format_days_some(self, *some_days):
			a = order.Order()
			a.next = some_days
			s = format_days(a)
			found = [w in s for w in WOCHENTAGE]
			self.assertSequenceEqual(found, some_days)
						
		def helper_test_format_days_special(self, expected, some_days):
			a = order.Order()
			a.next = some_days
			s = format_days(a)
			self.assertEqual(s, expected)
						
		def clock(self):
			return self.now
			
	unittest.main()

