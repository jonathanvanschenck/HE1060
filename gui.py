import tkinter
import he1060

class App(tkinter.Frame):
    def __init__(self,master=None):
        tkinter.Frame.__init__(self,master)
        self.grid(row=0)
        self.createWidgets()
        self.enableStatue = False
        self.connectStatue = False
        self.he = None
        
    def createWidgets(self):
        #Setup connect
        self.comCont = tkinter.LabelFrame(self,text="COM Port")
        self.comCont.grid(row=0,column=0)
        self.comLabel = tkinter.Entry(self.comCont)
        self.comLabel.insert(tkinter.END,"COM6")
        self.comLabel.grid(row=0,column=0)
        self.comLabel.configure(state="normal")
        self.connectButton = tkinter.Button(self.comCont,text="",command=self.connect)
        self.connectButton.grid(row=1,column=0)
        self.connectButton.configure(background="Grey",text="Connect Laser")
        #Setup RepRate Selection
        self.RRCont = tkinter.LabelFrame(self,text="Repetition Rate")
        self.RRCont.grid(row=0,column=1,stick=tkinter.W)
        self.rr = tkinter.DoubleVar()
        self.rr.set(0.5)
        self.reprates = [0.5,0.25,0.1,0.02,0.01]
        self.RRCheck = len(self.reprates)*[None]
        for i in range(len(self.reprates)):
            self.RRCheck[i] = tkinter.Radiobutton(self.RRCont,text = str(self.reprates[i])+" MHz",value=self.reprates[i],variable=self.rr,command=self.setRR)
            self.RRCheck[i].grid(row=i)
            self.RRCheck[i].configure(state="disabled")
        #Setup Power Selection
        self.PowerCont = tkinter.LabelFrame(self,text="Laser Power")
        self.PowerCont.grid(row=0,column=2,stick=tkinter.W)
        self.enableButton = tkinter.Button(self.PowerCont,text="",command=self.enable)
        self.enableButton.grid(row=0,column=0)
        self.enableButton.configure(background="Brown",text="Enable Laser")
        self.enableButton.configure(state="disabled")
        self.PP = tkinter.DoubleVar()
        self.PP.set(0.0)
        self.PPBox = tkinter.Entry(self.PowerCont)
        self.PPBox.insert(tkinter.END,"0.0")
        self.PPBox.grid(row=1,column=0)
        self.PPBox.configure(state="disabled")
        self.PPButton = tkinter.Button(self.PowerCont,text = "Send",command=self.setPP)
        self.PPButton.grid(row=1,column=1)
        self.PPButton.configure(state="disabled")
        self.PPLabel = tkinter.Label(self.PowerCont,text="Power Proportion="+str(round(self.PP.get(),2)))
        self.PPLabel.grid(row=2)
        #Setup Query
        self.queryCont = tkinter.LabelFrame(self,text="Send Text to Laser")
        self.queryCont.grid(row=1,column=0)#,stick=tkinter.W)
        self.queryBox = tkinter.Entry(self.queryCont)
        self.queryBox.grid(row=0,column=0)
        self.querySend = tkinter.Button(self.queryCont,text="Send",command=self.send)
        self.querySend.configure(state="disabled")
        self.querySend.grid(row=0,column=1)
        #Setup terminal
        self.terminalCont = tkinter.LabelFrame(self,text="Terminal")
        self.terminalCont.grid(row=2,columnspan=3)#,stick=tkinter.W)
        self.terminal = tkinter.Text(self.terminalCont)
        self.terminal.grid(row=1)
        self.terminal.insert(tkinter.END," > ")
        self.terminal.configure(state="disabled")
    
    def connect(self):
        if not self.connectStatue:
            connectedQ = False
            try:
                self.he = he1060.HE1060(self.comLabel.get())
                connectedQ = True
            except:
                self._print("No laser found on "+self.comLabel.get())
                connectedQ = False
            if connectedQ:
                self.connectStatue = True
                self.connectButton.configure(background="Red",text="Disconnect Laser")
                self.enableButton.configure(state="normal")
                self.querySend.configure(state="normal")
                for i in range(len(self.reprates)):
                    self.RRCheck[i].configure(state="normal")
                self._print("Connected to "+self.comLabel.get())
        else:
            connectedQ = True
            try:
                self.he.close()
                connectedQ = False
            except:
                self._print("No laser found to close")
                connectedQ = True
            if not connectedQ:
                self.connectStatue = False
                self.connectButton.configure(background="Grey",text="Connect Laser")
                self.enableButton.configure(state="disabled")
                self.querySend.configure(state="disabled")
                for i in range(len(self.reprates)):
                    self.RRCheck[i].configure(state="disabled")
                self.he.close()
                self._print("Disconnected")
            
    def enable(self):
        if not self.enableStatue:
            self.he.setEnable()
            he1060.sleep(2)#Allow enable time
            enableQ = self.he.getEnable()
            if enableQ:
                self.enableStatue = True
                self.PP.set(0.01)
                self.PPLabel.configure(text = "Power Proportion="+str(round(self.PP.get(),2)))
                self.enableButton.configure(background="Red",text="Disable Laser")
                for i in range(len(self.reprates)):
                    self.RRCheck[i].configure(state="disabled")
                self.PPBox.configure(state="normal")
                self.PPButton.configure(state="normal")
                self._print("Laser Enabled")
        else:
            self.he.setDisable()
            he1060.sleep(2)#Allow disable time
            enableQ = self.he.getEnable()
            if not enableQ:
                self.enableStatue = False
                self.PP.set(0.00)
                self.PPLabel.configure(text = "Power Proportion="+str(round(self.PP.get(),2)))
                self.enableButton.configure(background="Brown",text="Enable Laser")
                for i in range(len(self.reprates)):
                    self.RRCheck[i].configure(state="normal")
                self.PPBox.configure(state="disabled")
                self.PPButton.configure(state="disabled")
                self._print("Laser Disabled")
    
    def send(self):
        mesToSend = self.queryBox.get()
        self._print("Sending: \""+mesToSend+"\"")
        mes = self.he.query(mesToSend)
        self._print("Returned: \""+mes[:-2]+"\"")
		
    def setRR(self):
        rr = self.rr.get()
        self._print("Setting Rep Rate to "+str(round(rr,2))+" MHz")
        self.he.setRepRate(round(rr,2))
        self._print("Rep Rate Set to "+str(round(self.he.getRepRate(),2))+" MHz")

    def setPP(self):
        pp = float(self.PPBox.get())
        self._print("Setting Power to Proportion: "+str(pp))
        self.he.setPP(pp)
        self.PP.set(self.he.getPP())
        self._print("Power Set to Proportion: "+str(self.PP.get()))
        self.PPLabel.configure(text = "Power Proportion="+str(round(self.PP.get(),2)))

    def _print(self,message):
        self.terminal.configure(state="normal")
        self.terminal.insert(tkinter.END,message+"\n > ")
        self.terminal.see("end")
        self.terminal.configure(state="disabled")
		
if __name__ == '__main__':
	app = App()
	app.master.title("Fianium HE1060 Laser Controller")
	app.mainloop()