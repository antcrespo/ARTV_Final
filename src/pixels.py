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

		print "total is " + str(width*height)
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
	print "Storing dictionary"
	pickle.dump(wordDict, open(outfile, "wb"))

if __name__ == "__main__":
	main()
