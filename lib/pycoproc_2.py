F�F����FW&�2�f�"��&R��f�&�F���26VRF�R�6��Ɩ6V�6Rc�F�7V�V�B7WƖVBv�F�F��2f��R�� �2f��&�RB�GG3���wwr��6������V�6�W&6R�Ɩ6V�6��p�0�����'BF��P�g&���6���R���'B�$0����'B�F�����fW'6������s��"p��6�724�sd#��"""6�72f�"��FƖ�rF�RFV�W&GW&R6V�6�"4�sb�# ����FVr2W'&�"f�"FV�W&Gre
        +/- 5% error for relative humidity
        datasheet available at https://www.silabs.com/documents/public/data-sheets/Si7006-A20.pdf """

    SI7006A20_I2C_ADDR = const(0x40)

    # I2C commands
    TEMP_NOHOLDMASTER = const(0xF3)
    HUMD_NOHOLDMASTER = const(0xF5)
    WRITE_USER_REG1 = const(0xE6)
    READ_USER_REG1 = const(0xE7)
    WRITE_HEATER_CTRL_REG = const(0x51)
    READ_HEATER_CTRL_REG = const(0x11)

    # Register masks and offsets
    USER_REG1_HTR_ENABLE_MASK = const(0b00000100)
    USER_REG1_HTR_ENABLE_OFFSET = const(0x02)
    HTR_CTRL_REG_MASK = const(0b00001111)

    def __init__(self, pysense = None, sda = 'P22', scl = 'P21'):
        if pysense is not None:
            self.i2c = pysense.i2c
        else:
            self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl))

    def _getWord(self, high, low):
        return ((high & 0xFF) << 8) + (low & 0xFF)

    def temperature(self):
        """ obtaining the temperature(degrees Celsius) measured by sensor """
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([0xF3]))
        time.sleep(0.5)
        data = self.i2c.readfrom(SI7006A20_I2C_ADDR, 3)
        #print("CRC Raw temp data: " + hex(data[0]*65536 + data[1]*256 + data[2]))
        data = self._getWord(data[0], data[1])
        temp = ((175.72 * data) / 65536.0) - 46.85
        return temp

    def humidity(self):
        """ obtaining the relative humidity(%) measured by sensor """
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([0xF5]))
        time.sleep(0.5)
        data = self.i2c.readfrom(SI7006A20_I2C_ADDR, 2)
        data = self._getWord(data[0], data[1])
        humidity = ((125.0 * data) / 65536.0) - 6.0
        return humidity

    def read_user_reg(self):
        """ reading the user configuration register """
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([READ_USER_REG1]))
        time.sleep(0.5)
        data = self.i2c.readfrom(SI7006A20_I2C_ADDR, 1)
        return data[0]

    def read_heater_reg(self):
        """ reading the heater configuration register """
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([READ_HEATER_CTRL_REG]))
        time.sleep(0.5)
        data = self.i2c.readfrom(SI7006A20_I2C_ADDR, 1)
        return data[0]

    def write_heater_reg(self, heater_value):
        """ writing the heater configuration register """
        # We should only set the bottom four bits of this register
        heater_setting = heater_value & HTR_CTRL_REG_MASK
        self.write_reg(WRITE_HEATER_CTRL_REG, heater_setting)

    def heater_control(self, on_off):
        """ turn the heater on or off """
        # Get current settings for everything else
        user_reg = self.read_user_reg()
        # Set the heater bit
        user_reg = (user_reg & ~USER_REG1_HTR_ENABLE_MASK) | (on_off << USER_REG1_HTR_ENABLE_OFFSET)
        self.write_reg(WRITE_USER_REG1, user_reg)

    def read_electronic_id(self):
        """ reading electronic identifier """
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([0xFA]) + bytearray([0x0F]))
        time.sleep(0.5)
        sna = self.i2c.readfrom(SI7006A20_I2C_ADDR, 4)
        time.sleep(0.1)
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([0xFC]) + bytearray([0xC9]))
        time.sleep(0.5)
        snb = self.i2c.readfrom(SI7006A20_I2C_ADDR, 4)
        return [sna[0], sna[1], sna[2], sna[3], snb[0], snb[1], snb[2], snb[3]]

    def read_firmware(self):
        """ reading firmware version """
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([0x84])+ bytearray([0xB8]))
        time.sleep(0.5)
        fw = self.i2c.readfrom(SI7006A20_I2C_ADDR, 1)
        return fw[0]

    def read_reg(self, reg_addr):
        """ reading a register """
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([reg_addr]))
        time.sleep(0.5)
        data = self.i2c.readfrom(SI7006A20_I2C_ADDR, 1)
        return data[0]

    def write_reg(self, reg_addr, value):
        """ writing a register """
        self.i2c.writeto(SI7006A20_I2C_ADDR, bytearray([reg_addr])+bytearray([value]))
        time.sleep(0.1)

    def dew_point(self):
        """ computing the dew pointe temperature (deg C) for the current Temperature and Humidity measured pair
            at dew-point temperature the relative humidity is 100% """
        temp = self.temperature()
        humid = self.humidity()
        h = (math.log(humid, 10) - 2) / 0.4343 + (17.62 * temp) / (243.12 + temp)
        dew_p = 243.12 * h / (17.62 - h)
        return dew_p

    def humid_ambient(self, t_ambient, dew_p = None):
        """ returns the relative humidity compensated for the current Ambient temperature
            for ex: T-Ambient is 24.4 degC, but sensor indicates Temperature = 31.65 degC and Humidity = 47.3%
                    -> then the actual Relative Humidity is 72.2%
            this is computed because the dew-point should be the same """
        if dew_p is None:
            dew_p = self.dew_point()
        h = 17.62 * dew_p / (243.12 + dew_p)
        h_ambient = math.pow(10, (h - (17.62 * t_ambient) / (243.12 + t_ambient)) * 0.4343 + 2)
        return h_ambient
8�2�W7"�&���V�b�F���0�26��&�v�B�2�##��6��Ɩ֗FVB�0�2F��26�gGv&R�2Ɩ6V�6VBV�FW"F�Rt�Ru�fW'6���2�"琢2�FW"fW'6����v�F�W&֗GFVBFF�F����FW&�2�f�"��&R��f�&�F���26VRF�R�6��Ɩ6V�6Rc�F�7V�V�B7WƖVBv�F�F��2f��R�� �2f��&�RB�GG3���wwr��6������V�6�W&6R�Ɩ6V�6��p�0��26VR�GG3���F�72��6����f�"��&R��f�&�F���&Vv&F��rƖ'&'�7V6�f�70��g&���6���R���'B��g&���6���R���'B�$0����'BF��P����'B�6�Р���fW'6������s��"p��"""�2�5Rvkeup reason types """
WAKE_REASON_ACCELEROMETER = 1
WAKE_REASON_PUSH_BUTTON = 2
WAKE_REASON_TIMER