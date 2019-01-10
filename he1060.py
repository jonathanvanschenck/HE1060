import serial
from time import sleep

class HE1060:
	def __init__(self,comport="COM6"):
		self.ser = serial.Serial(comport,baudrate=38400,parity=serial.PARITY_NONE,timeout=0.5,
								  bytesize=8,stopbits=1)
		self.setDisable()#Disable the laser
		self.query("R=0.5")#Set PulsePick1 to default
		
	def close(self):
		self.ser.close()
		
	def setEnable(self):
		mes = self.query("E=1")
		sleep(3)#allow time to enable
		return mes
	def getEnable(self):
		return "enable" in self.query("E?")#self.query("E?")[:18]=="Laser is enabled\n\r"

	def setDisable(self):
		mes = self.query("E=0")
		sleep(3)#allow time to enable
		return mes
	def getDisable(self):
		return "disable" in self.query("E?")#self.query("E?")[:19]=="Laser is disabled\n\r"
		
	def getWarmUpTime(self):
		mes = self.query("O?")
		if mes[:27]!= "Laser temperature not ready":
			return 0
		return (int(mes[mes.find("=")+1:-2]))
		
	def getPowerMax(self):
		mes = self.query("S?")
		#self._pmax = int(mes[mes.find("is")+2:-2])
		return int(mes[mes.find("is")+2:-2])
	
	def getPower(self):
		mes = self.query("Q?")
		return int(mes[mes.find("=")+1:-2])
	def setPower(self,power):
		return self.query("Q="+str(power))

	def getPP(self):
		#self.getPowerMax()
		return self.getPower()/self.getPowerMax()#self._pmax
	def setPP(self,proportion):
		assert proportion>=0 and proportion<=1
		#self.getPowerMax()
		self.setPower(int(proportion*self.getPowerMax()))#self._pmax))
		
	def getRepRate(self):
		mes = self.query("Z?")
		return float(mes[mes.find("=")+1:-2])
	def setRepRate(self,reprate):
		#from 0.01 to self.query("R?") in MHz
		return self.query("Z="+str(round(reprate,2)))
	
	def query(self,message):
		self.ser.write((str(message)+"\n").encode())
		res = self.ser.read(1000).decode()
		res2 = "\n\r".join([i for i in res.split("\n\r") if i != "Command>"])
		return res2