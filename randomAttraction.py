import random
import sys
import threading
from Tkinter import *

#sys.path.insert(0, '/home/tanner/Dropbox/sandbox/GraphicsTools/')
import graphicsTools as g

from calculations import *

DELTA_T = 0.001

class Person:
	# radius
	r=8

	lineWidth=2
	lineDist=0.5
	switchProb=0.001 # probability of switching attractors in a frame

	pinColour = (0.5, 0.0, 0.0)

	root=[]
	canvas=[]

	drawLine=True

	def __init__(self, index, root, canvas, fixed=False):
		# location in [0,1]x[0,1] square
		self.loc=(random.random(), random.random())
		self.pixLoc=(0,0)

		# attractor (reference to whole person class instance)
		self.attractor=[]

		self.colour=normalize((random.random(), random.random(), random.random()))

		self.index=index

		self.root=root
		self.canvas=canvas

		self.pinned=False # for people who are pinned
		self.fixed=False # to indicate a fixed point

		if fixed:
			self.r = 3
			self.colour = (0.15,0.15,0.15)
			self.drawLine=False
			self.fixed=True


	def setAttractor(self, attractor):

		self.attractor = attractor

	def initDrawing(self):
		canvasW=self.root.winfo_width()
		canvasH=self.root.winfo_height()

		r = self.r
		# center of circle
		x = int(1.0*canvasW*self.loc[0])
		y = int(1.0*canvasH*self.loc[1])

		self.pixLoc=(x,y)



		if self.drawLine and self.attractor!=[]:
			attractorCoords = self.attractor.canvasCoords()
			l2x = ((1.0-self.lineDist)*x + self.lineDist*attractorCoords[0])
			l2y = ((1.0-self.lineDist)*y + self.lineDist*attractorCoords[1])
			lColour = g.toHex(tuple([v*0.3+0.0 for v in self.colour]))
			l = self.canvas.create_line(x, y, l2x, l2y, fill=lColour, activefill="white", width=self.lineWidth)
			self.canvasLineIndex=l


		x0p, y0p = x-r, y-r
		x1p, y1p = x+r, y+r

		fill, outline = g.toHex(self.colour), "black"
		p = self.canvas.create_oval(x0p, y0p, x1p, y1p, fill=fill, outline=outline, activeoutline="white")
		self.canvasIndex=p

		

		if not self.fixed:
			self.canvas.tag_bind(self.canvasIndex, '<ButtonPress-1>', self.togglePinned) 

	def togglePinned(self, event=[]):
		#print "here"
		self.pinned = not self.pinned
		if self.pinned:
			self.canvas.itemconfig(self.canvasIndex, fill=g.toHex(self.pinColour))
		else:
			self.canvas.itemconfig(self.canvasIndex, fill=g.toHex(self.colour))

	def rescale(self):
		canvasW=self.root.winfo_width()
		canvasH=self.root.winfo_height()

		x = int(1.0*canvasW*self.loc[0])
		y = int(1.0*canvasH*self.loc[1])

		# move the circle
		x0p, y0p = self.loc[0]*canvasW, self.loc[1]*canvasH

		curLoc = self.pixLoc
		diff = (int(x0p-curLoc[0]), int(y0p - curLoc[1]))

		self.canvas.move(self.canvasIndex, diff[0], diff[1])

		self.pixLoc = (self.pixLoc[0]+diff[0], self.pixLoc[1]+diff[1])

		if self.drawLine and self.attractor!=[]:
			# move the line
			attractorCoords = self.toCanvasCoords(self.nearestLocation(self.attractor))
			l2x = ((1.0-self.lineDist)*x + self.lineDist*attractorCoords[0])
			l2y = ((1.0-self.lineDist)*y + self.lineDist*attractorCoords[1])
			self.canvas.coords(self.canvasLineIndex, x, y, l2x, l2y)

			length = dist(self.loc, (1.0*l2x/canvasW, 1.0*l2y/canvasH))
			width = int(max(min(1./length,5), 1))
			self.canvas.itemconfig(self.canvasLineIndex, width=width)

	def moveBy(self, (x, y)):
		#newX = max(min(self.loc[0]+x, 1), 0)
		#newY = max(min(self.loc[1]+y, 1), 0)
		
		self.loc = clampCoords((self.loc[0]+x, self.loc[1]+y))

		self.rescale()

	def moveTo(self, (x, y)):
		self.moveBy((x - self.loc[0], y - self.loc[1]))

	def distanceTo(self, p):
		# distance to other person
		#v = (self.loc[0]-p.loc[0], self.loc[1]-p.loc[1])

		#l = math.sqrt(sum([a*a for a in v]))

		L = getToroidalLocationList(p.loc)

		minL = getMinDist(self.loc, L)

		return minL

	def nearestLocation(self, p):
		# find nearest toroidal location of p

		L = getToroidalLocationList(p.loc)

		return getNearestLocation(self.loc, L)

	def canvasCoords(self):
		canvasW=self.root.winfo_width()
		canvasH=self.root.winfo_height()

		x, y = self.loc[0]*canvasW, self.loc[1]*canvasH

		return (x, y)

	def toCanvasCoords(self, (x,y)):
		canvasW=self.root.winfo_width()
		canvasH=self.root.winfo_height()

		return (x*canvasW, y*canvasH)

	def flash(self, stage=0):

		if stage==0:
			self.canvas.itemconfig(self.canvasIndex, fill=g.toHex((1,1,1)))
		elif stage==1:
			self.canvas.itemconfig(self.canvasIndex, fill=g.toHex((0,0,0)))
		elif stage==2:
			self.canvas.itemconfig(self.canvasIndex, fill=g.toHex((1,1,1)))
		else:
			if not self.pinned:
				self.canvas.itemconfig(self.canvasIndex, fill=g.toHex(self.colour))
			else:
				self.canvas.itemconfig(self.canvasIndex, fill=g.toHex(self.pinColour))

		self.root.update()

		if stage <= 2:
			t = threading.Timer(0.1, self.flash, [stage+1])
			t.daemon = True
			t.start()

	def setOutlineColour(self, colour):
		self.canvas.itemconfig(self.canvasIndex, outline=g.toHex(colour))

	def setFillolour(self, colour):
		self.canvas.itemconfig(self.canvasIndex, fill=g.toHex(colour))

