from flask import Flask, send_file, make_response
from bs4 import BeautifulSoup as bs
from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import datetime
from pprint import pprint
from cStringIO import StringIO
from pycaption import DFXPReader, SRTWriter
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate


import sys, json, time, urllib2, urllib, os

app = Flask(__name__)

def getMsc(s):
	l = s.split(':')
	return int(l[0]) * 3600000 + int(l[1]) * 60000 + int(l[2].split('.')[0]) * 1000 + int(l[2].split('.')[1])

@app.route('/video/<word>')
def get_sound(word):
	#obj = urllib2.urlopen('http://127.0.0.1:8984/solr/select?q=word:' + word + '&wt=json')
	#thing = json.loads(obj.read())
	#result = thing['response']['docs'][0]
	#beginning = getMsc(result['begin'])
	#ending = getMsc(result['end'])
	#video = result['video_file']
	#song = AudioSegment.from_file(video)
	#new_result = song[beginning:ending]
	#new_result.export("result.wav", format="wav")
	os.system('python videogrep/videogrep.py --input episodes/ --search \'' + word + '\'')
	if(os.path.isfile('supercut.mp4')):
		return send_file('supercut.mp4', mimetype='video/mp4', as_attachment=True,attachment_filename="supercut.mp4")
	else:
		return ':('

if __name__ == '__main__':
    app.run(debug=True)