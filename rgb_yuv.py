#import ffmpeg
import os,sys
sys.path.insert(0, '../')
import numpy as np

def rgb_yuv(a,b,c,TO_YUV = True):
	if TO_YUV == True:
		R = 0.257 * a + 0.504 * b + 0.098 * c + 16
		G = -0.148 * a -0.291 * b + 0.439 * c + 128
		B = (0.439 * a) + (-0.368 * b) + (-0.071 * c) + 128
		return R,G,B
	else:
		Y = (a - 16)
		U = (b - 128)
		V = (c - 128)
		a = 1.164 * Y + 1.596 * V
		b = 1.164 * Y - 0.813 * V - 0.391 * U
		c = 1.164 * Y + 2.018 * U
		return a,b,c

def run_length_encoding(bits):
	result = []
	diffZero = True
	for bit in range(len(bits)):
		if int(bits[bit]) == 0 and diffZero == True:
			zerosBehind = 0
			for number in bits[bit:]:		
				if int(number) == 0:
					zerosBehind += 1
				else:
					break
			result.append(0)
			result.append(zerosBehind)
			diffZero = False
		if int(bits[bit]) != 0:
			#print(bits[bit])
			diffZero = True
			result.append(bits[bit])
	return result
	

def dct(n):
	N = len(n)
	matrix = np.zeros((N,N))
	for i in range(N):
		alpha = np.sqrt(2/N)
		if i == 0:
			alpha = np.sqrt(1/N)
		for j in range(N):
			matrix[i,j] = alpha * np.cos(( (2*j+1) * i * np.pi ) / (2*N) )
	transposedN = np.array([n]).T
	result = matrix @ transposedN
	return result
		
def idct(n,decode = True):
	N = len(n)
	matrix = np.zeros((N,N))
	for i in range(N):
		alpha = np.sqrt(2/N)
		if i == 0:
			alpha = np.sqrt(1/N)
		for j in range(N):
			matrix[i,j] = alpha * np.cos(( (2*j+1) * i * np.pi ) / (2*N) )
	transposedN = np.array([n]).T
	result_dct = matrix @ transposedN
	inverted_matrix = np.linalg.inv(matrix)
	return inverted_matrix @ result_dct
	
def resize_image():
	image = input("write the name of the image to resize with the extension:\n")
	os.system("ffmpeg -i "+ image +" -vf scale=320:240 output_320x240.png")
def imate_to_bw():
	image = input("write the name of the image to grayscale with the extension:\n")
	os.system("ffmpeg -i "+ image +" -vf format=gray outputBW.jpg")
def compress_image():
	image = input("write the name of the image to grayscale with the extension:\n")
	compression_level = input("give an input level 0-100 where 0 is the minimum compression\n")
	os.system("ffmpeg -i "+ image +" Lory_compressed.jpg -compression_level " + compression_level)
def main():
	exit = False
	while exit == False:
		option = input("choose the exercise you want to do execute:\n1\n2\n3\n4\nAny other key to exit\n")
		if option == "1":
			rgb_or_yuv = input("do you want to turn values to RGB or to YUV? (r/y)")
			if rgb_or_yuv == "r":
				rgb_or_yuv = False
				a = int(input("Y:"))
				b = int(input("U:"))
				c = int(input("V:"))
			elif rgb_or_yuv == "y":
				rgb_or_yuv = True
				a = int(input("R:"))
				b = int(input("G:"))
				c = int(input("B:"))
			else:
				print("invalid value")
				continue
			print(rgb_yuv(a,b,c,TO_YUV = True))
		elif option == "2":
			print("running run length encoding to the bit string: 000200005997654567800890")
			print(run_length_encoding('000200005997654567800890'))
		elif option == "3":
			arrayForDCT =[1,2,3,4,5,6,7,8]
			print("running dct to: ", arrayForDCT)
			x = dct(np.array(arrayForDCT))
			print("running idct to the result: ",x)
			print(idct(arrayForDCT))
		elif option == "4":
			suboption = input("1-resize an image\n2-turn image to grayscale\n3-compress an image\n")
			if suboption == "1":
				resize_image()
			elif suboption == "2":
				imate_to_bw()
			elif suboption == "3":
				compress_image()
			
		else:
			exit = True
if __name__ == "__main__":

	main()

