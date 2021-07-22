from PIL import Image, ImageDraw


class IllegalCharacter(Exception):
	pass
class NoMessage(Exception):
	pass
class ImageFull(Exception):
	pass

def turntoBinaryList(msg, encoding):
	def indexToBinary(index):
		nonlocal encoding

		bits = ""

		if encoding == 's':
			testbits = [2**x for x in range(8)]
		elif encoding == 'b':
			testbits = [2**x for x in range(6)]

		testbits.reverse()

		for testbit in testbits:
			if index-testbit >= 0:
				bits += "1"
				index -= testbit
			else:
				bits += "0"

		return bits

	def groupBinary(binary,amp):
		groups = []
		out = ""

		for index,char in enumerate(binary):
			out += char
			if index % amp == 1:
				groups.append(out)
				out = ""

		return groups


	msg = str(len(msg)) + ".hx." + msg + "."

	binaries = []

	if encoding == 's': #standard
		chars = "\n !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
	elif encoding == 'b': #barebones
		chars = " .0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


	for char in msg:
		try:
			loc = chars.index(char)
		except ValueError:
			raise IllegalCharacter

		bits = indexToBinary(loc)
		binaries.append(groupBinary(bits,2))

	return binaries
def modifyImage(imagename, binstr, encoding):

	def openImage():
		nonlocal imagename
		return Image.open(imagename)

	def toBinary(i):
		bits = ""
		testbits = [2**x for x in range(8)]

		testbits.reverse()

		for testbit in testbits:
			if i-testbit >= 0:
				bits += "1"
				i -= testbit
			else:
				bits += "0"

		return bits

	def toInt(b):
		total = 0

		testbits = [2**x for x in range(8)]
		testbits.reverse()

		for index,testbit in enumerate(testbits):
			if b[index] == '1':
				total += testbit

		return total

	img = openImage()
	width,height = img.size


	pixels = img.load()

	counter = 0

	if encoding == 's':
		for y in range(height):
			for x in range(width):
				pixel = []
				for c in range(3): #for each color
					colorval = toBinary(pixels[x,y][c])

					if counter >= len(binstr)*4:
						img.save(imagename[:imagename.index('.')] + "_steg.png")  # modifies output image name into: x.png > x_steg.png
						return True

					colorval = colorval[:-2] + binstr[counter//4%len(binstr)][counter%4]

					pixel.append(toInt(colorval))
					counter += 1

				pixels[x, y] = tuple(pixel)





	elif encoding == 'b':
		for y in range(height):
			for x in range(width):
				pixel = []
				for c in range(3):
					colorval = toBinary(pixels[x,y][c])

					if counter >= len(binstr):
						img.save(imagename[:imagename.index('.')] + "_steg.png")  # modifies output image name into: x.png > x_steg.png
						return True
					colorval = colorval[:-2] + binstr[counter][c]

					pixel.append(toInt(colorval))

				counter += 1
				pixels[x,y] = tuple(pixel)

def steganography(image,message,encoding):
	binstr = turntoBinaryList(message, encoding)
	modifyImage(image, binstr, encoding)
def readImage(imagename,encoding):

	def openImage():
		nonlocal imagename
		return Image.open(imagename).convert("RGB")

	def toBinary(i):
		bits = ""
		testbits = [2**x for x in range(8)]

		testbits.reverse()

		for testbit in testbits:
			if i-testbit >= 0:
				bits += "1"
				i -= testbit
			else:
				bits += "0"

		return bits

	def toInt(b):
		total = 0

		testbits = [2**x for x in range(8)]
		testbits.reverse()

		for index,testbit in enumerate(testbits):
			if b[index] == '1':
				total += testbit

		return total

	img = openImage()
	width,height = img.size


	pixels = img.load()

	output = ""
	byte = ""

	msglength = -1

	charsleft = -1


	if encoding == 's':
		chars = "\n !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~" # 96 indexes

		for y in range(height):
			for x in range(width):
				for c in range(3):

					byte += toBinary(pixels[x,y][c])[-2:]

					if len(byte) == 8:
						if charsleft == 0 and msglength != -1:
							return output[hxpos+4:]

						try:
							_ = toInt(byte)
							output += chars[_]
						except IndexError:
							raise NoMessage



						byte = ""
						hxpos = output.find(".hx.")

						if hxpos != -1:
							charsleft -= 1
							if msglength == -1:
								msglength = int(output[:hxpos])
								charsleft = msglength


	elif encoding == 'b':
		fail = True
		chars = " .0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" # 64 indexes
		for y in range(height):
			for x in range(width):
				byte = "00"
				for c in range(3):
					byte += toBinary(pixels[x,y][c])[-2:]

				letter = chars[toInt(byte)]

				output += letter

				if fail and letter in "0123456789":
					pass
				else:
					if letter == ".":
						fail = False
					else:
						raise NoMessage



				hxpos = output.find(".hx.")

				if charsleft == 0 and msglength != -1:
					return output[hxpos+4:-1]

				if hxpos != -1:
					charsleft -= 1
					if msglength == -1:
						msglength = int(output[:hxpos])
						charsleft = msglength


