import numpy as np 
import scipy.io.wavfile as read
import matplotlib.pyplot as plot 
import scipy.signal as signal 
import sys
import PIL.Image as convert

class apt_dec(object):
	sample_rate = 20800
	NOAA_Line_Width = 2080
	
	def __init__(self, input):
		(rate, self.inputSignal) = read.read(input)
		if rate != self.sample_rate:
			raise Exception("Resample the wave into ".format(self.sample_rate))
		#print self.inputSignal[0:10]
		input_chunk_length =len(self.inputSignal)//self.sample_rate
		input_chunk_length = int(input_chunk_length)
		NumberOfSamples =  self.sample_rate*input_chunk_length
		self.inputSignal =  self.inputSignal[:NumberOfSamples]  
		print len(self.inputSignal)
		
	def decode(self, outputFile = None):
		
		#Take the the hilber transform of the imput signal  
		hilbertTransform =  signal.hilbert(self.inputSignal)
		#filter the transfrom, remove noise 
		filteredSignal = signal.medfilt(np.abs(hilbertTransform),5)
		shapeDim = len(filteredSignal)//5
		signalReshaped = filteredSignal.reshape(shapeDim,5)
		imageSignal = signalReshaped[:,2]
		self.plot(self.inputSignal[1000:10000+1000],imageSignal[1000:10000+1000])
		scaledImageSignal = self.SignalDegitalizer(imageSignal)
		self.get_APT_format(scaledImageSignal)
		if not outputFile is None:
			image.save(outputFile)			
		return filteredSignal

	def get_APT_format(self, imageSignal):
		raws = 40
		col  = 2080
		Cycle0 = np.array((244,244,11,11), dtype = np.uint8)
		ones0 = np.ones(1, dtype = np.uint8)*11
		ones1 = np.ones(7, dtype = np.uint8)*11
		Cycle1 = np.tile(Cycle0,7)
		syncA =np.concatenate((ones0,Cycle1,ones1), axis = 0)
		scaledImageSignal = imageSignal
		number_of_lines = int(len(scaledImageSignal) / self.NOAA_Line_Width)
		imageMatrix = scaledImageSignal.reshape((number_of_lines, self.NOAA_Line_Width))
		imageMatrix = scaledImageSignal.reshape((number_of_lines, self.NOAA_Line_Width))
		image = convert.fromarray(imageMatrix)
		image.show()

		#print scaledImageSignal[1000:1400]
		#out = np.correlate(scaledImageSignal, syncA, mode = 'valid')

		#index =[i for i, j in enumerate(out) if j == 177]
		#print index[0:10]
		
		#number_of_lines = int(len(scaledImageSignal) / self.NOAA_Line_Width)
		#print len(scaledImageSignal)
		#imageMatrix = scaledImageSignal.reshape((raws,col))
		#print imageMatrix.shape

		#print  scaledImageSignal[100:200]
		
		
	
	def SignalDegitalizer(self, imageSignal, percent_low = 0.1, percent_high = 99.99):
		
		(low, high) = np.percentile(imageSignal,(percent_low,percent_high))
		difference = high - low
		signal = np.round(255*(imageSignal-low) / difference)  # all samples between 0 to 255
		signal[signal < 0] = 0    		# less 0, set to 0
		signal[signal > 255] = 255 		#scale bw 0 to 255
		return signal.astype(np.uint8)
	
	def plot(self, signal1, signal2):
		# Plots signals
		signal1 = self.SignalDegitalizer(signal1)
		NO_OF_samples = len(signal1)
		timeVector = np.linspace(0,5, NO_OF_samples) 
		plot.plot(timeVector, signal1/255)
		plot.show()
		


if __name__ == '__main__':
	apt = apt_dec(sys.argv[1])
	if len(sys.argv) > 2:
		outputFile = sys.argv[2]
	else:
		outputFile = None
		transfrom = apt.decode(outputFile)
		#apt.plot(transfrom)


