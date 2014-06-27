import  notification

n = notification.schedule("Hello, World", delay=5, action_url="pythonista://Sandbox%2Fnotificationtest.py?action=run")
print n
