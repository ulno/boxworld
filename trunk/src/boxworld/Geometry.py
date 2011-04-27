
class Dimensions:
	
	def __init__(self, x, y, z):
		
		assert x >= 0
		assert y >= 0
		assert z >= 0
		
		self.x = x
		self.y = y
		self.z = z

	def volume(self):
		return self.x * self.y * self.z

	def __eq__(self,other):
		return self.x == other.x and self.y == other.y and self.z == other.z

	def __str__(self):    
		return "[x=%d y=%d z=%d]" % (self.x, self.y, self.z)

class Coord:
	
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		
	def surroundingCoords(self):
		
		return (Coord(self.x-1, self.y, self.z),
				Coord(self.x+1, self.y, self.z),
				Coord(self.x, self.y-1, self.z),
				Coord(self.x, self.y+1, self.z),
				Coord(self.x, self.y, self.z-1),
				Coord(self.x, self.y, self.z+1))
	
	def __str__(self):
		return "[x=%d y=%d z=%d]" % (self.x, self.y, self.z)
	
	def __eq__(self,other):
		return self.x == other.x and self.y == other.y and self.z == other.z
	
	def __hash__(self):
		return self.x ^ self.y ^ self.z
	
class Segment:
    '''
    Represents the location and of a world segment. 
    Defined by two nonequal points. Contains all points between
    the definition points, inclusive.
    '''
    
    def __init__(self, startCoord, endCoord):
        '''
        for all values V in endCoord, endCoord.V MUST BE >= startCoord.V
        '''
        self.startCoord = startCoord
        self.endCoord = endCoord
        
        assert (endCoord.x >= startCoord.x), "Coord %s not >= %s" % (endCoord, startCoord)
        assert (endCoord.y >= startCoord.y), "Coord %s not >= %s" % (endCoord, startCoord)
        assert (endCoord.z >= startCoord.z), "Coord %s not >= %s" % (endCoord, startCoord)
    
    def dimensions(self):
    	
    	# +1 for dimension difference, as coordinates are inclusive
    	return Dimensions(self.endCoord.x - self.startCoord.x + 1,
						  self.endCoord.y - self.startCoord.y + 1,
						  self.endCoord.z - self.startCoord.z + 1)
    
    def volume(self):
    	return self.dimensions().volume()
    
    def __str__(self):
        return "[ %s %s ]" % (self.startCoord, self.endCoord)
        
    def contains(self, coord):
        return self.startCoord.x <= coord.x and \
               self.startCoord.y <= coord.y and \
               self.startCoord.z <= coord.z and \
               self.endCoord.x >= coord.x and \
               self.endCoord.y >= coord.y and \
               self.endCoord.z >= coord.z
               
    def coorditer(self):
        for x in range(self.startCoord.x, self.endCoord.x+1):
            for y in range(self.startCoord.y, self.endCoord.y+1):
                for z in range(self.startCoord.z, self.endCoord.z+1):
                    yield Coord(x, y, z)
                    
    def vtkCoordIter(self):
    	for z in range(self.startCoord.z, self.endCoord.z+1):
    		for y in range(self.startCoord.y, self.endCoord.y+1):
    			for x in range(self.startCoord.x, self.endCoord.x+1):
    				yield Coord(x, y, z)
    			
		
