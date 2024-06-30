import pandas as pd
from datetime import datetime as dt


class EventManager:

	def __init__(self):
		self.data = pd.read_excel('src/engine/data/Bday.xlsx', sheet_name='Family')


	def event_finder(self, time=pd.Timestamp(dt.today())):
		data = self.data.sort_values(['Date'])
		events_today = data[data.Date == time]
		events_nextweek = data[data.Date > pd.Timestamp(dt.today())].iloc[:3, ]
		events_today['Date'] = events_today['Date'].dt.strftime('%Y-%m-%d')
		events_nextweek['Date'] = events_nextweek['Date'].dt.strftime('%Y-%m-%d')
		today_events = events_today.to_json(orient="records")
		upcoming_events = events_nextweek.to_json(orient="records")
		return {"today": today_events, "upcoming_events": upcoming_events}
