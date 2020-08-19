from pythonosc import dispatcher
from pythonosc import osc_server

import time
import board
import neopixel

#IP = "192.168.0.53"
IP = "10.0.1.5"
PORT = 5005

settings = {'auto_update': 0,
			'master_toggle': 0,
			'red_toggle': 0,
			'green_toggle': 0,
			'blue_toggle': 0,
			'lamp_toggle': 0,
			'full_toggle': 0,
			'rest_toggle': 0,
			'alarm_master_toggle': 0,
			'alarm_lights_toggle': 0,
			'alarm_sound_toggle': 0,
			'blank': 0,
			'current_preset': (0, 0)
}

curColor = {'red_Slider': 0,
			'green_Slider': 0,
			'blue_Slider': 0,
			'brightness': 0
}

conv = {1: 'alarm_master_toggle',
		2: 'alarm_sound_toggle',
		3: 'alarm_lights_toggle',
		4: 'blank',
		5: 'blank',
		6: 'blank'
}


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def rainbow_cycle(wait):
#	for j in range(255):
	for i in range(300):
		pixel_index = (i * 256 // 300)
		pixels[i] = wheel(pixel_index & 255)
	pixels.show()
	time.sleep(wait)

def updateColour(preset=()):
	# pass
	if len(preset) > 0:
		if preset == ('1', '1'):
			rainbow_cycle(0.001)
	else:
		#Lamp
		print('==========================')
		print(pixels[166:190])
		print([(curColor['red_Slider']*settings['red_toggle']*settings['master_toggle']*settings['lamp_toggle'],curColor['green_Slider']*settings['green_toggle']*settings['master_toggle']*settings['lamp_toggle'],curColor['blue_Slider']*settings['blue_toggle']*settings['master_toggle']*settings['lamp_toggle'])] * 24)
		print('==========================')

		if settings['full_toggle']:
			pixels[:297] = [(curColor['red_Slider']*settings['red_toggle']*settings['master_toggle']*settings['full_toggle'], curColor['green_Slider']*settings['green_toggle']*settings['master_toggle']*settings['full_toggle'], curColor['blue_Slider']*settings['blue_toggle']*settings['master_toggle']*settings['full_toggle'])] * 297

		if settings['lamp_toggle']:
			pixels[166:190] = [(curColor['red_Slider']*settings['red_toggle']*settings['master_toggle']*settings['lamp_toggle'],curColor['green_Slider']*settings['green_toggle']*settings['master_toggle']*settings['lamp_toggle'],curColor['blue_Slider']*settings['blue_toggle']*settings['master_toggle']*settings['lamp_toggle'])] * 24

		#all
#		pixels.fill(((curColor['red_Slider']*settings['red_toggle'])*settings['master_toggle']*settings['full_toggle'], (curColor['green_Slider']*settings['green_toggle'])*settings['master_toggle']*settings['full_toggle'], (curColor['blue_Slider']*settings['blue_toggle'])*settings['master_toggle']*settings['full_toggle']))

#		pixels.show()
		#pixels = []

		#All except lamp
		if settings['rest_toggle']:
			pixels[:165] = [(curColor['red_Slider']*settings['red_toggle']*settings['master_toggle']*settings['rest_toggle'],curColor['green_Slider']*settings['green_toggle']*settings['master_toggle']*settings['rest_toggle'],curColor['blue_Slider']*settings['blue_toggle']*settings['master_toggle']*settings['rest_toggle'])] * 165
			pixels[191:297] = [(curColor['red_Slider']*settings['red_toggle']*settings['master_toggle']*settings['rest_toggle'],curColor['green_Slider']*settings['green_toggle']*settings['master_toggle']*settings['rest_toggle'],curColor['blue_Slider']*settings['blue_toggle']*settings['master_toggle']*settings['rest_toggle'])] * 106

		pixels.brightness = curColor['brightness']
		pixels.show()



def aSettings(addr, val):
	aAddr = addr.split('/')[len(addr.split('/'))-1]
	# print(addr)
	# print(aAddr)
	settings[conv[int(aAddr)]] = int(val)
	print('alarm_master_toggle: {0}, alarm_sound_toggle: {2}, alarm_lights_toggle: {1} '.format(settings['alarm_master_toggle'], settings['alarm_lights_toggle'], settings['alarm_sound_toggle']))
	# print('addr: {0}, val: {1}'.format(addr, val))

def pButtons(addr, val):
	split_addr = addr.split('/')
	settings['current_preset'] = (split_addr[len(addr.split('/'))-1], split_addr[len(addr.split('/'))-2])
	print(settings['current_preset']) #Bottom left is (1, 1)

	#TODO: add matrix to map locations to presets
	updateColour(settings['current_preset'])


def cToggles(addr, val):
	toggleName = addr.split('/')[len(addr.split('/'))-1]
	settings[toggleName] = int(val)
	print('red_toggle: {0}, green_toggle: {1}, blue_toggle: {2}, master_toggle: {3}'.format(settings['red_toggle'], settings['green_toggle'], settings['blue_toggle'], settings['master_toggle']))
	if settings['auto_update']:
		updateColour()

def bright(addr, val):
	curColor['brightness'] = round(val,2)
	print('RED: {0}, GREEN: {1}, BLUE: {2}, BRIGHTNESS: {3}'.format(curColor['red_Slider'], curColor['green_Slider'], curColor['blue_Slider'], curColor['brightness']))
	if settings['auto_update']:
		updateColour()

def colours(addr, val):
	slide = addr.split('/')[len(addr.split('/'))-1]
	curColor[slide] = int(val)
	print('RED: {0}, GREEN: {1}, BLUE: {2}, BRIGHTNESS: {3}'.format(curColor['red_Slider'], curColor['green_Slider'], curColor['blue_Slider'], curColor['brightness']))
	if settings['auto_update']:
		updateColour()

def aSelect(addr, val):
	selector = addr.split('/')[len(addr.split('/'))-1]
	if selector == '1':
		settings['lamp_toggle'] = int(val)
	elif selector == '2':
		settings['full_toggle'] = int(val)
	elif selector == '3':
		settings['rest_toggle'] = int(val)
	print('Lamp: {0}, Full: {1}, Rest: {2}'.format(settings['lamp_toggle'], settings['full_toggle'], settings['rest_toggle']))

	if settings['auto_update']:
		updateColour()

def uMode(addr, val):
	settings['auto_update'] = int(val)

def mUpdate(addr, val):
	if not settings['auto_update']:
		updateColour()

if __name__ == "__main__":
	# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
	# NeoPixels must be connected to D10, D12, D18 or D21 to work.
	pixel_pin = board.D18
	# The number of NeoPixels
	num_pixels = 297 #300
	# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
	# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
	ORDER = neopixel.GRB
	pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, pixel_order=ORDER) #auto_write=False, 

