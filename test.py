from statistics import Statistics
import json
from datetime import datetime

statistics = Statistics("stats.json")

data = statistics.data

print(statistics.games_played)
print(statistics.average_score)
print((statistics.total_play_time)/(1000*60*60))