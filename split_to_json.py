import codecs
import sys
import json
import re

lines = {}

def split_line_parser(line):
	s = line
	splitters = ".!?:"
	lesser_splitters = " |"
	cands = sorted(map(lambda x: (x,abs(len(s)/2.-x[0])),filter(lambda x: x[1] in splitters,zip(xrange(len(s)),s))), key=lambda x: x[1])
	if len(cands) == 0:
		cands = sorted(map(lambda x: (x,abs(len(s)/2.-x[0])),filter(lambda x: x[1] in lesser_splitters,zip(xrange(len(s)),s))), key=lambda x: x[1])
	if len(cands) == 0:
		cands = sorted(map(lambda x: (x,abs(len(s)/2.-x[0])),filter(lambda x: True,zip(xrange(len(s)),s))), key=lambda x: x[1])
	limit = int(cands[0][0][0]) + 1
	print limit, cands
	return (line[:limit], line[limit:])


def format_line(line):
	result = line.replace("--", "-")
	result = result.replace("|", " ")
	result = result.strip()
	istart = 0
	ion = True
	while istart != -1:
		istart = result.find("_", istart)
		if istart != -1:
			if ion:
				result = result[:istart] + "<i>" + result[istart+1:]
				ion = False
			else:
				result = result[:istart] + "</i>" + result[istart+1:]
				ion = True
	return result


def save_line(line, line_in_file):
	pos = len(lines)
	ll = format_line(line)
	size = max(2,min(6,2 + (20-len(ll))/20.0))
	res = {'text': ll, 'line': pos, 'next': pos + 1, 'chapter': line_in_file, 'align': "center" if len(ll) < 40 else "left", 'textsize': "%0.2fem" % (size)}
	lines[pos] = (res)


if __name__ == '__main__':
	f = codecs.open("pg4300.txt", "r", "utf-8")
	lif = 0
	curr_line = ""
	for l in f:
		ll = l.strip()
		if len(ll) == 0 and len(curr_line) > 0:
			save_line(curr_line, lif)
			curr_line = ""
		elif len(ll) > 0:
			curr_line = curr_line + "|" + ll
			if len(curr_line) > 200 and curr_line[-1] in ['!?.:']:
				save_line(curr_line, lif)
				curr_line = ""
			elif len(curr_line) > 300:
				(left, right) = split_line_parser(curr_line)
				save_line(left, lif)
				curr_line = right
		lif = lif + 1
	f.close()
	fout = codecs.open("pg4300.json", "w", "utf-8")
	fout.write(json.dumps(lines, indent=4))
	fout.close()


