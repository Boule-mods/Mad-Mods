import machine

def setAD5282(self,ADDR ,DATA):
        data_frame = bytearray([0x00, DATA])
        self.i2c1.writeto(ADDR, data_frame)
      
def setAD5258(self,ADDR ,DATA):
        data_frame = bytearray([0x00, DATA])
        self.i2c1.writeto(ADDR, data_frame)

def setMCP4541(self,ADDR ,DATA):
        data_frame = bytearray([DATA])
        self.i2c2.writeto_mem(ADDR,0x00, data_frame)
