from PIL import Image
import random

def main():
	imfile = "test.jpg"
	im = Image.open(imfile)

	pixels = list(im.getdata())
	width, height = im.size
	pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
	outPixels = []

	print "pixels: " + str(width*height)
	for x in range(0, height):
		wordDict = {}
		wordCount = {}
		pixel1 = ""
		pixel2 = ""
		for i in range(0,width):
			pixel3 = pixels[x][i]
			if wordDict.has_key((pixel1 , pixel2)):
				if pixel3 in wordDict[(pixel1 , pixel2)]:
					wordCount[(pixel1 , pixel2, pixel3)] += 1
					wordDict[(pixel1 , pixel2)].append(pixel3)
				else:
					wordDict[(pixel1 , pixel2)].append(pixel3)
					wordCount[(pixel1 , pixel2, pixel3)] = 1
			else:
				wordDict[(pixel1 , pixel2)] = [pixel3]
				wordCount[(pixel1 , pixel2, pixel3)] = 1
			#print (pixel1,pixel2,pixel3)
			pixel1 = pixel2
			pixel2 = pixel3
	
		pixel1 = ""
		pixel2 = ""
		for i in range(0, width):
			if wordDict.has_key((pixel1 , pixel2)):
				pixel3 = random.choice(wordDict[(pixel1,pixel2)])
			else:
				pixel3 = (pixels[x][0])
			outPixels.append(pixel3)
		
			pixel1 = pixel2
			pixel2 = pixel3
	
	outImage = Image.new(im.mode, im.size)
	outImage.putdata(outPixels)
	outImage.save("test_out.png")
if __name__ == "__main__":
	main()
