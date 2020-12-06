#import adafruit_motor.servo
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685

# Initialize I2C connection
i2c_bus = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c_bus)

# Define PWM frequency
pca.frequency = 50

# Create servo child class, inheriting from the ServoKit class as parent
class i2cServo(ServoKit):
	def __init__(self, channel, defaultAngle=90, dutyCycle=0x7FFF, lowerLim=0, upperLim=180):
		super().__init__(channels=16)

		self.channel = channel
		self.pcaCh = pca.channels[channel]
		self.defaultAngle = defaultAngle
		self.currentAngle = defaultAngle
		self.dutyCycle = dutyCycle
		self.lowerLim = lowerLim
		self.upperLim = upperLim

		self.resetMe()


	def resetMe(self):
		super().servo[self.channel].angle = self.defaultAngle


	def moveCW(self, angleStep=5):
		self.currentAngle = self.currentAngle - angleStep

		if self.currentAngle <= self.lowerLim:
			self.currentAngle = self.currentAngle + angleStep
		else:
			super().servo[self.channel].angle = self.currentAngle


	def moveCCW(self, angleStep=5):
		self.currentAngle = self.currentAngle + angleStep

		if self.currentAngle >= self.upperLim:
			self.currentAngle = self.currentAngle - angleStep
		else:
			super().servo[self.channel].angle = self.currentAngle
