from obj import *
if __name__ == '__main__':
	b = Board()
	E1 = Emitter([0,0], "E", b)
	en1 = Enumerator([14,0],b, "n")
	#E2 = Emitter([0,20], "S", b, out=1)
	#en2 = Enumerator([0,10],b)
	em = Emulator([10,0], b, "+ NE")
	while True:
		for e in b.emitters:
			e.update()
		for e in b.enumerators:
			e.update()
		for e in b.emulators:
			e.update()
		if len(b.particles) == 0:
			break
		for e in b.particles:
			e.update()
		print(len(b.particles))