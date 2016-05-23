from PIL import Image
import random
import sys

wordDict = {}
wordCount = {}
	
def flatPrediction(array):
    val1 = ""
    val2 = ""
    length = len(array)
    #print "total is " + str(length)
    for i in range(0,length):
	    val3 = array[i]
	
	    if wordDict.has_key((val1 , val2)):
		    if val3 in wordDict[(val1 , val2)]:
			    wordCount[(val1 , val2, val3)] += 1
			    wordDict[(val1 , val2)].append(val3)
		    else:
			    wordDict[(val1 , val2)].append(val3)
			    wordCount[(val1 , val2, val3)] = 1
	    else:
		    wordDict[(val1 , val2)] = [val3]
		    wordCount[(val1 , val2, val3)] = 1
		
	    val1 = val2
	    val2 = val3
	
def linePrediction (array, width, height) :
    array = [array[i * width:(i + 1) * width] for i in xrange(height)]
    for sub in array:
        flatPrediction(sub)
            
def main():
	
    outfile = sys.argv[-1]
    for imfile in sys.argv[1:-1]:
        im = Image.open(imfile)

        pixels = list(im.getdata())
        width, height = im.size
        #flatPrediction(pixels)
        linePrediction(pixels, width, height)

    out = []
    #flatOut(out, width*height)
    lineOut(out, width, height)
    outImage = Image.new(im.mode, im.size)
    outImage.putdata(out)
    outImage.save(outfile)


def flatOut(outPixels, count):
    pixel1 = ""
    pixel2 = ""

    for i in range(0, count):
        if wordDict.has_key((pixel1 , pixel2)):
	        pixel3 = random.choice(wordDict[(pixel1,pixel2)])
        else:
	        pixel3 = (pixels[0])
	        print "bad"
        outPixels.append(pixel3)

        pixel1 = pixel2
        pixel2 = pixel3
	
def lineOut(outPixels, width, height):
    for i in range(0,height):
        flatOut(outPixels, width)
	
if __name__ == "__main__":
	main()
