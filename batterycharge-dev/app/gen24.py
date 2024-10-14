import modbus.client
import ctypes
import time
import functools
import os
import sys


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


print = functools.partial(print, flush=True)

class Gen24:
    def __init__(self, host):
        self.host = host
        with HiddenPrints():
            self.client = modbus.client.client(host=host)
            self.setTimeout(75*60)
    
    def _write(self, *DAT, FC=16, ADR=0):
        with HiddenPrints():
            self.client.write(*DAT, FC, ADR)

    def _read(self, FC=4, ADR=0, LEN=10):
        with HiddenPrints():
            return self.client.read(FC, ADR, LEN)

    def getData(self):
        self.WChaMax, self.WChaGra, self.WDisChaGra, self.StorCtl_Mod, _, self.MinRsvPct, self.ChaState, _, _, self.ChaSt, self.OutWRte, self.InWRte, _, self.InOutWRte_RvrtTms, _, self.ChaGriSet, self.WChaMax_SF, self.WChaDisChaGra_SF, _, self.MinRsvPct_SF, self.ChaState_SF, _, _, self.InOutWRte_SF = self._read(FC=3, ADR=40345, LEN=24)

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
        self._write(mode, FC=6, ADR=40348)         # StorCtl_Mod

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
        self._write(us_percent, FC=6, ADR=40355)   # DischargeRate

    def setChargeRate(self, percent):
        us_percent = ctypes.c_uint16(int(percent*100)).value
        self._write(us_percent, FC=6, ADR=40356)   # ChargeRate

    def setTimeout(self, timeout):
        self._write(timeout, FC=6, ADR=40358)   # Seconds

    def setMinReserve(self, percent):
        percent = percent * 100
        self._write(percent, FC=6, ADR=40350)  # MinReserve
    
    def setChaGriSet(self, state):
        self._write(state, FC=6, ADR=40360)


if __name__ == "__main__":
    gen = Gen24("192.168.1.178")
    gen.printData()

    # gen.chargeBattery(10000)

    # gen.dischargeBattery(10000)
    # gen.setChargeRate(100)
    # gen.enableGridCharging()

    # gen.backToNormal()

    gen.setMinReserve(20)
    
    time.sleep(5)
    gen.printData()
    print(gen.getSoC())
