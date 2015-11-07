import math

def dist(p1, p2):
	v = (p1[0]-p2[0], p1[1]-p2[1])

	l = math.sqrt(sum([a*a for a in v]))
	return l

def normalize(v, thresold=0.0001):
	# normalize vector v

	l = math.sqrt(sum([a*a for a in v]))

	if l <= thresold:
		return (0,0)

	v = tuple([a/l for a in v])

	return v

def getToroidalLocationList(v):
	L = []
	L.append((v[0]-1, v[1]-1))
	L.append((v[0]-1, v[1]))
	L.append((v[0]-1, v[1]+1))

	L.append((v[0], v[1]-1))
	L.append((v[0], v[1]))
	L.append((v[0], v[1]+1))

	L.append((v[0]+1, v[1]-1))
	L.append((v[0]+1, v[1]))
	L.append((v[0]+1, v[1]+1))

	return L

def getMinDist(p, L):
	# p: single point
	# L: list of points

	minDist = min([dist(p, l) for l in L])

	return minDist

def getNearestLocation(p, L):
	# p: single point
	# L: list of points

	dL = [dist(p, l) for l in L]
	minDist = min(dL)

	return L[dL.index(minDist)]

def clampCoords(p):
	newX = p[0]
	if newX > 1:
		newX = newX-1.0
	elif newX < 0:
		newX = newX+1.0

	newY = p[1]
	if newY > 1:
		newY = newY-1.0
	elif newY < 0:
		newY = newY+1.0

	return (newX, newY)