#	pixels.brightness = 0.5
#	pixels.fill((0, 0, 255))
#	pixels.show()

        #for i in range(297):
        #pixel_index = (i * 256 // 300)
#	for i in range(166, 190):
#		#pixels[i] = wheel(pixel_index & 255)
#		pixels[i] = (0, 0, 255)
#		pixels.show()
        #time.sleep(wait)



	dispatcher = dispatcher.Dispatcher()
	dispatcher.map("/Alarm/Alarm_Settings/1/*", aSettings) #Alarm Settings
	dispatcher.map("/Presets/Preset_Buttons/*/*", pButtons) #Preset Colors
	dispatcher.map("/Custom Colors/brightness", bright) # Master Brightness
	dispatcher.map("/Custom Colors/*_Slider", colours) #Colour Amounts
	dispatcher.map("/Custom Colors/*_toggle", cToggles) #Colour Toggle Buttons
	dispatcher.map("/Custom Colors/Area_Selection/1/*", aSelect) #Area Selection
	dispatcher.map("/Custom Colors/auto_update", uMode)
	dispatcher.map("/Custom Colors/manual_update", mUpdate)

	server = osc_server.ThreadingOSCUDPServer((IP, PORT), dispatcher)
	print("Serving on {}".format(server.server_address))
	server.serve_forever()
