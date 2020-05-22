#chiptune Cafe CSV based OBS music stream script
#by pegmode

#I am so sorry about the organization of obj interactions

import csv,sys

#File paths
CSV_PATHS = ["cat1.csv","cat2.csv","cat3.csv"]#ordered categories col1 = songName, col2 = ArtistName
OUTPUT_ARTIST_PATH = "CurrentArtist.txt"
OUTPUT_SONG_PATH = "CurrentSong.txt"
#text
STARTUPTEXT = '''****CC Stream SCRIPT****
Csv based obs music stream script
by pegmode

Type help for commands'''
HELPTEXT = '''
commands:
next - go to next entry in current category
back - go to previous entry in current category
jumpTo [entry num]- jump to num entry in current category
current - display current song
category [category num] - change to category
exit - exit script

nums are indexed at zero
'''

class SongContainer():
	def __init__(self,categories):
		self.categories = categories
		self.currentCat = 0
		self.currentEntry = 0
	def nextS(self):
		if self.currentEntry < len(self.categories[self.currentCat]) - 1:
			self.currentEntry += 1
		else:
			print("**WARNING: end of category")
	def backS(self):
		if self.currentEntry > 0:
			self.currentEntry -= 1
		else:
			print("**WARNING: at beginning of category")
	def jumpTo(self,pos):
		if 0 <= pos <= len(self.categories[self.currentCat]) - 1:
			self.currentEntry = pos
		else:
			print("**WARNING: position {} out of range".format(pos))
	def changeCategory(self,cat):
		if 0 <= cat <= len(self.categories) - 1:
			self.currentCat = cat
			self.currentEntry = 0
		else:
			print("**WARNING: category out of range")
	def getCurrentSongName(self):
		return self.categories[self.currentCat][self.currentEntry][0]
	def getCurrentSongArist(self):
		return self.categories[self.currentCat][self.currentEntry][1]
		
#functions

def startup():
	categories = []
	i = 0
	for cat in CSV_PATHS:
		currentCat = []
		CSV_f = open(cat)
		CSV_Entires =csv.reader(CSV_f,delimiter = ',')
		for entry in CSV_Entires:
			currentCat.append(entry)
			#print(entry)
		categories.append(currentCat)
		CSV_f.close()
	print("Loaded {} categories".format(len(categories)))
	return SongContainer(categories)
		
def nextS(sContainer):
	sContainer.nextS()
	updateSong(sContainer)
	current(sContainer)

def backS(sContainer):
	sContainer.backS()
	updateSong(sContainer)
	current(sContainer)

def current(sContainer):
	print("category {}\nentry {}\ncurrent song: {} - {}".format(sContainer.currentCat,sContainer.currentEntry,sContainer.getCurrentSongName(),sContainer.getCurrentSongArist()))
	
def jumpTo(sContainer,arg):
	sContainer.jumpTo(arg)
	updateSong(sContainer)
	current(sContainer)
	
def changeCategory(sContainer,arg):
	sContainer.changeCategory(arg)
	updateSong(sContainer)
	current(sContainer)
	
def exitS(sContainer):
	sys.exit(0)
	
def helpS(sContainer):
	print(HELPTEXT)
	
def updateSong(sContainer):
	f = open(OUTPUT_SONG_PATH,'w+')
	f.truncate(0)
	f.write(sContainer.getCurrentSongName())
	f.close
	f = open(OUTPUT_ARTIST_PATH,'w+')
	f.truncate(0)
	f.write(sContainer.getCurrentSongArist())
	f.close


#command dict & func pointers
command_dict = {
	"next":nextS,
	"back":backS,
	"jumpTo":jumpTo,
	"current":current,
	"exit":exitS,
	"help":helpS,
	"category":changeCategory
}

#main loop

print(STARTUPTEXT)
sContainer = startup()
updateSong(sContainer)
current(sContainer)
while True:
	commands = input("> ").split()
	#sorry about this mess
	if len(commands) == 0:
		continue
	elif commands[0] in command_dict and len(commands) == 1:
		command_dict[commands[0]](sContainer)
	elif  commands[0] in command_dict and len(commands) == 2:
		if isinstance(commands[1],int):
			command_dict[commands[0]](sContainer,int(commands[1]))
		else:
			print("Malformatted arguement")
	else:
		print("incorrect command\n"+HELPTEXT)
		
