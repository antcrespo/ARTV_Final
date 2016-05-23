from PIL import Image
import random
import sys
try:
   import cPickle as pickle
except:
   import pickle

def main():

	wordDict = {}

	outfile = sys.argv[-1]
	n = int(sys.argv[1])
	wordDict["n"] = n
	wordDict["size"] = []
	#length = len(sys.argv)
	past = []
	for i in range(0,n):
		past.append("")
	
	blank = list(past)
	for imfile in sys.argv[2:-1]:
		im = Image.open(imfile)
		wordDict["size"].append(im.size)
		pixels = list(im.getdata())
		width, height = im.size
		#pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
		past = list(blank)

		print imfile + " " + str(width) + "x" + str(height)
		for i in range(0,width*height):
			#if (i%1000 == 0):
				#print i
			cur = pixels[i]
			key = tuple(past)
			if wordDict.has_key(key):
				wordDict[key].append(cur)
			else:
				wordDict[key] = [cur]

			past.pop(0)
			past.append(cur)
	#print "Storing dictionary"
	#pickle.dump(wordDict, open(outfile, "wb"))
	
	for i in range(5):
		print "saving image " +str(i) 
		makeImage(wordDict, outfile +str(i)+".jpg")
	
def makeImage(wordDict, outfile):
	width, height = random.choice(wordDict["size"])
	n = wordDict["n"]
	past = [""]*n
	outPixels = []
	print "predicting"
	for i in range(0, height*width):
		key = tuple(past)
		if not wordDict.has_key(key):
			past = [""]*n
			key = tuple(past)
		cur = random.choice(wordDict.get(key, [(0,0,0)]))
		outPixels.append(cur)
		
		past.pop(0)
		past.append(cur)

	outImage = Image.new("RGB", (width, height))
	outImage.putdata(outPixels)
	outImage.save(outfile)

if __name__ == "__main__":
	main()
