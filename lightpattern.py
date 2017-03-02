import math

class LightPattern:
	# Defined at the top are some necessary constants.
	# NUM_LED describes the number of LEDs we wish to control
    NUM_LED = 150
	# NUM_GROUPS describes number of buckets we use for our particular lighting scheme.
    NUM_GROUPS = 10
	# These Thresholds describe arbitrary points to change the color of the lights based on the input normalized FFT values
    THRESHOLD_GREEN = 80
    THRESHOLD_BLUE = 100
	# THRESHOLD_PURPOSE was introduced at one point, but didn't add enough visual difference to keep for our demonstration
    THRESHOLD_PURPLE = 140
	
    # mode describes the current lighting scheme for the strip, whereas we have only prepared one
    mode = None
	# group_size describes how many LEDs we consider per bucket
    group_size = None
	# lightArray is the array of color values we return to the main function to describe each light in the strip
    lightArray = []
    
	# Initialize the LightPattern object
    def __init__(self, mode):
		# Set internal mode
        self.mode = mode
		# Calculate group size based on current (and only) lighting scheme
        self.group_size = self.NUM_LED / self.NUM_GROUPS
		# Initialize all LED colors to BLACK 
        for i in range (self.NUM_LED):
			# lightArray is a structure that holds a 3-wide list for every index. Each index of these 3-wide lists indicates the brightness value for one of the RGB components for each LED
            self.lightArray.append([0, 0, 0])
    
	# Functionality to change lighting mode in case we enable more than one mode in the future
    def setMode(self, mode):
        self.mode = mode
    
	# This is called at every frame after audio analysis
    def applyConversion(self, frequencyArray, intensity):
		# Begin color analysis if our only mode is selected
        if self.mode == 1:
			# For each LED in the light strip
            for light in range(self.NUM_LED):
				# Calculate which frequency bucket the current LED is in
                group = int(math.floor(light / float(self.group_size)))
				# Calculate which LED index we're at relative to the group's start
                index = light % (self.group_size)
				# Test for the level of the frequency amplitude for the current group against the constant thresholds
                if frequencyArray[group] <= self.THRESHOLD_GREEN:
					# Amplitude is too low, so set red. The brightness of the red LED is dependant on the overall system audio intensity (for all frequencies)
                    self.lightArray[(group * self.group_size) + index] = [0, intensity, 0] # Red LED
                elif frequencyArray[group] <= self.THRESHOLD_BLUE:
					# Amplitude is somewhere in the middle, so set green with the brightness dependant on system audio intensity
                    self.lightArray[(group * self.group_size) + index] = [intensity, 0, 0] # Green LED
                else:
					# Amplitude is high, so set Blue and have brightness depend on system audio intensity
                    self.lightArray[(group * self.group_size) + index] = [0, 0, intensity] # Blue LED
		# Return the completed LED color/brightness snapshot for this frame
        return self.lightArray
