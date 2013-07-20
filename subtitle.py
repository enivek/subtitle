#!/usr/bin/python
import sys
import re


class Time(object):
  
  def __init__(self, in_str):
    self.hour = 0
    self.minute = 0 
    self.sec = 0
    self.milli = 0
    res = re.search("([0-9]{0,2}):([0-9]{0,2}):([0-9]{0,2}),([0-9]{0,3})", in_str)
    if res is not None:
      # print res.group(1) + ";" + res.group(2) + ";" + res.group(3) + ";" + res.group(4)
      self.hour = int(res.group(1))
      self.minute = int(res.group(2))
      self.sec = int(res.group(3))
      self.milli = int(res.group(4))
    else:
       raise Exception( in_str + " is not a valid time format" )

  def to_milli(self):
    return (self.milli + self.sec*1000 + self.minute*60*1000 + 
            self.hour*60*60*1000)  

  def add(self, in_time):
    total_milli = self.to_milli() + in_time.to_milli()
    self.hour = int(total_milli / (60*60*1000))
    total_milli -= (self.hour*(60*60*1000))
    self.minute = int(total_milli / (60*1000))
    total_milli -= (self.minute*(60*1000))
    self.sec = int(total_milli / 1000)
    total_milli -= (self.sec*1000)
    self.milli = total_milli
        
  def __str__(self):
    str_h = ("0" + str(self.hour))[-2:]
    str_m = ("0" + str(self.minute))[-2:]
    str_s = ("0" + str(self.sec))[-2:]
    str_mi = ("00" + str(self.milli))[-3:]
    return str_h + ":" + str_m + ":" + str_s + "," + str_mi   


class Subtitle(object):

  def __init__(self):
    self.num = ""
    self.time = ""
    self.text = ""  
    self.start_time = None
    self.end_time = None

  def __str__(self):
    return ("[" + str(self.num) + "#" + str(self.start_time) + "#" + str(self.end_time) + "#" + self.time + "#" + self.text + "]")


class CorrectSubtitle(object):

  def correct(self, in_file, in_time):
    li_of_sub = self.extract_subtitles(in_file)
    #for sub in li_of_sub:
    #  print "->" + str(sub)

    for sub in li_of_sub:
      sub.start_time.add(in_time)
      sub.end_time.add(in_time)
      #print "->" + str(sub)
      print sub.num
      print str(sub.start_time) + " --> " + str(sub.end_time)
      print sub.text
      print 

  def extract_subtitles(self, in_file):
    # Extract list of strings from file.
    li_of_str = self.read_file(in_file)
    # print "found " + str(len(li_of_str)) + " lines"

    # Extract list of subtitle objects from list of strings
    li_of_sub = []
    x = 0
    while x+4 <= len(li_of_str):
      s = Subtitle()
      s.num = li_of_str[x]
      s.time = li_of_str[x+1]
      s.text = li_of_str[x+2]
      i = 3
      txt = li_of_str[x+i]
      while len(txt) > 0:
        s.text += ("\r\n" + txt)
        i += 1
        txt = li_of_str[x+i]  

      li_of_sub.append(s)
      x += i+1
    # print "found " + str(len(li_of_sub)) + " subtitles"
       
    # Convert time in subtitle to object
    for s in li_of_sub:
      try:
        self.set_date(s)
        #print s
      except Exception as e:
        print "Error: " + str(s)

    # Return it
    return li_of_sub

  def set_date(self, in_sub):
    res = re.search("([0-9|:|,]+) --> ([0-9|:|,]+)", in_sub.time)    
    in_sub.start_time = Time(res.group(1))
    in_sub.end_time = Time(res.group(2))

  def read_file(self, in_file):
    li = []
    for line in open(in_file, "r"):
      li.append(line.strip())
    return li

if __name__ == "__main__":
  cs = CorrectSubtitle()
  t = Time(sys.argv[2])
  cs.correct( sys.argv[1], t)


