É…¹” À°±•¹Ñ ¤è4(€€€€€€€€€€€¥˜€¡‰±½­m¥t€ğ€ÄØ¤è4(€€€€€€€€€€€€€€€É•Ñ}Ù…°€¬ô€ ˆÀ•à€ˆ€”‰±½­m¥t¤4(€€€€€€€€€€€•±Í”:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
8¢2÷W7"ö&–âöVçb—F†öà¢0¢26÷—&–v‡B†2’##Â–6öÒÆ–Ö—FVBà¢0¢2F†—26ögGv&R—2Æ–6Vç6VBVæFW"F†RtåRuÂfW'6–öâ2÷"ç¢2ÆFW"fW'6–öâÂv—F‚W&Ö—GFVBFF—F–öæÂFW&×2âf÷"Ö÷&R–æf÷&ÖF–öà¢26VRF†R–6öÒÆ–6Væ6RcãFö7VÖVçB7WÆ–VBv—F‚F†—2f–ÆRÂ÷ ¢2f–Æ&ÆRB‡GG3¢ò÷wwrç–6öÒæ–òö÷Vç6÷W&6RöÆ–6Vç6–æp¢0 ¦–×÷'BF–ÖP¦g&öÒÖ6†–æR–×÷'B“$0 ¤ÅD•ETDRÒ6öç7Bƒ¥$U55U$RÒ6öç7Bƒ ¦6Æ72ÕÃ3T&W†6WF–öâ„W†6WF–öâ“ ¢70 ¦6Æ72ÕÃ3T# ¢ÕÃ3Uô“$4DE"Ò6öç7Bƒƒc¢ÕÃ3UõTATUS = const(0x00)
    MPL3115_PRESSURE_DATA_MSB = const(0x01)
    MPL3115_PRESSURE_DATA_CSB = const(0x02)
    MPL3115_PRESSURE_DATA_LSB = const(0x03)
    MPL3115_TEMP_DATA_MSB = const(0x04)
    MPL3115_TEMP_DATA_LSB = const(0x05)
    MPL3115_DR_STATUS = const(0x06)
    MPL3115_DELTA_DATA = const(0x07)
    MPL3115_WHO_AM_I = const(0x0c)
    MPL3115_FIFO_STATUS = const(0x0d)
    MPL3115_FIFO_DATA = const(0x0e)
    MPL3115_FIFO_SETUP = const(0x0e)
    MPL3115_TIME_DELAY = const(0x10)
    MPL3115_SYS_MODE = const(0x11)
    MPL3115_INT_SORCE = const(0x12)
    MPL3115_PT_DATA_CFG = const(0x13)
    MPL3115_BAR_IN_MSB = const(0x14)
    MPL3115_P_ARLARM_MSB = const(0x16)
    MPL3115_T_ARLARM = const(0x18)
    MPL3115_P_ARLARM_WND_MSB = const(0x19)
    MPL3115_T_ARLARM_WND = const(0x1b)
    MPL3115_P_MIN_DATA = const(0x1c)
    MPL3115_T_MIN_DATA = const(0x1f)
    MPL3115_P_MAX_DATA = const(0x21)
    MPL3115_T_MAX_DATA = const(0x24)
    MPL3115_CTRL_REG1 = const(0x26)
    MPL3115_CTRL_REG2 = const(0x27)
    MPL3115_CTRL_REG3 = const(0x28)
    MPL3115_CTRL_REG4 = const(0x29)
    MPL3115_CTRL_REG5 = const(0x2a)
    MPL3115_OFFSET_P = const(0x2b)
    MPL3115_OFFSET_T = const(0x2c)
    MPL3115_OFFSET_H = const(0x2d)

    def __init__(self, pysense = None, sda = 'P22', scl = 'P21', mode = PRESSURE):
        if pysense is not None:
            self.i2c = pysense.i2c
        else:
            self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl))

        self.STA_reg = bytearray(1)
        self.mode = mode

        if self.mode is PRESSURE:
            self.i2c.writeto_mem(MPL3115_I2CADDR, MPL3115_CTRL_REG1, bytes([0x38])) # barometer mode, not raw, oversampling 128, minimum time 512 ms
            self.i2c.writeto_mem(MPL3115_I2CADDR, MPL3115_PT_DATA_CFG, bytes([0x07])) # no events detected
            self.i2c.writeto_mem(MPL3115_I2CADDR, MPL3115_CTRL_REG1, bytes([0x39])) # active
        elif self.mode is ALTITUDE:
            self.i2c.writeto_mem(MPL3115_I2CADDR, MPL3115_CTRL_REG1, bytes([0xB8])) # altitude mode, not raw, oversampling 128, minimum time 512 ms
            self.i2c.writeto_mem(MPL3115_I2CADDR, MPL3115_PT_DATA_CFG, bytes([0x07])) # no events detected
            self.i2c.writeto_mem(MPL3115_I2CADDR, MPL3115_CTRL_REG1, bytes([0xB9])) # active
        else:
            raise MPL3115A2exception("Inv