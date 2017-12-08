#!/usr/bin/python
import pyaudio
import audioop
import sys
import timeit
import numpy
import wave
import os
import struct
import math
from time import sleep
# Import our custom lightpattern object
from lightpattern import LightPattern as lp
#from neopixel import *

class raspberryjam:
    LED_COUNT   = 150       # Number of LED pixels in the strip
    LED_PIN     = 18        # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800khz)
    LED_DMA     = 5         # DMA channel to use for generating signal (try 5)
    LED_INVERT  = False     # True to invert the signal (when using NPN transistor level shift)
    CHUNK_SIZE  = 1024      # Audio Data Chunk Size. Change if too fast/slow, never less than 1024
    BUFFER_SIZE = 10        # Size of the light delay buffer
    strip = None            # Reference to the led strip
    stream = None           # Reference to input audio stream
    device = None           # Reference to our chosen audio input device 
    p = None                # Reference to PyAudio object
    DELAY = 0               # Delay
    # Buffer object to combat Bluetooth audio lag for the system audio intensity variable
    buffVOL = [0] * BUFFER_SIZE
    # Buffer object to combat Bluetooth audio lag for the FFT analysis array variables
    buffFFT = [[0] * 10] * BUFFER_SIZE
    # Class wide object to hold our custom default pattern
    patternDefault = None
    start = 0               # Start time
    stop = 0                 # Stop time
    #  list_devices uses PyAudio to list all system audio devices and allows the user to choose one for audio analysis. We use the device labeled 'pulse'
    def list_devices(self):
        # Create a PyAudio instance object and store it in the class field
        self.p = pyaudio.PyAudio()
        # Create our pattern instance and store it in the class field
        self.patternDefault = lp(1)
        i = 0
        n = self.p.get_device_count()
        # Print out all available audio devices with registered channels (no null devices)
        while i < n:
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                print str(i) + '. ' + dev['name']
            i += 1
        # Quickly written device chooser that allows flexibility for when the number of audio devices in the machine changes and the pulse object changes index
        print 'Please enter which audio device to read from'
        self.device = int(raw_input(">> "))
    
    # Initialize our control script, including LED strip and audio stream
    def initialize(self):
        start = timeit.default_timer()
        self.p = pyaudio.PyAudio()
        self.patternDefault = lp(1)
        # Create an instance of a virtual light strip with the constant parameters from the top of this program
        audio_file = wave.open("christmas.wav", 'rb')
        rate = audio_file.getframerate()
        self.DELAY =  float(self.CHUNK_SIZE)/rate
        
       # self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT)
        # begin() must be called on the LED strip for it to start accepting any LED inputs
        #self.strip.begin()
        # Initialize auto stream pulling, specifying rate and chunk size. We didn't play around too much with the default values for the sake of not breaking things. Chunk size was doubled.
        print "Initializing Stream ------------\n"
        self.stream = self.p.open(format = pyaudio.paInt16,
                        channels = 1,
                        rate = 44100,
                        output = True,
                        frames_per_buffer = self.CHUNK_SIZE
                        )
        print "\n--------------------------------"
        print "Beginning audio read and LED write, use Ctrl+C to stop"
        # Begin core LED control and audio reading loop. May throw error, so we need to clean up afterwards.
        try:
            data = audio_file.readframes(self.CHUNK_SIZE)
            while True:
                # Read the current chunk off of the audio stream
                
                # Find the RMS value of the audio stream, indicative of the overall 'intensity' value of the current chunk. This is later passed to the pattern object
                #rms = audioop.rms(data, 2)
                # Normalize the RMS value to between 0 and 255. Used to directly control the LED brightness.
                #normalized = max(min(rms / (2.0 ** 14), 1.0), 0.0) # Have confidence the value is normalized between 0 and 1
                #normalized = int((normalized ** 1.8) * 255)
                #print normalized
                
                # The following is the routine we follow to gather useful semi-normalized FFT values. While the general gist is obvious from the output of these function calls, the specifics
                # regarding each step is still a little confusing to us and was a subject to some experimentation. We altered the formula from 6 buckets to 10
                
                # Set format to C unsigned int
                fmt = "%dH"%(2*self.CHUNK_SIZE)
                # Unpack the binary data into given format
                data2 = struct.unpack(fmt, data)
                # Split data string into array of unsigned integers 
                data2 = numpy.array(data2, dtype = 'h') 

                # Perform Fourier Transform; returns complex numbers
                fourier = numpy.fft.fft(data2)
		
                # Get real values of positive frequencies of fourier transform and convert to KHz
                # See https://docs.scipy.org/doc/numpy-1.13.0/reference/routines.fft.html#implementation-details 
                ffty = numpy.abs(fourier[0:len(fourier)/2])
                 
                
                # Splice the positive frequencies into two equally sizes arrays
                ffty1 = ffty[:len(ffty) / 2]
                ffty2 = ffty[len(ffty) / 2::] + 2
                # Reverse the second half of the sequence
                ffty2 = ffty2[::-1]
                # Add them together
                ffty = ffty1 + ffty2
                
                # Take natural log
                ffty = numpy.log(ffty) - 2
                fourier = list(ffty)[5:-4]
                fourier = fourier[:len(fourier) / 2]
                
                # Determine level of intensity (0 - 255)
                size = len(fourier)
	        # Divide the frequencies into 10 buckets
                levels = [sum(fourier[i:(i+size / 150)]) for i in xrange(0, size, size / 150)][:150]
                for i in range(0, len(levels)):
                    levels[i] = max(min(int(levels[i]*17), 255), 0)
               # print levels
                #
                
                # Call our pattern object that accepts the normalized system volume intensity and the semi-normalized frequency bucket intensity. The buffer is used here to delay the lights in attempt to sync with the music
         #       outLightArray = self.patternDefault.applyConversion(self.buffFFT.pop(-1), self.buffVOL.pop(-1))
                # Using the obtained array object, set each LED on the light to it's corresponding values
           #     for i in range(self.LED_COUNT):
          #          self.strip.setPixelColor(i, Color(outLightArray[i][0], outLightArray[i][1], outLightArray[i][2]))
                # Refresh the light strip to change the color of each LED at once
            #    self.strip.show()
                # Store the values for the song calculated on this frame, to be displayed at a later frame
            #    self.buffFFT.append(levels)
             #   self.buffVOL.append(normalized)
                #self.stream.write(data)
                sleep(self.DELAY)
                data = audio_file.readframes(self.CHUNK_SIZE)
        # When we want to stop the program, facilitate using Ctrl+C
        except KeyboardInterrupt:
            pass
        finally:
            audio_file.close()
            # Clean up the audio and light output streams to make sure no resources leak
            print "\nStopping"
            self.stream.close()
            stop = timeit.default_timer()
            print 'Total runtime: ' + str(stop-start)
            self.p.terminate()
            
        
if __name__ == '__main__':
    # We played around with nice levels. Changing the nice level to something lower did not assist in performance, but actually hindered bluetooth performance
    os.nice(0)
    # Create an instance of the object represented by our control strip
    rj = raspberryjam()
    # Initialize the script and list current audio devices to control the lights from
    # rj.list_devices()
    # Begin loop that reads from the audio stream and controls the lights
    rj.initialize()
