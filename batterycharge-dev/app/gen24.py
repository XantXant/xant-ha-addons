import modbus.client
import ctypes
import time
import functools

print = functools.partial(print, flush=True)

class Gen24:
    def __init__(self, host):
        self.host = host
        self.client = modbus.client.client(host=host)
        self.setTimeout(75*60)

    def getData(self):
        self.WChaMax, self.WChaGra, self.WDisChaGra, self.StorCtl_Mod, _, self.MinRsvPct, self.ChaState, _, _, self.ChaSt, self.OutWRte, self.InWRte, _, self.InOutWRte_RvrtTms, _, self.ChaGriSet, self.WChaMax_SF, self.WChaDisChaGra_SF, _, self.MinRsvPct_SF, self.ChaState_SF, _, _, self.InOutWRte_SF = self.client.read(FC=3, ADR=40345, LEN=24)

        self.s_WChaMax_SF = ctypes.c_int16(self.WChaMax_SF).value
        self.s_WChaDisChaGra_SF = ctypes.c_int16(self.WChaDisChaGra_SF).value
        self.s_MinRsvPct_SF = ctypes.c_int16(self.MinRsvPct_SF).value
        self.s_ChaState_SF = ctypes.c_int16(self.ChaState_SF).value
        self.s_InOutWRte_SF = ctypes.c_int16(self.InOutWRte_SF).value

        self.s_OutWRte = ctypes.c_int16(self.OutWRte).value
        self.s_InWRte = ctypes.c_int16(self.InWRte).value

        self.c_WChaMax = self.WChaMax*(10**self.s_WChaMax_SF)
        self.c_WChaGra = self.WChaGra*(10**self.s_WChaDisChaGra_SF)
        self.c_WDisChaGra = self.WDisChaGra*(10**self.s_WChaDisChaGra_SF)
        self.c_MinRsvPct = self.MinRsvPct*(10**self.s_MinRsvPct_SF)
        self.c_ChaState = self.ChaState*(10**self.s_ChaState_SF)
        self.c_OutWRte = self.s_OutWRte*(10**self.s_InOutWRte_SF)
        self.c_InWRte = self.s_InWRte*(10**self.s_InOutWRte_SF)
    
    def getSoC(self):
        self.getData()
        return self.c_ChaState
    
    def printData(self):
        self.getData()
        ChaSt_str = ["OFF", "EMPTY", "DISCHARGING", "CHARGING", "FULL", "HOLDING", "TESTING"]
        print(f"MaxCharge/DisCharge: {self.c_WChaMax:11} W")
        print(f"MaxChargeRate:       {self.c_WChaGra:11} %")
        print(f"MaxDischargeRate:    {self.c_WDisChaGra:11} %")
        print(f"ControlMode:         {self.StorCtl_Mod:11}")
        print(f"MinReserve:          {self.c_MinRsvPct:11} %")
        print(f"SoC:                 {self.c_ChaState:11.1f} %")
        print(f"State:               {ChaSt_str[self.ChaSt-1]:>11}")
        print(f"MaxDischargeRate:    {self.c_OutWRte:11.1f} % --> {self.c_WChaMax*self.c_OutWRte/100:11} W")
        print(f"MaxChargeRate:       {self.c_InWRte:11.1f} % --> {self.c_WChaMax*self.c_InWRte/100:11} W")
        print(f"TimeoutPeriod:       {self.InOutWRte_RvrtTms:11} s -->{self.InOutWRte_RvrtTms/60:8} min")
        print(f"ChaGridSet:          {self.ChaGriSet:11}")

    def chargeBattery(self, power):
        self.getData()
        self.setDischargeRatePower(power)
        self.setStorCtl_Mod(3)
    
    def dischargeBattery(self, power):
        self.getData()
        self.setChargeRatePower(power)
        self.setStorCtl_Mod(3)
    
    def backToNormal(self):
        percent = 100
        self.getData()
        self.setDischargeRate(percent)
        self.setChargeRate(percent)
        self.setStorCtl_Mod(0)
    
    def setChargeMode(self):
        self.getData()
        self.setStorCtl_Mod(3)

    def setNormalMode(self):
        self.getData()
        self.setStorCtl_Mod(0)

    def enableGridCharging(self):
        self.getData()
        self.setChaGriSet(1)

    def disableGridCharging(self):
        self.getData()
        self.setChaGriSet(0)

    def setStorCtl_Mod(self, mode):
        self.client.write(mode, FC=6, ADR=40348)         # StorCtl_Mod

    def setDischargeRatePower(self, power):
        per = power * 100 / self.c_WChaMax
        if per > 100:
            per = 100
        self.setDischargeRate(-per)
    
    def setChargeRatePower(self, power):
        per = power * 100 / self.c_WChaMax
        if per > 100:
            per = 100
        print(per)
        self.setChargeRate(-per)

    def setDischargeRate(self, percent):
        us_percent = ctypes.c_uint16(int(percent*100)).value
        self.client.write(us_percent, FC=6, ADR=40355)   # DischargeRate

    def setChargeRate(self, percent):
        us_percent = ctypes.c_uint16(int(percent*100)).value
        self.client.write(us_percent, FC=6, ADR=40356)   # ChargeRate

    def setTimeout(self, timeout):
        self.client.write(timeout, FC=6, ADR=40358)   # Seconds

    def setMinReserve(self, percent):
        percent = percent * 100
        self.client.write(percent, FC=6, ADR=40350)  # MinReserve
    
    def setChaGriSet(self, state):
        self.client.write(state, FC=6, ADR=40360)


if __name__ == "__main__":
    gen = Gen24("192.168.1.178")
    gen.printData()

    # gen.chargeBattery(10000)

    # gen.dischargeBattery(1000)

    gen.backToNormal()

    # gen.setMinReserve(20)
    
    time.sleep(5)
    gen.printData()
    print(gen.getSoC())

