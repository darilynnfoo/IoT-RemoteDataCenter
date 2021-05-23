�ɸ���͔((���������ɕ���ɔ�͕����(�����������͕����������1Q%QU�(������������Ʌ�͔�5A0����ɕፕ�ѥ����%����ɕ�Ё5����ɕ���Ё5����5A0����Ȉ�((��������=UQ}A}5M��͕����Ɍ�ɕ���ɽ�}����5A0����}$�H��5A0����}AIMMUI}Q}5M�Ĥ(��������=UQ}A}M��͕����Ɍ�ɕ���ɽ�}����5A0����}$�H��5A0����}AIMMUI}Q}M�Ĥ(��������=UQ}A}1M��͕����Ɍ�ɕ���ɽ�}����5A0����}$�H��5@L3115_PRESSURE_DATA_LSB,1)

        return float((OUT_P_MSB[0] << 10) + (OUT_P_CSB[0] << 2) + ((OUT_P_LSB[0] >> 6) & 0x03) + ((OUT_P_LSB[0] >> 4) & 0x03) / 4.0)

    def altitude(self):
        if self.mode == PRESSURE:
            raise MPL3115A2exception("Incorrect Measurement Mode MPL3115A2")

        OUT_P_MSB = self.i2c.readfrom_mem(MPL3115_I2CADDR, MPL3115_PRESSURE_DATA_MSB,1)
        OUT_P_CSB = self.i2c.readfrom_mem(MPL3115_I2CADDR, MPL3115_PRESSURE_DATA_CSB,1)
        OUT_P_LSB = self.i2c.readfrom_mem(MPL3115_I2CADDR, MPL3115_PRESSURE_DATA_LSB,1)

        alt_int = (OUT_P_MSB[0] << 8) + (OUT_P_CSB[0])
        alt_frac = ((OUT_P_LSB[0] >> 4) & 0x0F)

        if alt_int > 32767:
            alt_int -= 65536

        return float(alt_int + alt_frac / 16.0)

    def temperature(self):
        OUT_T_MSB = self.i2c.readfrom_mem(MPL3115_I2CADDR, MPL3115_TEMP_DATA_MSB,1)
        OUT_T_LSB = self.i2c.readfrom_mem(MPL3115_I2CADDR, MPL3115_TEMP_DATA_LSB,1)

        temp_int = OUT_T_MSB[0]
        temp_frac = OUT_T_LSB[0]

        if temp_int > 127:
            temp_int -= 256

        return float(temp_int + temp_frac / 256.0)
8�2�W7"�&���V�b�F���0�26��&�v�B�2�#���6��Ɩ֗FVB�0�2F��26�gGv&R�2Ɩ6V�6VBV�FW"F�Rt�Ru�fW'6���2�"琢2�FW"fW'6����v�F�W&֗GFVBF