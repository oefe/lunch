#coding: utf-8
import datetime
import json

WOCHENTAGE = 'Montag Dienstag Mittwoch Donnerstag Freitag'.split()
WEEKLABEL = ['Diese Woche', 'Nächste Woche']

class Order (object):

    def __init__(self, clock=datetime.datetime.now):
        self.clock = clock
        self.current = (False, False, False, False, False)
        self.next = [False, False, False, False, False]
        self.already_ordered = False

    def dump_json(self, f):
        this, next = self._json_keys()
        d = {}
        d[this] = dict(final=True, orders=self.current,)
        d[next] = dict(final=self.already_ordered, orders=self.next)
        json.dump(d, f)

    def load_json(self, f):
        this, next = self._json_keys()
        d = json.load(f)
        dd = d.get(this)
        if dd and dd['final']:
            self.current = tuple(dd['orders'])
        dd = d.get(next)
        if dd:
            self.already_ordered = dd['final']
            self.next = dd['orders']

    def first_day(self):
        today = self.clock().date()
        weekday = today.weekday()
        return today - datetime.timedelta(days=weekday)

    def label(self, week, day):
        d = self.first_day() + datetime.timedelta(weeks=week, days=day)
        return '{wd} {d}.{m}.'.format(wd = WOCHENTAGE[day], d=d.day, m=d.month)
        
    def weeklabel(self, week):
        d = self.first_day() + datetime.timedelta(weeks=week)
        return '{p} - KW{iw}'.format(p=WEEKLABEL[week], iw=d.isocalendar()[1])
        
    def _json_keys(self):
        this_monday = self.first_day()
        next_monday = this_monday + datetime.timedelta(days=7)
        return self._json_key(this_monday), self._json_key(next_monday)

    @staticmethod
    def _json_key(date):
        year, week, _ = date.isocalendar()
        return '{year}-{week:02}'.format(year=year, week=week)

if __name__ == '__main__':
    import StringIO
    import unittest

    class TestOrder(unittest.TestCase):

        def test_empty(self):
            b = Order()
            self.assertItemsEqual(b.current, [False] * 5)
            self.assertItemsEqual(b.next, [False] * 5)
            self.assertFalse(b.already_ordered)

        def test_save_load(self):
            self.now = datetime.datetime(2014, 6, 24, 12, 30)
            a = Order(clock=self.clock)
            a.next[0] = True
            a.already_ordered = True
            json = self.save(a)
            b = self.load(json)
            self.assertTrue(b.next[0])
            self.assertTrue(b.already_ordered)

        def test_save_load_later_same_week(self):
            self.now = datetime.datetime(2014, 6, 24, 12, 30)
            a = Order(clock=self.clock)
            a.next[0] = True
            a.already_ordered = True
            json = self.save(a)
            self.now = datetime.datetime(2014, 6, 26, 12, 30)
            b = self.load(json)
            self.assertTrue(b.next[0])
            self.assertTrue(b.already_ordered)

        def test_save_load_next_week(self):
            self.now = datetime.datetime(2014, 6, 24, 12, 30)
            a = Order(clock=self.clock)
            a.next[0] = True
            a.already_ordered = True
            json = self.save(a)
            self.now = datetime.datetime(2014, 7, 1, 12, 30)
            b = self.load(json)
            self.assertTrue(b.current[0])
            self.assertFalse(b.next[0])
            self.assertFalse(b.already_ordered)

        def test_save_load_two_weeks_later(self):
            self.now = datetime.datetime(2014, 6, 24, 12, 30)
            a = Order(clock=self.clock)
            a.next[0] = True
            a.already_ordered = True
            json = self.save(a)
            self.now = datetime.datetime(2014, 7, 8, 12, 30)
            b = self.load(json)
            self.assertItemsEqual(b.current, [False] * 5)
            self.assertItemsEqual(b.next, [False] * 5)
            self.assertFalse(b.already_ordered)
        
        def test_label(self):
            self.now = datetime.datetime(2015, 4, 6, 12, 30)
            a = Order(clock=self.clock)
            self.assertEqual(a.label(0, 0), 'Montag 6.4.')                
            self.assertEqual(a.label(0, 4), 'Freitag 10.4.')
            self.assertEqual(a.label(1, 0), 'Montag 13.4.')                
            self.assertEqual(a.label(1, 4), 'Freitag 17.4.')
        
        def test_weeklabel(self):
            self.now = datetime.datetime(2015, 4, 6, 12, 30)
            a = Order(clock=self.clock)
            self.assertEqual(a.weeklabel(0), 'Diese Woche - KW15')                
            self.assertEqual(a.weeklabel(1), 'Nächste Woche - KW16')
                        
        def save(self, order):
            f = StringIO.StringIO()
            order.dump_json(f)
            return f.getvalue()

        def load(self, json):
            #print json
            f = StringIO.StringIO(json)
            order = Order(clock=self.clock)
            order.load_json(f)
            return order

        def clock(self):
            return self.now

    unittest.main()
