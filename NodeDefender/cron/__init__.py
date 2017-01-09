# Scheduled tasks
from . import cronjobs
StatTaskSched = GeventScheduler()
StatTaskSched.add_job(cronjobs.StatTask, 'interval', minutes=15)
HourlyCron = GeventScheduler()
HourlyCron.add_job(cronjobs.UpdateHourly, 'cron', hour='*')
DailyCron = GeventScheduler()
DailyCron.add_job(cronjobs.UpdateDaily, 'cron', day='*')

StatTaskSched.start()
HourlyCron.start()
DailyCron.start()
