# Create build glyphs file :
# Turn on Export for Bracket Glyphs (given as argument from shell) and disable non ttf instances
# Add extra opentype code for rvrn glyphs that are substituted by another feature as well

import sys
from glyphsLib import GSFont
from glyphsLib import GSGlyph

file = sys.argv[1]

font = GSFont(file)
print "\tPreparing %s" % file

# Glyphs to re-enable export, in the Glyphs App export these are not active but get swapped with a custom parameter
italicBracketGlyphs = [
"cedi.rvrn",
"colonsign.rvrn",
"guarani.rvrn",
"cent.rvrn",
"dollar.rvrn",
"dollar.tf.rvrn",
"cent.tf.rvrn",
"naira.rvrn",
"peseta.rvrn",
"won.rvrn",
"peso.rvrn",
"curvedStemParagraphSignOrnament.rvrn",
"paragraph.rvrn"
]

uprightBracketGlyphs = italicBracketGlyphs + [
"apple.rvrn",
"Adieresis.rvrn",
"Odieresis.rvrn",
"Udieresis.rvrn",
"Adieresis.titl.rvrn",
"Odieresis.titl.rvrn",
"Udieresis.titl.rvrn",
]

# Extra FEA code so that the glyphs swapped by rvrn can be substituted again by another opentype feature
# https://github.com/fonttools/fonttools/issues/1371#issuecomment-437613378
uprightFeaCode = [
("tnum", """sub cent.rvrn by cent.tf.rvrn; # for rvrn
sub dollar.rvrn by dollar.tf.rvrn; # for rvrn"""),
("titl", """# for rvrn
sub Adieresis.rvrn by Adieresis.titl.rvrn;
sub Odieresis.rvrn by Odieresis.titl.rvrn;
sub Udieresis.rvrn by Udieresis.titl.rvrn;""")
]

italicFeaCode = [
("tnum", """sub cent.rvrn by cent.tf.rvrn; # for rvrn
sub dollar.rvrn by dollar.tf.rvrn; # for rvrn""")
]

for instance in font.instances:
	deavtivateThisInstance = True
	for customParam in instance.customParameters:
		if customParam.name == "Save as TrueType" and customParam.value == 1:
			deavtivateThisInstance = False
	if deavtivateThisInstance == True:
		instance.active = 0

style = sys.argv[2]
if style == "Italic":
	glyphsToActivateExport = italicBracketGlyphs
	appendFeatureCode = italicFeaCode
elif style == "Upright":
	glyphsToActivateExport = uprightBracketGlyphs
	appendFeatureCode = uprightFeaCode

for eachGlyph in glyphsToActivateExport:
	font.glyphs[eachGlyph].export = 1

for feaCode in appendFeatureCode:
	for f in font.features:
		if f.name == feaCode[0]:
			f.code += "\n" + feaCode[1]
			f.automatic = False
			# print f.code

newFileName = file.replace(".glyphs", "-build.glyphs")

font.save(newFileName)