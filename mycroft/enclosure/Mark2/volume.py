import os, time
from mycroft.enclosure.MycroftHardware.MycroftVolume import MycroftVolume

class Volume(MycroftVolume):
    default_volume = 5         # valid from 0-10
    register = 75              # 0x4b
    min_vol = 10               # hardware constraint
    max_vol = 60
    vol_inc = (max_vol - min_vol) / 10 
    fifty_two_zeros = "0 " * 52
    vfctrl_cmd = "sudo /home/pi/sj201_revB/vfctrl_usb SET_I2C_WITH_REG"

    def __init__(self):
        self.level = self.default_volume
        self.set_volume(self.level)
        self.capabiities = {
                    "range":(0.0,1.0),
                    "type":"MycroftAmp"
                }

    def get_volume(self):
        return self.level

    def set_volume(self, level):
        # it wants a value between 0-10
        if level > -1 and level < 11:
            self.level = level
        else:
            if level < 0:
                self.level = 0

            if level > 10:
                self.level = 10

        new_vol = self.min_vol + (self.vol_inc * self.level)

        params = "%d %d %d %d" % (self.register, 0, 1, new_vol)
        cmd = "%s %s %s" % (self.vfctrl_cmd, params, self.fifty_two_zeros)

        #print(cmd)
        os.system(cmd)

    def set_hw_volume(self, vol):
        # old code likes 0.0 - 1.0
        # this code wants 0-10
        vol = int(vol * 10)
        self.set_volume(vol)

    def get_hw_volume(self):
        if self.level < 1:
            return float(0.0)
        return float(float(self.level) / 10)

    def get_capabilities(self):
        return self.capabilities

