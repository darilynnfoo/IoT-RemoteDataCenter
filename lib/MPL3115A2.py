W7V�B7V6�F�@Т2vRF���B��6RF�R&�BvR�W7B6WB�bvR�fR collision.
                for rbx in range(0, rx_len):
                    uid_this_level[int(known_bits / 8) + rbx] = uid_this_level[int(known_bits / 8) + rbx] | buf[rbx]
                self.print_debug("uid_this_level after reading buffer (known_bits=%d):" % known_bits)
                self.mfrc630_print_block(uid_this_level, 0)
                self.print_debug("known_bits: %x + collision_pos: %x = %x" % (known_bits, collision_pos, known_bits + collision_pos))
                known_bits = known_bits + collision_pos
                self.print_debug("known_bits: %x" % known_bits)

                if known_bits >= 32:
                    self.print_debug("exit collision loop: uid_this_level kb %d long: " % known_bits);
                    self.mfrc630_print_block(uid_this_level, 10)
                    break;  # done with collision loop
                # end collission loop

            # check if the BCC matches
            bcc_val = uid_this_level[4]  # always at position 4, either with CT UID[0-2] or UID[0-3] in front.
            bcc_calc = uid_this_level[0] ^ uid_this_level[1] ^ uid_this_level[2] ^ uid_this_level[3]
            self.print_debug("BCC calc: %x" % bcc_calc)
            if (bcc_val != bcc_calc):
                self.print_debug("Something went wrong, BCC does not match.")
                return 0

            # clear interrupts
            self.mfrc630_clear_irq0()
            self.mfrc630_clear_irq1()

            send_req[0] = cmd
            send_req[1] = 0x70
            send_req[2] = uid_this_level[0]
            send_req[3] = uid_this_level[1]
            send_req[4] = uid_this_level[2]
            send_req[5] = uid_this_level[3]
            send_req[6] = bcc_calc
            message_length = 7

            # Ok, almost done now, we re-enable the CRC's
            self.mfrc630_write_reg(MFRC630_REG_TXCRCPRESET, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_ON)
            self.mfrc630_write_reg(MFRC630_REG_RXCRCCON, MFRC630_RECOM_14443A_CRC | MFRC630_CRC_ON)

            # reset the Tx and Rx registers (disable alignment, transmit full bytes)
            self.mfrc630_write_reg(MFRC630_REG_TXDATANUM, (known_bits % 8) | MFRC630_TXDATANUM_DATAEN)
            rxalign = 0
            self.mfrc630_write_reg(MFRC630_REG_RXBITCTRL, (0 << 7) | (rxalign << 4))

            # actually send it!
            self.mfrc630_cmd_transceive(send_req)
            self.print_debug("send_req %d long: " % message_length)
            self.mfrc630_print_block(send_req, message_length)

            # Block until we are done...
            irq1_value = 0
            while not (irq1_value & (1 << timer_for_timeout)):
                irq1_value = self.mfrc630_irq1()
                if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):  # either ERR_IRQ or RX_IRQ
                    break  # stop polling irq1 and quit the timeout loop.
            self.mfrc630_cmd_idle()

            # Check the source of exiting the loop.
            irq0_value = self.mfrc630_irq0()
            self.print_debug("irq0: %x" % irq0_value)
            if irq0_value & MFRC630_IRQ0_ERR_IRQ:
                # Check what kind of error.
                error = self.mfrc630_read_reg(MFRC630_REG_ERROR)
                self.print_debug("error: %x" % error)
                if error & MFRC630_ERROR_COLLDET:
                    # a collision was detected with NVB=0x70, should never happen.
                    self.print_debug("a collision was detected with NVB=0x70, should never happen.")
                    return 0
            # Read the sak answer from the fifo.
            sak_len = self.mfrc630_fifo_length()
            self.print_debug("sak_len: %x" % sak_len)
            if sak_len != 1:
                return 0

            sak_value = self.mfrc630_read_fifo(sak_len)

            self.print_debug("SAK answer: ")
            self.mfrc630_print_block(sak_value, 1)

            if (sak_value[0] & (1 << 2)):
                # UID not yet complete, continue with next cascade.
                # This also means the 0'th byte of the UID in this level was CT, so we
                # have to shift all bytes when moving to uid from uid_this_level.
                for UIDn in range(0, 3):
                    # uid_this_level[UIDn] = uid_this_level[UIDn + 1];
                    uid[(cascade_level - 1) * 3 + UIDn] = uid_this_level[UIDn + 1]
            else:
                # Done according so SAK!
                # Add the bytes at this level to the UID.
                for UIDn in range(0, 4):
                    uid[(cascade_level - 1) * 3 + UIDn] = uid_this_level[UIDn];

                # Finally, return the length of the UID that's now at the uid "pointer".
                return cascade_level * 3 + 1

        self.print_debug("Exit cascade loop nr. %d: !rn cascade_level * 3 + 1

        self.print_debug("Exit cascade loop nr. %d: " % cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH���̀���4(4(��������͕����ɥ��}���՜���Ё��͍����������ȸ���耈�����͍���}��ٕ��4(��������͕�����Ɍ���}�ɥ��}������ե������4(4(��������ɕ��ɸ���������ѥ�����U%��������4(4(����������Ɍ���}5}��Ѡ�͕����ե������}�������������4(����������������ѡ��ɥ��Ё��ѕ�����̸4(4(�����B'���FW""�Т&W@  # configure a timeout timer.   self.print_debug("Exit cascade loop nr. %d: " % cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_fbug("Exit cascade loop nr. %d: " % cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  e loop nr. %d: " % cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match t`% cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interr
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

       !frc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to dck(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interru       return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and tic getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENailed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
   & mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include Eh(self, uid, key_type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
 /type, block):
        # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc6       # Enable the right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFPthe right interrupts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN,5pts.

    !�������ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_�����ѕȈ�4(����������������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFR@�����������ɕ���ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_I��ۙ�Y�\�HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
        skY[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
        self.mfrc630_writh��������ѥ���}���}ѥ����Ѐ������͡�ձ����э��ѡ������������ѕ����и4(4(�������������ɑ����Ѽ���х͡��Ё%�ѕ����Ё������������ѥ��ȁݥѠ�5UQ!9P����Ё����4(��������������Ց��II=H��́ݕ���4(��������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I}%ID�8��5I���}%ID�9}%1}%IE8���5I���}%ID�9}II}%IE8�4(��������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I%�F��V�WB�26��V�B�F6�F�RV�&�VB��FW''WB�РТ266�&F��rF�FF6�VWB��FW''WB���F�R�BF��W"v�F��dUD�T�B�'WB�WG0Т2��6�VFRU%$�"2vV���Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu��%T���e$3c3��%T���D�U��%T���e$3c3��%T��U%%��%T�Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu��%T���e$3c3��[X]�H[�X�Y[�\��\�B�B��X��ܙ[���]\�Y][�\��\ۈYH[�[Y\��]Q�UUS��]]�B��[��YHT��Ԉ\��[�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LS�Q��͌��T�LS��QW�T�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��e enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
        self.mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)  # only tre�и4(4(�������������ɑ����Ѽ���х͡��Ё%�ѕ����Ё������������ѥ��ȁݥѠ�5UQ!9P����Ё����4(��������������Ց��II=H��́ݕ���4(��������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I}%ID�8��5I���}%ID�9}%1}%IE8���5I���}%ID�9}II}%IE8�4(��������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I}%ID�8��5I���}%ID�9}Q%5H�}%IE8����������ɥ���ȁ���ѥ��ȁ�266�&F��rF�FF6�VWB��FW''WB���F�R�BF��W"v�F��dUD�T�B�'WB�WG0Т2��6�VFRU%$�"2vV���Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu��%T���e$3c3��%T���D�U��%T���e$3c3��%T��U%%��%T�Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu��%T���e$3c3��%T��D��U#��%T�2��ǒG&�vvW"��F��W"f�"�'РТ \�Y][�\��\ۈYH[�[Y\��]Q�UUS��]]�B��[��YHT��Ԉ\��[�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LS�Q��͌��T�LS��QW�T�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\���n idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
        self.mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)  # only trigger on timer for irq1

        # Set timer to 221 kHz clock, sta�ݥѠ�5UQ!9P����Ё����4(��������������Ց��II=H��́ݕ���4(��������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I}%ID�8��5I���}%ID�9}%1}%IE8���5I���}%ID�9}II}%IE8�4(��������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I}%ID�8��5I���}%ID�9}Q%5H�}%IE8����������ɥ���ȁ���ѥ��ȁ��ȁ����4(4(����������M�Ёѥ��ȁѼ���ā�!聍�������х�Ё�Ёѡ��������'WB�WG0Т2��6�VFRU%$�"2vV���Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu��%T���e$3c3��%T���D�U��%T���e$3c3��%T��U%%��%T�Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu��%T���e$3c3��%T��D��U#��%T�2��ǒG&�vvW"��F��W"f�"�'РТ26WBF��W"F�##���6��6��7F'BBF�RV�B�bG��Т6T�[��YHT��Ԉ\��[�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LS�Q��͌��T�LS��QW�T�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imT�\��[�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LS�Q��͌��T�LS��QW�T�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(t�[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LS�Q��͌��T�LS��QW�T�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout'�ܚ]WܙY�Q��͌�ԑQ��T�LS�Q��͌��T�LS��QW�T�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTRL�ԑQ��T�LS�Q��͌��T�LS��QW�T�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFR͌��T�LS��QW�T�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_STBT�QS�Q��͌��T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
   T�LS��T���T�QS�CB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waitcB��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = ��͌��ܚ]WܙY�Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2Q��͌�ԑQ��T�LQS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # QS�Q��͌��T�LQS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to QS��SQT��T�QS�H�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that x�ۛH�Y��\�ۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait fۈ[Y\��܈\�LCB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of |CB�B���][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

       ][Y\����H�������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timb������\�]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(tiX]H[�و�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout,#�B��[��Y��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 tiY��͌��imer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 ticks of 5 usec is!��}����ɽ��ѥ���}���}ѥ����а�5I���}Q=9QI=1}1-|���-!h���5I���}Q=9QI=1}MQIQ}Qa}9�4(����������Ʌ���݅�ѥ���ѥ���]P����؁���ؽ������ȁ]$4(����������]$�����ձ�́Ѽ����ȸ���ͼ�ѡ�Ёݽձ�������݅�Ё��ȁ����᥵մ������յ�4(4(��������͕�����Ɍ���}ѥ���}͕�}ɕ�����ѥ���}���}ѥ����а���������������ѥ��́���ԁ�͕���̀����̸4(���������f�%�F��V�WB��e$3c3�D4��E$���4ĵ�#�����e$3c3�D4��E$���5D%E�E��T�B�Т2g&�Rv�F��rF��S�euB��#Sb�b�f2��"et�Т2et�FVfV�G2F�f�W"���6�F�Bv�V�B�V�v�Bf�"����V��b�V�0РТ6V�b��g&3c3�F��W%�6WE�&V��B�F��W%�f�%�F��V�WB�#�2#F�6�2�bRW6V2�2�2�Т6V�b��g&3c3�F��P͌���ӕ�����̌LR��Q��͌���ӕ����T���S�
CB����[YH�Z][��[YN���H
�M�M�٘�H���CB����HY�][����\������]��[YX[��Z]�܈HX^[][Hو�[\�B�B��[��Y��͌��[Y\���]ܙ[�Y
[Y\�ٛܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y[_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 ticks of 5 usec is 10 ms.
        self.mfrc630_timer_set_value(timer_for_timeout, 20�}Q=9QI=1}MQIQ}Qa}9�4(����������Ʌ���݅�ѥ���ѥ���]P����؁���ؽ������ȁ]$4(����������]$�����ձ�́Ѽ����ȸ���ͼ�ѡ�Ёݽձ�������݅�Ё��ȁ����᥵մ������յ�4(4(��������͕�����Ɍ���}ѥ���}͕�}ɕ�����ѥ���}���}ѥ����а���������������ѥ��́���ԁ�͕���̀����̸4(��������͕�����Ɍ���}ѥ���}͕�}م�Ք�ѥ���}���}ѥ����а������4(4(����������E��T�B�Т2g&�Rv�F��rF��S�euB��#Sb�b�f2��"et�Т2et�FVfV�G2F�f�W"���6�F�Bv�V�B�V�v�Bf�"����V��b�V�0РТ6V�b��g&3c3�F��W%�6WE�&V��B�F��W%�f�%�F��V�WB�#�2#F�6�2�bRW6V2�2�2�Т6V�b��g&3c3�F��W%�6WE�f�VR�F��W%�f�%�F��V�WB�#�РТ�'�f�VR� Р����[YH�Z][��[YN���H
�M�M�٘�H���CB����HY�][����\������]��[YX[��Z]�܈HX^[][Hو�[\�B�B��[��Y��͌��[Y\���]ܙ[�Y
[Y\�ٛܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y� time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 ticks of 5 usec is 10 ms.
        self.mfrc630_timer_set_value(timer_for_timeout, 2000)

        irq1_value = 0

        self.mfrc630_clear_irq0(؁���ؽ������ȁ]$4(����������]$�����ձ�́Ѽ����ȸ���ͼ�ѡ�Ёݽձ�������݅�Ё��ȁ����᥵մ������յ�4(4(��������͕�����Ɍ���}ѥ���}͕�}ɕ�����ѥ���}���}ѥ����а���������������ѥ��́���ԁ�͕���̀����̸4(��������͕�����Ɍ���}ѥ���}͕�}م�Ք�ѥ���}���}ѥ����а������4(4(������������}م�Ք���4(4(��������͕�����Ɍ���}�����}��������������ȁ����5t�Т2et�FVfV�G2F�f�W"���6�F�Bv�V�B�V�v�Bf�"����V��b�V�0РТ6V�b��g&3c3�F��W%�6WE�&V��B�F��W%�f�%�F��V�WB�#�2#F�6�2�bRW6V2�2�2�Т6V�b��g&3c3�F��W%�6WE�f�VR�F��W%�f�%�F��V�WB�#�РТ�'�f�VR� РТ6V�b��g&3c3�6�V%��'��26�V"�' Т6V�b��fHY�][����\������]��[YX[��Z]�܈HX^[][Hو�[\�B�B��[��Y��͌��[Y\���]ܙ[�Y
[Y\�ٛܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 ticks of 5 usec is 10 ms.
        self.mfrc630_timer_set_value(timer_for_timeout, 2000)

        irq1_value = 0

        self.mfrc630_clear_irq0()  # clear irq0
        self.mfrc630_clear_irq1()  # clear irq9YX[��Z]�܈HX^[][Hو�[\�B�B��[��Y��͌��[Y\���]ܙ[�Y
[Y\�ٛܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # stHX^[][Hو�[\�B�B��[��Y��͌��[Y\���]ܙ[�Y
[Y\�ٛܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentil�B�B��[��Y��͌��[Y\���]ܙ[�Y
[Y\�ٛܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure��Y��͌��[Y\���]ܙ[�Y
[Y\�ٛܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.l�]ܙ[�Y
[Y\�ٛܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(Y�ܗ�[Y[�]�
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block,
H��X���وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

       (وH\�X�\�L\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we\˃B��[��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
    #��Y��͌��[Y\���]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (ir\�]ݘ[YJ[Y\�ٛܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 <<!�ܗ�[Y[�]�
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeo|
CB�B�\�LWݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
           Wݘ[YHHB�B��[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = seH�[��Y��͌���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1((���X\��\�L

H��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            ih��X\�\�LB��[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFX�[��Y��͌���X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL��X\��\�LJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):
         �������ȁ����4(4(�����������х�Ёѡ����ѡ��ѥ��ѥ����ɽ����ɔ�4(��������͕�����Ɍ���}���}��Ѡ����}�������������ե��4(4(����������������չѥ��ݔ��ɔ�����4(��������ݡ������Ѐ�����}م�Ք����Ā���ѥ���}���}ѥ����Ф��4(����������������}م�Ք��͕�����Ɍ���}���Ġ�4(��������������������}م�Ք���5I���}%ID�}1=	1}%ID��4(�����������������ɕ�������27F'BF�RWF�V�F�6F���&�6VGW&R�Т6V�b��g&3c3�6�E�WF���W��G�R�&��6��V�B�РТ2&��6�V�F��vR&RF��PТv���R��B��'�f�VRb���F��W%�f�%�F��V�WB���Т�'�f�VR�6V�b��g&3c3��'��Т�b��'�f�VRb�e$3c3��%�t��$���%��Т'&V�27F���Ɩ�r�'H]][�X�][ۈ���Y\�K�B��[��Y��͌���Y�]]
�^W�\K����ZY
CB�B������[�[�H\�HۙCB��[H��
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B�\�LWݘ[YHH�[��Y��͌��\�LJ
CB�Y�
\�LWݘ[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]Hon procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):
                break  # stop polling irq1 and quit the timeout loop.

 �������͕�����Ɍ���}���}��Ѡ����}�������������ե��4(4(����������������չѥ��ݔ��ɔ�����4(��������ݡ������Ѐ�����}م�Ք����Ā���ѥ���}���}ѥ����Ф��4(����������������}م�Ք��͕�����Ɍ���}���Ġ�4(��������������������}م�Ք���5I���}%ID�}1=	1}%ID��4(�����������������ɕ�������ѽ�������������ā�����եЁѡ��ѥ����Ё�����4(4(����������������}c3�6�E�WF���W��G�R�&��6��V�B�РТ2&��6�V�F��vR&RF��PТv���R��B��'�f�VRb���F��W%�f�%�F��V�WB���Т�'�f�VR�6V�b��g&3c3��'��Т�b��'�f�VRb�e$3c3��%�t��$���%��Т'&V�27F���Ɩ�r�'�BV�BF�RF��V�WB����РТ�b��'�f�VRb���F��\K����ZY
CB�B������[�[�H\�HۙCB��[H��
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B�\�LWݘ[YHH�[��Y��͌��\�LJ
CB�Y�
\�LWݘ[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B�
        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):
                break  # stop polling irq1 and quit the timeout loop.

        if (irq1_value & (1 << timer_for_timeout)):
            # thh�չѥ��ݔ��ɔ�����4(��������ݡ������Ѐ�����}م�Ք����Ā���ѥ���}���}ѥ����Ф��4(����������������}م�Ք��͕�����Ɍ���}���Ġ�4(��������������������}م�Ք���5I���}%ID�}1=	1}%ID��4(�����������������ɕ�������ѽ�������������ā�����եЁѡ��ѥ����Ё�����4(4(����������������}م�Ք����Ā���ѥ���}���}ѥ����Ф��4(��������������ѡ�́������ѕ́��ѥ�PТv���R��B��'�f�VRb���F��W%�f�%�F��V�WB���Т�'�f�VR�6V�b��g&3c3��'��Т�b��'�f�VRb�e$3c3��%�t��$���%��Т'&V�27F���Ɩ�r�'�BV�BF�RF��V�WB����РТ�b��'�f�VRb���F��W%�f�%�F��V�WB���Т2F��2��F�6FW2F��V�W@Т��
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B�\�LWݘ[YHH�[��Y��͌��\�LJ
CB�Y�
\�LWݘ[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����@& (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):
                break  # stop polling irq1 and quit the timeout loop.

        if (irq1_value & (1 << timer_for_timeout)):
            # this indicates a timeout
            return 0  # we have no authkܗ�[Y[�]
JN�B�\�LWݘ[YHH�[��Y��͌��\�LJ
CB�Y�
\�LWݘ[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

   \�LWݘ[YHH�[��Y��͌��\�LJ
CB�Y�
\�LWݘ[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status iq�[YHH�[��Y��͌��\�LJ
CB�Y�
\�LWݘ[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, iM���\�LJ
CB�Y�
\�LWݘ[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in hY�
\�LWݘ[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentic�[YH	�Q��͌��T�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
$�LW��АS�T�JN�B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = B���XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_reah��XZ�����[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_RE[�[��\�LH[�]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
      ]Z]H[Y[�]���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status���B�B�Y�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUPY�
\�LWݘ[YH	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)
	�
H[Y\�ٛܗ�[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_��[Y[�]
JN�B��\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):�\�[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc[�X�]\�H[Y[�]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MF]]B��]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MFRC630_REG_STATUS�]\����Hve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MFRC630_REG_STATUS, 0)

    def dve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MFRC630_REG_STATUS, 0)

    def format_block(sela���ѥ��4(4(�����������х��́�́��݅�́م������Ё�͕́ЁѼ��������͔������ѡ��ѥ��ѥ��������ɔ�4(���������х��̀�͕�����Ɍ���}ɕ��}ɕ��5I���}I}MQQUL�4(��������ɕ��ɸ���х��̀��5I���}MQQUM}IeAQ<�}=8�4(4(����������Ɍ���}5}����Ѡ�͕����4(������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I}MQQUL����4(4(����������ɵ��}������͕���������������Ѡ�27FGW2�2�v�2fƖB��B�26WBF���66R�bWF�V�F�6F���f��W&R�Т7FGW2�6V�b��g&3c3�&VE�&Vr��e$3c3�$Tu�5DEU2�Т&WGW&��7FGW2b�e$3c3�5DEU5�5%�D����РТFVb�g&3c3��e�FVWF��6V�b��Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu�5DEU2��РТFVbf�&�E�&��6��6V�b�&��6���V�wF���Т&WE�f�^\��[Y]\��]�[��\�Hو]][�X�][ۈ�Z[\�K�B��]\�H�[��Y��͌�ܙXYܙY�Q��͌�ԑQ���UT�CB��]\��
�]\�	�Q��͌���UT��ԖT�W�ӊCB�B�Y�Y��͌��Q��X]]
�[�N�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ���UT�
CB�B�Y��ܛX]؛����[�����[��
N�B��]ݘ[H��B� set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MFRC630_REG_STATUS, 0)

    def format_block(self, block, length):
        ret_val = ""
        for i in range(0,������ѡ��ѥ��ѥ��������ɔ�4(���������х��̀�͕�����Ɍ���}ɕ��}ɕ��5I���}I}MQQUL�4(��������ɕ��ɸ���х��̀��5I���}MQQUM}IeAQ<�}=8�4(4(����������Ɍ���}5}����Ѡ�͕����4(������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I}MQQUL����4(4(����������ɵ��}������͕���������������Ѡ��4(��������ɕ�}م��􀈈4(����������ȁ�����Ʌ�����������Ѡ��4(��������f��W&R�Т7FGW2�6V�b��g&3c3�&VE�&Vr��e$3c3�$Tu�5DEU2�Т&WGW&��7FGW2b�e$3c3�5DEU5�5%�D����РТFVb�g&3c3��e�FVWF��6V�b��Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu�5DEU2��РТFVbf�&�E�&��6��6V�b�&��6���V�wF���Т&WE�f��" Тf�"���&�vR���V�wF���Т�b�&��6���]\�H�[��Y��͌�ܙXYܙY�Q��͌�ԑQ���UT�CB��]\��
�]\�	�Q��͌���UT��ԖT�W�ӊCB�B�Y�Y��͌��Q��X]]
�[�N�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ���UT�
CB�B�Y��ܛX]؛����[�����[��
N�B��]ݘ[H��B��܈H[��[��J[��
N�B�Y�
�����WHM�N�B�,f.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MFRC630_REG_STATUS, 0)

    def format_block(self, block, length):
        ret_val = ""
        for i in range(0, length):
            if (block[i] < 16):
                ret_vi���5I���}I}MQQUL�4(��������ɕ��ɸ���х��̀��5I���}MQQUM}IeAQ<�}=8�4(4(����������Ɍ���}5}����Ѡ�͕����4(������͕�����Ɍ���}�ɥѕ}ɕ��5I���}I}MQQUL����4(4(����������ɵ��}������͕���������������Ѡ��4(��������ɕ�}م��􀈈4(����������ȁ�����Ʌ�����������Ѡ��4(���������������������m�t����ؤ�4(����������������ɕ�}م���􀠈���������DEU2�Т&WGW&��7FGW2b�e$3c3�5DEU5�5%�D����РТFVb�g&3c3��e�FVWF��6V�b��Т6V�b��g&3c3�w&�FU�&Vr��e$3c3�$Tu�5DEU2��РТFVbf�&�E�&��6��6V�b�&��6���V�wF���Т&WE�f��" Тf�"���&�vR���V�wF���Т�b�&��6�����b��Т&WE�f����#W�"R&��6���ҐТ�]\��
�]\�	�Q��͌���UT��ԖT�W�ӊCB�B�Y�Y��͌��Q��X]]
�[�N�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ���UT�
CB�B�Y��ܛX]؛����[�����[��
N�B��]ݘ[H��B��܈H[��[��J[��
N�B�Y�
�����WHM�N�B��]ݘ[
�H
�	^�	H�����WJCB�[�:
  ��͌���UT��ԖT�W�ӊCB�B�Y�Y��͌��Q��X]]
�[�N�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ���UT�
CB�B�Y��ܛX]؛����[�����[��
N�B��]ݘ[H��B��܈H[��[��J[��
N�B�Y�
�����WHM�N�B��]ݘ[
�H
�	^�	H�����WJCB�[�:
                revT�W�ӊCB�B�Y�Y��͌��Q��X]]
�[�N�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ���UT�
CB�B�Y��ܛX]؛����[�����[��
N�B��]ݘ[H��B��܈H[��[��J[��
N�B�Y�
�����WHM�N�B��]ݘ[
�H
�	^�	H�����WJCB�[�:
                ret_val += ("%x " %Y�Y��͌��Q��X]]
�[�N�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ���UT�
CB�B�Y��ܛX]؛����[�����[��
N�B��]ݘ[H��B��܈H[��[��J[��
N�B�Y�
�����WHM�N�B��]ݘ[
�H
�	^�	H�����WJCB�[�:
                ret_val += ("%x " % block[i])
    !X]]
�[�N�B��[��Y��͌��ܚ]WܙY�Q��͌�ԑQ���UT�
CB�B�Y��ܛX]؛����[�����[��
N�B��]ݘ[H��B��܈H[��[��J[��
N�B�Y�
�����WHM�N�B��]ݘ[
�H
�	^�	H�����WJCB�[�:
                ret_val += ("%x " % block[i])
        return ret_vaH�[��Y��͌��ܚ]WܙY�Q��͌�ԑQ���UT�
CB�B�Y��ܛX]؛����[�����[��
N�B��]ݘ[H��B��܈H[��[��J[��
N�B�Y�
�����WHM�N�B��]ݘ[
�H
�	^�	H�����WJCB�[�:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
w&�FU�&Vr��e$3c3�$Tu�5DEU2��РТFVbf�&�E�&��6��6V�b�&��6���V�wF���Т&WE�f��" Тf�"���&�vR���V�wF���Т�b�&��6�����b��Т&WE�f����#W�"R&��6���ҐТV�6:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
8�e_reg(MFRC630_REG_STATUS, 0)

    def format_block(self, block, length):
        ret_val = ""
        for i in range(0, length):
            if (block[i] < 16):
                ret_val += ("0%x " % block[i])
            else:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
8�e_reg(MFRC630_REG_STATUS, 0)

    def format_block(self, block, length):
        ret_val = ""
        for i in range(0, length):
            if (block[i] < 16):
                ret_val += ("0%x " % block[i])
            else:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
8�e_reg(MFRC630_RE