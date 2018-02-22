import sys,time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Token:
	def __init__(self,t, v):
		self.t = t
		self.v = v
	def __str__(self):
		return "{}\t{}".format(self.t, self.v)

class Piece(object):
	def __init__(self, coords, board):
		self.coords = coords
		self.b = board

		self.c = "{},{}".format(self.coords[0],self.coords[1])
		if not self.b.d.get(self.c,False):
			self.b.d[self.c] = []
		self.b.d[self.c].append(self)

	def update(self):
		print ("not yet implemented\n updating...")

	def listen(self):
		l = []
		for i in self.b.d[self.c]:
			if isinstance(i, Particle):
				self.b.particles.remove(i)
				self.b.d[self.c].remove(i)
				l.append(i)
		self.l = l


class Board(object):
	def __init__(self):
		self.d = {}
		self.emitters = []
		self.particles = []
		self.enumerators = []
		self.emulators = []
		self.emCells = []
		self.inCells = []
		self.step = 0

	def run(self, s):
		visual = []
		numE =0
		for l in s.split("\n"):
			if len(l) == 0 or l[0] == "!":
				continue
			l = l.split(";")
			if len(l) != 3:
				print("incomlete line!")
				print("".join(l))
				sys.exit(1)
			if l[0] == "E":
				self.emitters.append(Emitter(eval(l[1]), self, l[2]))
				sym = "e"
				numE +=1
			elif l[0] == "N":
				self.enumerators.append(Enumerator(eval(l[1]), self, l[2]))
				sym = "n"
			elif l[0] == "M":
				self.emulators.append(Emulator(eval(l[1]), self, l[2]))
				sym = "m"
			elif l[0] == "R":
				self.emCells.append(MemoryCell(eval(l[1]), self, l[2]))
				sym = "r"
			elif l[0] == "I":
				sp = l[2].split(" ")
				self.inCells.append(InputCell(eval(l[1]), self, sp[1], sp[0]))
				sym = "i"
			else:
				print("bad code!")
				print(l)
				sys.exit(1)
			
			coords = eval(l[1])

			while len(visual) < coords[1]+1:
				visual.append([])
			while len(visual[coords[1]]) < coords[0]+1:
				visual[coords[1]].append(" ")
			y = int(coords[1])
			x = int(coords[0])
			width = max([len(x) for x in visual])
			visual[y][x] = sym
		print(bcolors.OKGREEN+"Visualization:"+bcolors.ENDC)
		print("{}{}{}".format(u'\u250c',u'\u2500'*(width),u'\u2510'))
		for line in visual[::-1]:
			print (u'\u2502'+"".join(line).ljust(width)+u'\u2502')
		print("{}{}{}".format(u'\u2514',u'\u2500'*(width),u'\u2518'))
		print(bcolors.OKGREEN+"Program Output:"+bcolors.ENDC)
		run = True
		warning = False
		while run:
			for e in self.emitters:
				e.receive()
			for e in self.enumerators:
				e.receive()
			for e in self.emulators:
				e.receive()
			for e in self.emCells:
				e.receive()
			for e in self.inCells:
				e.receive()
			for e in self.particles:
				e.update()
			for e in self.inCells:
				e.update()
			for e in self.enumerators:
				e.update()
			for e in self.emulators:
				e.update()	
			for e in self.emitters:
				e.update()
			for e in self.emCells:
				e.update()
			if len(self.particles) == 0:
				warning = True
			if warning and len(self.particles) == 0:
				run = False
			self.step += 1

class Emitter(Piece):
	def __init__(self, coords, board, direction):
		super().__init__(coords, board)
		self.direction = direction
		self.emitting = True
		self.value = 0

	def receive(self):
		self.listen()
		for i in self.l:
			if i.strong:
				self.emitting = True
				self.value = i.value
				print("power to emitter:",self.value)
			else:
				self.emitting = False

	def update(self):
		if self.emitting and self.b.step%2 == 0:
			pCoords = newCoords(self.coords, self.direction)
			self.b.particles.append(Particle(pCoords, b, self.direction, self.value,False))
		else:
			pass


class InputCell(Piece):
	def __init__(self, coords, board, direction, code):
		super().__init__(coords, board)
		self.direction = direction
		self.code = code
		self.value = 0

	def receive(self):
		self.listen()

	def update(self):
		for i in self.l:
			#if i.strong:
				#print("STRONG")
			#print(self.code, i.value)
			if str(i.value) == str(self.code):
				#print("MATCH")
				self.value = input("$")
				pCoords = newCoords(self.coords, self.direction)
				self.b.particles.append(Particle(pCoords, b, self.direction, self.value,False))
				self.value = 0
			else:
				pass	

class MemoryCell(Piece):
	def __init__(self, coords, board, direction):
		super().__init__(coords, board)
		self.direction = direction
		self.memory = 0
	
	def receive(self):
		self.listen()

	def update(self):

		if True:
			
			for i in self.l:
				if i.strong:
					pCoords = newCoords(self.coords, self.direction)
					self.b.particles.append(Particle(pCoords, b, self.direction, self.memory,False))
					self.memory = 0
					break
				else:
					self.memory += int(i.value)

