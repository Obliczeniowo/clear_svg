#!/usr/bin/env python3
# coding: utf-8

# https://regexone.com/references/python - regularne wyrażenia
# https://github.com/Obliczeniowo/clear_svg/blob/master/clear_svg.py

import re
import sys

class SvgClear:
	def __init__(self, filename):
		self.filename = filename
		self.targetfilename = re.sub(r"\.svg", " - kopia.svg", filename)
		print(self.targetfilename)
		openfile = open(filename, "r")
		
		self.filetext = openfile.read()
		
		openfile.close()
		
		self.clearHeader()
		
		self.clearComments()
		
		self.clearDocumentProperties()
		
		self.filetext = re.sub(r"sodipodi:nodetypes=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:connector-curvature=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"xml:space=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:version=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"version=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"id=\"g\d*?\"|id=\"text\d*?\"|id=\"tspan\d*?\"|id=\"stop\d*?\"", "", self.filetext)
		self.filetext = re.sub(r"fill-opacity:1;*|stroke-opacity:1;*|marker:none;*|stroke-dashoffset:0;*|stroke-dasharray:none;*|visibility:visible;*|display:inline;*|enable-background:accumulate;*|sodipodi:|\s*id=\"defs4\"|inkscape:collect=\"always\"|color-interpolation-filters=\"sRGB\"|xmlns:svg=\".*?\"|inkscape:|xmlns:inkscape=\".*?\"|xmlns:sodipodi=\".*?\"|xmlns:rdf=\".*?\"|font-style:normal;*|font-variant:normal;*|font-weight:normal;*|font-stretch:normal;*|style\"\"", "", self.filetext)
		self.filetext = re.sub(r"overflow:visible;","", self.filetext)
		self.filetext = re.sub(r"linearGradient([\d]{1,})", r'lg\1', self.filetext);
		
		self.clearId("path")
		self.clearId("rect")
		
		self.filetext = re.sub(r"[\s]{2,}", " ", self.filetext)
		
		self.clearPathStyle()
		
		self.filetext = re.sub(r"\s*<namedview.*?>.*?</namedview>", "", self.filetext)
		self.filetext = re.sub(r"\s*<namedview.*?/>\s*", "", self.filetext)
		self.filetext = re.sub(r"<cc:Work.*?</cc:Work>", "", self.filetext)
		self.filetext = re.sub(r"<rdf:RDF>.*?</rdf:RDF>", "", self.filetext)
		self.filetext = re.sub(r">\s*?<", "><", self.filetext)
		self.filetext = re.sub(r"\"\s*?/", "\"/", self.filetext)
		
		self.filetext = self.filetext.strip()
		
		self.write()
	
	def clearHeader(self):
		self.filetext = re.sub(r"<\?.*?\?>", "", self.filetext)
	
	def clearComments(self):
		self.filetext = re.sub(r"<!--.*?-->", "", self.filetext)
		
	def clearDocumentProperties(self):
		self.filetext = re.sub(r"xmlns:dc=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"xmlns:cc=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:window-width=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:window-height=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:window-x=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:window-y=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:window-maximized=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:export-filename=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:export-ydpi=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"inkscape:export-xdpi=\".*?\"", "", self.filetext)
		self.filetext = re.sub(r"docname=\".*?\"", "", self.filetext)
	
	def clearId(self, name):
		matches = re.findall(re.escape(name) + r"[\d-]{1,}", self.filetext)
		for match in matches:
			if re.search("#" + match, self.filetext) is None:
				#print(match + " " + "id=\"{match}\"".format(match = match))
				print("Remove some uselsess ID: " + match);
				self.filetext = self.filetext.replace("id=\"{match}\"".format(match = match), "")
				
	def clearPathStyle(self):
		paths = re.findall(r"<path.*?/>", self.filetext)
		count = 0
		for path in paths:
			#print(path)
			if re.search(r"stroke:none", path):
				count += 1
				print("Remove stroke none useless style definitions from path objects number: {nr}".format(nr = count))
				newpath = re.sub(r"color:.*?;", "", path)
				newpath = re.sub(r"stroke-width:\d+;", "", newpath)
				self.filetext = self.filetext.replace(path, newpath, 1)
				#print("newpath = " + newpath)
	
	def write(self):
		with open(self.targetfilename, "w") as writefile:
			writefile.write(self.filetext)

print(sys.argv)
#SvgClear("Uwaga.svg")
for svgFile in sys.argv[1:]:
	svgclear = SvgClear(svgFile)
print("It is done Youri?\nNo camrat premier, it is only began")
k = input()
