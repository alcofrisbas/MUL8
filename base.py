import sys,time

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
				#print("collision!")
				self.b.particles.remove(i)
				self.b.d[self.c].remove(i)
				l.append(i)
		return l


class Board(object):
	def __init__(self):
		self.d = {}
		self.emitters = []
		self.particles = []
		self.enumerators = []
		self.emulators = []

class Emitter(Piece):
	def __init__(self, coords, board, direction):
		super().__init__(coords, board)
		self.direction = direction
		self.b.emitters.append(self)

	def update(self):
		l = self.listen()
		if len(l) == 0:
			pCoords = newCoords(self.coords, self.direction)
			self.b.particles.append(Particle(pCoords, b, self.direction, 0))


class Enumerator(Piece):
	def __init__(self, coords, board, t):
		super().__init__(coords, board)
		self.b.enumerators.append(self)
		self.t = t

	def update(self):
		l = self.listen()
		for i in l:
			if self.t == "a":
				c = chr(int(i.value))
			elif self.t == "n":
				c = str(i.value)
			sys.stdout.write("{}".format(c))
			sys.stdout.flush()


class Emulator(Piece):
	def __init__(self, coords, board, instructions):
		super().__init__(coords, board)
		self.b.emulators.append(self)
		self.tokenSet = self.tokenize(instructions)

	def tokenize(self, instructions):
		x = 0
		while x < len(instructions):
			c = instructions[x]
			x += 1

	def update(self):
		l = self.listen()



class Particle(Piece):
	def __init__(self, coords, board, direction, value):
		super().__init__(coords, board)
		self.direction = direction
		self.value = value
		#print (self.direction)
		#print("partcle made..")
		#print(self.coords)

	def update(self):
		#print("i am an particle!")
		oldC = self.c
		self.coords = newCoords(self.coords,self.direction)
		self.c = "{},{}".format(self.coords[0],self.coords[1])
		if not self.b.d.get(self.c,False):
			self.b.d[self.c] = []
		self.b.d[self.c].append(self)
		self.b.d[oldC].remove(self)
		#print (self.coords)



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
		pass#print("BAD")
	#print ("COOOOORDS")
	#print ("{} || {}".format(old, coords))
	return coords

if __name__ == '__main__':
	b = Board()
	e = Emitter([0,0], b, "E")
	#e1 = Emitter([0,40], b, "S")
	e2 = Enumerator([10,0], b,"n")
	#e3 = Emulator([0,2], b, "")
	while True:
		#time.sleep(0.1)
		for e in b.emitters:
			e.update()
		for e in b.enumerators:
			e.update()
		for e in b.emulators:
			e.update()
		if len(b.particles) == 0:
			break
		#print(len(b.particles))
		for e in b.particles:
			e.update()
	#e.update()
	#print (b.emitters)
	#print (b.d)