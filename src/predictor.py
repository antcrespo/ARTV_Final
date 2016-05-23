from PIL import Image
import random
import sys
try:
   import cPickle as pickle
except:
   import pickle

def main():
	wordDict = pickle.load(open(sys.argv[1], "rb"))
	outfile = sys.argv[2]
	width, height = random.choice(wordDict["size"])
	n = wordDict["n"]
	past = [""]*n
	outPixels = []
	for i in range(0, height*width):
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