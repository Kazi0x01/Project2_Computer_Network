import math

class highLevelMessage:
  def __init__(event,type,time,long,lat):
       event.map = [[0, -1, 2, 10, -1, -1],
                    [-1, 0, -1, 2, 1, -1],
                    [2, -1, 0, 1, -1, 18],
                    [10, 2, 1, 0, 11, 6],
                    [-1, 1, -1, 11, 0, 2],
                    [-1, -1, 18, 6, 2, 0]]
       event.time = time
       event.long = long
       event.lat = lat
       event.type= type

  def distance(self, Event2):
      h= math.sqrt((math.sin((Event2.lat-self.lat)/2))**2 + math.cos(Event2.lat)*math.cos(self.lat)*(math.sin((Event2.long-self.long)/2))**2)
      distance=2*6371000*math.asin(h)
      return distance

