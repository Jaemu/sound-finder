from bs4 import BeautifulSoup as bs
from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import datetime
from pprint import pprint
import sys, json, time
from cStringIO import StringIO
from pycaption import DFXPReader, SRTWriter, CaptionConverter

doc = []
unique_id = 0

def getMsc(s):
	l = s.split(':')
	return int(l[0]) * 3600000 + int(l[1]) * 60000 + int(l[2].split('.')[0]) * 1000 + int(l[2].split('.')[1])

def toJson(captions):
	global unique_id
	caption_data = bs(open(captions + '.xml'))
	song = AudioSegment.from_file(captions + '.mp4')
	for segment in caption_data.find_all('p'):
		original = segment.find('span').get_text().replace('!', ' ').replace(',', ' ').strip('[').strip(']').replace('.', ' ')
		text = original.split(' ')
		beginning = getMsc(segment.get('begin'))
		ending = getMsc(segment.get('end'))
		thing = song[beginning:ending]
		for word in text:	
			new_segment = {}
			index = text.index(word)
			new_segment['id'] = unique_id
			new_segment['begin'] = segment.get('begin')
			new_segment['end'] = segment.get('end')
			new_segment['caption_file'] = captions + '.srt'
			new_segment['video_file'] = captions + '.mp4'
			new_segment['word'] = word
			new_segment['phrase'] = text
			new_segment['phraseText'] = original
			doc.append(new_segment)
			unique_id = unique_id + 1

		
def toSrt(file_name):
	converter = CaptionConverter()
	transcript = open(file_name + '.xml')
	new_transcript = transcript.read().replace('&#x266A;', '')
	converter.read(unicode(new_transcript), DFXPReader())
	f = open(file_name + '.srt', 'w')
	string = converter.write(SRTWriter())
	f.write(string)
	f.close()


if __name__ == "__main__": 
	for line in sys.stdin.readlines():
		toJson('episodes/' + line.rstrip('\n'))	
	print json.dumps(doc, indent=4, separators=(',', ': '))
