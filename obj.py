import sys
"""
An object that continuously emits Particles in the direction specified
"""
class Emitter(object):
	def __init__(self, coords, direction, board, out=0):
		self.b = board
		self.coords = coords
		self.direction = direction
		self.out = out
		self.emit = True
		self.c = "{},{}".format(self.coords[0],self.coords[1])
		if not self.b.d.get(self.c,False):
				self.b.d[self.c] = []
		self.b.d[self.c].append(self)
		self.b.emitters.append(self)

	def update(self):
		#buggy!
		if not self.emit:
			return	
		for i in self.b.d[self.c]:
			if isinstance(i, Particle):
				self.emit=False
				self.b.d[self.c].remove(i)
				self.b.particles.remove(i)
				print "off"
		#print "making particle"
		if self.direction == "N":
			newcoords = "{},{}".format(self.coords[0], self.coords[1]+1)
		elif self.direction == "S":
			newcoords = "{},{}".format(self.coords[0], self.coords[1]-1)
		elif self.direction == "E":
			newcoords = "{},{}".format(self.coords[0]+1, self.coords[1])
		elif self.direction == "W":
			newcoords = "{},{}".format(self.coords[0]-1, self.coords[1])
		if not self.b.d.get(newcoords,False):
			self.b.d[newcoords] = []
			#print "allocating {}".format(newcoords)
		self.b.d[newcoords].append(Particle(newcoords.split(","), self.direction, self.out, self.b))
		#print "sending {} {}".format(self.out, self.direction)
"""
An object, that, when it receives Particles, absorbs them, then prints their values
"""
class Enumerator(object):
	def __init__(self, coords,board):
		self.coords = coords
		self.b =board
		self.c = "{},{}".format(self.coords[0],self.coords[1])
		if not self.b.d.get(self.c,False):
				self.b.d[self.c] = []
		self.b.d[self.c].append(self)
		self.b.enumerators.append(self)
	def update(self):
		for i in self.b.d[self.c]:
			#print self.b.d
			if isinstance(i, Particle):
				self.b.d[self.c].remove(i)
				self.b.particles.remove(i)
				sys.stdout.write("{}".format(i.value))
				sys.stdout.flush()
		#check whether there is a 
		#particle in the immediate vicinity

"""
A moving dot with a stored value.
"""
class Particle(object):
	def __init__(self, coords, direction, value,board):
		self.coords = coords
		self.b = board
		self.direction = direction
		self.value = value
		c = "{},{}".format(self.coords[0],self.coords[1])
		if not self.b.d.get(c,False):
				self.b.d[c] = []
		self.b.d[c].append(self)
		self.b.particles.append(self)

	def update(self):
		#print self.coords
		prev = "{},{}".format(self.coords[0],self.coords[1])
		if self.direction == "N":
			self.coords[1] = str(int(self.coords[1])+1)
		elif self.direction == "S":
			self.coords[1] = str(int(self.coords[1])-1)
		elif self.direction == "E":
			self.coords[0] = str(int(self.coords[0])+1)
		elif self.direction == "W":
			self.coords[0] = str(int(self.coords[0])-1)
		cur = "{},{}".format(self.coords[0],self.coords[1])
		self.b.d[prev].remove(self)
		if not self.b.d.get(cur):
			self.b.d[cur] = []
		self.b.d[cur].append(self)
"""
An object that performs operations on Particles based on very basic instruction sets.

Potential Instruction Set:
+ W : increment the particle and send it west
+ WE: increment the particle and sent it west and east
- decrement
= 23 W E if particle == 23 send west else east
directions: WENS and _: nothing
+
-
= 
or:
NO#e <char> <direction> (emit)
t <in> <out> <direction>
n <a|n> (enumerate a(scii) or n(umerical))


"""
class Emulator(object):
	def __init__(self, coords, board, iSet):
		print "setup"
		self.iSet = iSet
		self.coords = coords
		self.b = board
		c = "{},{}".format(self.coords[0],self.coords[1])
		if not self.b.d.get(c,False):
				self.b.d[c] = []
		self.b.d[c].append(self)
		self.b.emitters.append(self)
		self.tokenize()
	def tokenize(self):
		dirs = "EWNS"
		ops = "+=-tn"
		args = "an"
		punct = "|,"
		x = 0
		tokens = []
		while x < len(self.iSet):
			if self.iSet[x] in dirs:
				tokens.append(Token("D", self.iSet[x]))
			elif self.iSet[x] in ops:
				tokens.append(Token("O", self.iSet[x]))
			elif self.iSet[x] in args:
				tokens.append(Token("A", self.iSet[x]))
			elif self.iSet[x] in punct:
				tokens.append(Token("P", self.iSet[x]))
			elif self.iSet[x].isdigit():
				n = self.iSet[x]
				x += 1
				while x < len(self.iSet) and self.iSet[x].isdigit():
					n += self.iSet[x]
					x += 1
				tokens.append(Token("D", n))
			elif self.iSet[x] == " ":
				pass # ignore spaces
			else:
				print "tokeize error: "
				sys.exit(1)
			x += 1
		for i in tokens:
			print i
		self.parse(tokens)
	def parse(self, tokens):
		x = 0
		fn = ""
		while x < len(tokens):
			#print "looking"
			if tokens[x].t == "O":
				if tokens[x].v == "+" or tokens[x].v == "-":
					op = tokens[x].v
					x += 1
					outs = []
					while x < len(tokens) and tokens[x].t == "D":
						outs.append(tokens[x].v)
						x +=1
			x += 1
		print op, outs
	def update(self):
		pass
"""
A method for keeping track of everything.
"""
class Board(object):
	def __init__(self):
		self.d = {}
		self.emitters = []
		self.particles = []
		self.enumerators = []
		self.emulators = []

	#def update(coords, ):

class Token:
	def __init__(self,t, v):
		self.t = t
		self.v = v
	def __str__(self):
		return "{}\t{}".format(self.t, self.v)
