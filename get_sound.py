from flask import Flask, send_file
from bs4 import BeautifulSoup as bs
from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import datetime
from pprint import pprint
from cStringIO import StringIO
from flask import make_response

import sys, json, time, urllib2, urllib

app = Flask(__name__)

def getMsc(s):
	l = s.split(':')
	return int(l[0]) * 3600000 + int(l[1]) * 60000 + int(l[2].split('.')[0]) * 1000 + int(l[2].split('.')[1])

@app.route('/sound/<word>')
def get_sound(word):
	obj = urllib2.urlopen('http://127.0.0.1:8984/solr/select?q=word:' + word + '&wt=json')
	thing = json.loads(obj.read())
	result = thing['response']['docs'][0]
	beginning = getMsc(result['begin'])
	ending = getMsc(result['end'])
	video = result['video_file']
	song = AudioSegment.from_file(video)
	new_result = song[beginning:ending]
	new_result.export("result.wav", format="wav")
	return send_file('result.wav', mimetype='audio/wav', as_attachment=True,attachment_filename="result.wav")

if __name__ == '__main__':
    app.run(debug=True)