class People:

	speed=1.0/300
	totalShift=(0,0)

	switchEnabled = True

	def __init__(self, n, root, canvas):
		# create population
		self.people=[]

		self.root=root
		self.canvas=canvas

		self.initFixedPoints()

		for i in range(0, n):
			self.people.append(Person(index=i, root=root, canvas=canvas))

		# set their attractors
		for p in self.people:
			p.setAttractor(self.getRandomPerson(ignore=[p.index]))

		
			#print locs[i]
		
	def initFixedPoints(self):
		self.fixedPoints = []
		locs = []
		res=10
		for i in range(0, res):
			for j in range(0, res):
				locs.append((1.0*i/res, 1.0*j/res))

		for i in range(0, len(locs)):
			self.fixedPoints.append(Person(index=-1, root=self.root, canvas=self.canvas, fixed=True))
			self.fixedPoints[i].loc = locs[i]

	def step(self):
		global DELTA_T

		if len(self.people) <= 1: return

		# small probability of any person switching attractors (per second)
		if self.switchEnabled:
			for p in self.people:
				if random.random() <= p.switchProb:# and random.random() <= DELTA_T:
					p.setAttractor(self.getRandomPerson(ignore=[p.index]))
					p.flash()
		
		# move everyone closer to their attractor
		for p in self.people:
			if p.pinned: continue

			# caluclate vector away from rest of people
			weightSum=0
			dirSum=(0,0)
			for q in self.people:
				if q==p:
					continue

				qLoc = p.nearestLocation(q)

				# inverse distance weighting
				qDist=p.distanceTo(q)
				# normalize the distance to [0,1]
				qDist = qDist/(math.sqrt(2.0)/2.0)

				qDir = (qLoc[0]-p.loc[0], qLoc[1]-p.loc[1])

				weight = 0
				dS = qDist*qDist
				if q == p.attractor:
					weight = 100*1.0/(max(0.00001, 1.0 - dS))
					dirSum = (dirSum[0] + qDir[0]*weight, dirSum[1] + qDir[1]*weight)
					weightSum += weight
				else:
					weight = 1.0/(max(0.00001, dS))
					dirSum = (dirSum[0] - qDir[0]*weight, dirSum[1] - qDir[1]*weight)

				weightSum += weight
				
			avgDir = (dirSum[0]/weightSum, dirSum[1]/weightSum)
			#avgDir = normalize(avgDir)
			avgDir = (avgDir[0]*len(self.people), avgDir[1]*len(self.people))

			diff = (avgDir[0]*self.speed, avgDir[1]*self.speed)

			p.moveBy(diff)

		return

	def toggleSwitching(self, event=[]):
		self.switchEnabled = not self.switchEnabled

		if self.switchEnabled:
			for p in self.people:
				# make their outline black
				p.setOutlineColour((0,0,0))
		else:
			for p in self.people:
				# make their outline black
				p.setOutlineColour((0.5,0,0))

		#print "here"

	def getRandomPerson(self, ignore=[]):
		if len(self.people) <= 1:
			return []

		A = range(0, len(self.people))
		for e in ignore:
			try:
				A.remove(e)
			except:
				print "Error"
				pass
		return self.people[A[random.randint(0, len(A)-1)]]

	def initDrawing(self):

		self.canvas.bind("<ButtonPress-3>", self.toggleSwitching)

		self.canvas.delete("all")

		for p in self.fixedPoints:
			p.initDrawing()

		if len(self.people)==0:
			return

		#for i in range(len(self.people)):
		#	self.people[i].initDrawing(tk_root, tk_canvas)
		for p in self.people:
			p.initDrawing()

	def resizeLayout(self):
		pixelX=self.root.winfo_width()
		pixelY=self.root.winfo_height()

		canvasW = pixelX
		canvasH = pixelY-0

		for p in self.people:
			p.rescale()

		for p in self.fixedPoints:
			p.rescale()
	
	def shiftAll(self):
		# set center of mass to be at the center of the screen
		weightSum=0
		vecSum=(0,0)

		shiftFactor = 0.05
		
		for q in self.people:
			vecSum = (vecSum[0]+q.loc[0], vecSum[1]+q.loc[1])

		avgLoc = (vecSum[0]/len(self.people), vecSum[1]/len(self.people))

		#print avgLoc

		center = (0.5, 0.5)

		diff = (center[0]-avgLoc[0], center[1]-avgLoc[1])

		shift = (shiftFactor*diff[0], shiftFactor*diff[1])

		self.totalShift = (self.totalShift[0] + shift[0], self.totalShift[1] + shift[1])


		for p in self.fixedPoints:
			p.moveBy(shift)
		

		# now shift everyone over
		for p in self.people:
			p.moveBy(shift)
	
def setBinds():

	tk_root.bind("<Configure>", resizeLayout)

def resizeLayout(event=[]):
	pixelX=tk_root.winfo_width()
	pixelY=tk_root.winfo_height()

	canvasW = pixelX
	canvasH = pixelY-0

	tk_canvas.place(x=0, y=0, width=canvasW, height=canvasH)

	Population.resizeLayout()

def graphicsInit():
	tk_root.title("Random Attraction")
	tk_root.configure(background="black")

	defW, defH = 500, 500

	tk_root.geometry("%dx%d%+d%+d" % (defW, defH, g.WIDTH/2 - defW/2, g.HEIGHT/2-defH/2))

	tk_canvas.configure(bd=0, highlightthickness=0, bg="black")

	tk_root.update()

def animate():
	global DELTA_T

	Population.step()
	Population.shiftAll()

	t = threading.Timer(DELTA_T, animate)
	t.daemon = True
	t.start()

if __name__ == "__main__":

	tk_root = Tk()

	tk_canvas = Canvas(tk_root)


	graphicsInit()

	# create population
	Population=People(n=8, root=tk_root, canvas=tk_canvas)

	Population.initDrawing()

	resizeLayout()
	
	setBinds()

	animate()

	tk_root.mainloop()