class Enumerator(Piece):
	def __init__(self, coords, board, t):
		super().__init__(coords, board)
		self.t = t
		self.toPrint = []
	def receive(self):
		self.listen()
		self.toPrint = []
		for i in self.l:
			self.toPrint.append(i.value)
	
	def update(self):
		for i in self.toPrint:
			if self.t == "a":
				c = chr(int(i))
			elif self.t == "n":
				c = str(int(i))
			sys.stdout.write("{}".format(c))
			sys.stdout.flush()



class Emulator(Piece):
	def __init__(self, coords, board, instructions):
		super().__init__(coords, board)
		self.tokenSet = self.tokenize(instructions)
		self.parse()

	def tokenize(self, instructions):
		x = 0
		dirs = "EWNS"
		ops = "+=-.%"
		args = "an"
		punct = "|,"
		self.tokens = []
		while x < len(instructions):
			if instructions[x] in dirs:
				self.tokens.append(Token("D", instructions[x]))
			elif instructions[x] in ops:
				self.tokens.append(Token("O", instructions[x]))
			elif instructions[x] in args:
				self.tokens.append(Token("A", instructions[x]))
			elif instructions[x] in punct:
				self.tokens.append(Token("P", instructions[x]))
			elif instructions[x].isdigit():
				n = instructions[x]
				x += 1
				while x < len(instructions) and instructions[x].isdigit():
					n += instructions[x]
					x += 1
				self.tokens.append(Token("N", n))
			elif instructions[x] == " ":
				pass # ignore spaces
			else:
				print ("tokenize error: ")
				sys.exit(1)
			x += 1

	def parse(self):
		x = 0
		self.iSet = {}
		while x < len(self.tokens):
			if self.tokens[x].t == "O":
				if self.tokens[x].v == "=":
					self.iSet["action"] = "=="
					x += 1
					if self.tokens[x].t == "N":
						self.iSet["value"] = self.tokens[x].v
					else:
						print(self.tokens[x])
						print("parse error on conditional")
						sys.exit(1)
					x += 1
					if not self.iSet.get("False", False):
							self.iSet["False"] = []
					while x < len(self.tokens) and self.tokens[x].t == "D":
						self.iSet["False"].append(self.tokens[x].v)
						x += 1
					if self.tokens[x].t == "P" and self.tokens[x].v == "|":
						x += 1
					else:
						print("parse error on conditional")
						print (self.tokens[x])
						sys.exit(1)
					if not self.iSet.get("True", False):
							self.iSet["True"] = []
					while x < len(self.tokens) and self.tokens[x].t == "D":
						self.iSet["True"].append(self.tokens[x].v)
						x += 1
				else:
					if self.tokens[x].v == ".":
						self.tokens[x].v = "*"
					self.iSet["action"] = self.tokens[x].v# + "= 1"
					if not self.iSet.get("True", False):
							self.iSet["True"] = []
					x += 1
					while x < len(self.tokens) and self.tokens[x].t == "D":
						self.iSet["True"].append(self.tokens[x].v)
						x += 1
			x += 1

	def receive(self):
		self.listen()

	def update(self):
		for i in self.l:
			st = i.strong
			if self.iSet["action"] == "==":
				if i.strong:
					print("conditional strong")
					self.iSet["value"] = i.value
					res = "True"
				else:
					print("conditional value:",i.value, self.iSet["value"])
					res = str(i.value) == str(self.iSet["value"])
				v = i.value
			elif self.iSet["action"] == "+":
				v = i.value + 1
				res = "True"
			elif self.iSet["action"] == "-":
				v = i.value - 1
				res = "True"
			elif self.iSet["action"] == "*":
				v = i.value * 1
				res = "True"
			elif self.iSet["action"] == "%":
				if not i.strong:
					st = True
				else:
					st = False
				v = i.value
				res = "True"
				print("power:",v,st)
			else:
				print("some error")
				print(self.iSet["action"])
				sys.exit(1)
				
			for d in self.iSet[str(res)]:
					pCoords = newCoords(self.coords, d)
					self.b.particles.append(Particle(pCoords, b, d, v,st))


class Particle(Piece):
	def __init__(self, coords, board, direction, value, strong):
		super().__init__(coords, board)
		self.direction = direction
		self.value = value
		self.init = True
		self.strong = strong

	def update(self):
		if self.init:
			oldC = self.c
			self.coords = newCoords(self.coords,self.direction)
			self.c = "{},{}".format(self.coords[0],self.coords[1])
			if not self.b.d.get(self.c,False):
				self.b.d[self.c] = []
			self.b.d[self.c].append(self)
			self.b.d[oldC].remove(self)
		self.init = True
		
	def __str__(self):
		return "{}\t{}".format(str(self.coords), str(self.value))



def newCoords(old, d):
	coords = [old[0],old[1]]
	if d == "N":
		coords[1] = str(int(coords[1])+1)
	elif d == "S":
		coords[1] = str(int(coords[1])-1)
	elif d == "E":
		coords[0] = str(int(coords[0])+1)
	elif d == "W":
		coords[0] = str(int(coords[0])-1)
	else:
		pass
	return coords

if __name__ == '__main__':
	b = Board()
	with open(sys.argv[1]) as r:
		s = r.read()
	b.run(s)
	

