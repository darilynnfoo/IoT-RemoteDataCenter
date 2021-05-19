W7VÇB7V6‚F†@Ð¢2vRFòæ÷BÆ÷6RF†R&—BvR§W7B6WB–bvR†fR collision.
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

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH€¨€Ì€¬€Ä4(4(€€€€€€€Í•±˜¹ÁÉ¥¹Ñ}‘•‰Õœ ‰á¥Ð…Í…‘”±½½À¹È¸€•è€ˆ€”…Í…‘•}±•Ù•°¤4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÁÉ¥¹Ñ}‰±½¬¡Õ¥°€ÄÀ¤4(4(€€€€€€€É•ÑÕÉ¸€À€€Œ•ÑÑ¥¹œ„U%™…¥±•¸4(4(€€€‘•˜µ™ÉŒØÌÁ}5}…ÕÑ ¡Í•±˜°Õ¥°­•å}ÑåÁ”°‰±½¬¤è4(€€€€€€€€Œ¹…‰±”Ñ¡”É¥¡Ð¥¹Ñ•ÉÉÕÁÑÌ¸4(4(€€€€†B'ö–çFW""àÐ¢&W@  # configure a timeout timer.   self.print_debug("Exit cascade loop nr. %d: " % cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_fbug("Exit cascade loop nr. %d: " % cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  e loop nr. %d: " % cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match t`% cascade_level)
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interr
        self.mfrc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

       !frc630_print_block(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to dck(uid, 10)

        return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interru       return 0  # getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and tic getting a UID failed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENailed.

    def mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
   & mfrc630_MF_auth(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include Eh(self, uid, key_type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
 /type, block):
        # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc6       # Enable the right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFPthe right interrupts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN,5pts.

    !€‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_‰Á½¥¹Ñ•Èˆ¸4(€€€€€€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFR@€€€€€€€€€€É•ÐÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IÈÛÛ™šYÝ\™HH[Y[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
        skY[ut timer.
        timer_for_timeout = 0  # should match the enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
        self.mfrc630_writh€€€€€€€Ñ¥µ•É}™½É}Ñ¥µ•½ÕÐ€ô€À€€ŒÍ¡½Õ±µ…Ñ Ñ¡”•¹…‰±•¥¹Ñ•ÉÉÕÁÐ¸4(4(€€€€€€€€Œ½É‘¥¹œÑ¼‘…Ñ…Í¡••Ð%¹Ñ•ÉÉÕÁÐ½¸¥‘±”…¹Ñ¥µ•ÈÝ¥Ñ 5UQ!9P°‰ÕÐ±•ÑÌ4(€€€€€€€€Œ¥¹±Õ‘”II=H…ÌÝ•±°¸4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I}%IDÁ8°5IØÌÁ}%IDÁ9}%1}%IE8ð5IØÌÁ}%IDÁ9}II}%IE8¤4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I%÷F–ÖV÷WBÒ26†÷VÆBÖF6‚F†RVæ&ÆVB–çFW''WBàÐ Ð¢266÷&F–ærFòFF6†VWB–çFW''WBöâ–FÆRæBF–ÖW"v—F‚ÔdUD„TåBÂ'WBÆWG0Ð¢2–æ6ÇVFRU%$õ"2vVÆÂàÐ¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuô•%TâÂÔe$3c3ô•%Tåô”DÄUô•%TâÂÔe$3c3ô•%TåôU%%ô•%TâÐ¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuô•%TâÂÔe$3c3ÚÝ[X]ÚH[˜X›Y[\œ\ƒBƒBˆÈXØÛÜ™[™ÈÈ]\ÚY][\œ\ÛˆYH[™[Y\ˆÚ]QUUS•]]ÃBˆÈ[˜ÛYHT”“Ôˆ\ÈÙ[ƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LS‹Q”ÍŒÌÒT”LS—ÒQWÒT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒe enabled interrupt.

        # According to datasheet Interrupt on idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
        self.mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)  # only treÁÐ¸4(4(€€€€€€€€Œ½É‘¥¹œÑ¼‘…Ñ…Í¡••Ð%¹Ñ•ÉÉÕÁÐ½¸¥‘±”…¹Ñ¥µ•ÈÝ¥Ñ 5UQ!9P°‰ÕÐ±•ÑÌ4(€€€€€€€€Œ¥¹±Õ‘”II=H…ÌÝ•±°¸4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I}%IDÁ8°5IØÌÁ}%IDÁ9}%1}%IE8ð5IØÌÁ}%IDÁ9}II}%IE8¤4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I}%IDÅ8°5IØÌÁ}%IDÅ9}Q%5HÁ}%IE8¤€€Œ½¹±äÑÉ¥•È½¸Ñ¥µ•È™266÷&F–ærFòFF6†VWB–çFW''WBöâ–FÆRæBF–ÖW"v—F‚ÔdUD„TåBÂ'WBÆWG0Ð¢2–æ6ÇVFRU%$õ"2vVÆÂàÐ¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuô•%TâÂÔe$3c3ô•%Tåô”DÄUô•%TâÂÔe$3c3ô•%TåôU%%ô•%TâÐ¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuô•%TâÂÔe$3c3ô•%TåõD”ÔU#ô•%Tâ’2öæÇ’G&–vvW"öâF–ÖW"f÷"—'Ð Ð¢ \ÚY][\œ\ÛˆYH[™[Y\ˆÚ]QUUS•]]ÃBˆÈ[˜ÛYHT”“Ôˆ\ÈÙ[ƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LS‹Q”ÍŒÌÒT”LS—ÒQWÒT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈn idle and timer with MFAUTHENT, but lets
        # include ERROR as well.
        self.mfrc630_write_reg(MFRC630_REG_IRQ0EN, MFRC630_IRQ0EN_IDLE_IRQEN | MFRC630_IRQ0EN_ERR_IRQEN)
        self.mfrc630_write_reg(MFRC630_REG_IRQ1EN, MFRC630_IRQ1EN_TIMER0_IRQEN)  # only trigger on timer for irq1

        # Set timer to 221 kHz clock, staÝ¥Ñ 5UQ!9P°‰ÕÐ±•ÑÌ4(€€€€€€€€Œ¥¹±Õ‘”II=H…ÌÝ•±°¸4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I}%IDÁ8°5IØÌÁ}%IDÁ9}%1}%IE8ð5IØÌÁ}%IDÁ9}II}%IE8¤4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I}%IDÅ8°5IØÌÁ}%IDÅ9}Q%5HÁ}%IE8¤€€Œ½¹±äÑÉ¥•È½¸Ñ¥µ•È™½È¥ÉÄÄ4(4(€€€€€€€€ŒM•ÐÑ¥µ•ÈÑ¼€ÈÈÄ­!è±½¬°ÍÑ…ÉÐ…ÐÑ¡”•¹½’'WBÆWG0Ð¢2–æ6ÇVFRU%$õ"2vVÆÂàÐ¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuô•%TâÂÔe$3c3ô•%Tåô”DÄUô•%TâÂÔe$3c3ô•%TåôU%%ô•%TâÐ¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuô•%TâÂÔe$3c3ô•%TåõD”ÔU#ô•%Tâ’2öæÇ’G&–vvW"öâF–ÖW"f÷"—'Ð Ð¢26WBF–ÖW"Fò##´‡¢6Æö6²Â7F'BBF†RVæBöbG‚àÐ¢6TÈ[˜ÛYHT”“Ôˆ\ÈÙ[ƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LS‹Q”ÍŒÌÒT”LS—ÒQWÒT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimTˆ\ÈÙ[ƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LS‹Q”ÍŒÌÒT”LS—ÒQWÒT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(tÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LS‹Q”ÍŒÌÒT”LS—ÒQWÒT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout'ÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LS‹Q”ÍŒÌÒT”LS—ÒQWÒT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTRLÌÔ‘Q×ÒT”LS‹Q”ÍŒÌÒT”LS—ÒQWÒT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRÍŒÌÒT”LS—ÒQWÒT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_STBT”QSˆQ”ÍŒÌÒT”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
   T”LS—ÑT”—ÒT”QSŠCBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waitcBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = œ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2Q”ÍŒÌÔ‘Q×ÒT”LQS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # QS‹Q”ÍŒÌÒT”LQS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to QS—ÕSQTŒÒT”QSŠHÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that xÈÛ›HšYÙÙ\ˆÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait fÛˆ[Y\ˆ›Üˆ\œLCBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of |CBƒBˆÈÙ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

       ][Y\ˆÈŒŒHÒˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timbˆÛØÚËÝ\]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(tiX]H[™ÙˆƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout,#ƒBˆÙ[‹›Yœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 tiYœ˜ÍŒÌÝimer_set_control(timer_for_timeout, MFRC630_TCONTROL_CLK_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 ticks of 5 usec is!•Ñ}½¹ÑÉ½°¡Ñ¥µ•É}™½É}Ñ¥µ•½ÕÐ°5IØÌÁ}Q=9QI=1}1-|ÈÄÅ-!hð5IØÌÁ}Q=9QI=1}MQIQ}Qa}9¤4(€€€€€€€€ŒÉ…µ”Ý…¥Ñ¥¹œÑ¥µ”è]P€ô€ ÈÔØà€ÄØ½™Œ¤à€È]$4(€€€€€€€€Œ]$‘•™…Õ±ÑÌÑ¼™½ÕÈ¸¸¸Í¼Ñ¡…ÐÝ½Õ±µ•…¸Ý…¥Ð™½È„µ…á¥µÕ´½˜ø€ÕµÌ4(4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}Ñ¥µ•É}Í•Ñ}É•±½…¡Ñ¥µ•É}™½É}Ñ¥µ•½ÕÐ°€ÈÀÀÀ¤€€Œ€ÈÀÀÀÑ¥­Ì½˜€ÔÕÍ•Œ¥Ì€ÄÀµÌ¸4(€€€€€€€¥öf÷%÷F–ÖV÷WBÂÔe$3c3õD4ôåE$ôÅô4Äµó#´…¢ÂÔe$3c3õD4ôåE$ôÅõ5D%EõE…ôTäBÐ¢2g&ÖRv—F–ærF–ÖS¢euBÒƒ#Sb‚böf2’‚"etÐ¢2et’FVfVÇG2Fòf÷W"âââ6òF†Bv÷VÆBÖVâv—Bf÷"Ö†–×VÒöbâV×0Ð Ð¢6VÆbæÖg&3c3÷F–ÖW%÷6WE÷&VÆöB‡F–ÖW%öf÷%÷F–ÖV÷WBÂ#’2#F–6·2öbRW6V2—2×2àÐ¢6VÆbæÖg&3c3÷F–ÖPÍŒÌÕÓÓ•“ÓÐÓ×ÌŒLRÒˆQ”ÍŒÌÕÓÓ•“ÓÔÕT•ÕÑS‘
CBˆÈœ˜[YHØZ][™È[YNˆ•ÕH
MˆM‹Ù˜ÊHˆ•ÒCBˆÈ•ÒHY˜][ÈÈ›Ý\‹‹‹ˆÛÈ]ÛÝ[YX[ˆØZ]›ÜˆHX^[][HÙˆˆ[\ÃBƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ü™[ØY
[Y\—Ù›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y[_211KHZ | MFRC630_TCONTROL_START_TX_END)
        # Frame waiting time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 ticks of 5 usec is 10 ms.
        self.mfrc630_timer_set_value(timer_for_timeout, 20Á}Q=9QI=1}MQIQ}Qa}9¤4(€€€€€€€€ŒÉ…µ”Ý…¥Ñ¥¹œÑ¥µ”è]P€ô€ ÈÔØà€ÄØ½™Œ¤à€È]$4(€€€€€€€€Œ]$‘•™…Õ±ÑÌÑ¼™½ÕÈ¸¸¸Í¼Ñ¡…ÐÝ½Õ±µ•…¸Ý…¥Ð™½È„µ…á¥µÕ´½˜ø€ÕµÌ4(4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}Ñ¥µ•É}Í•Ñ}É•±½…¡Ñ¥µ•É}™½É}Ñ¥µ•½ÕÐ°€ÈÀÀÀ¤€€Œ€ÈÀÀÀÑ¥­Ì½˜€ÔÕÍ•Œ¥Ì€ÄÀµÌ¸4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}Ñ¥µ•É}Í•Ñ}Ù…±Õ”¡Ñ¥µ•É}™½É}Ñ¥µ•½ÕÐ°€ÈÀÀÀ¤4(4(€€€€€€€…õE…ôTäBÐ¢2g&ÖRv—F–ærF–ÖS¢euBÒƒ#Sb‚böf2’‚"etÐ¢2et’FVfVÇG2Fòf÷W"âââ6òF†Bv÷VÆBÖVâv—Bf÷"Ö†–×VÒöbâV×0Ð Ð¢6VÆbæÖg&3c3÷F–ÖW%÷6WE÷&VÆöB‡F–ÖW%öf÷%÷F–ÖV÷WBÂ#’2#F–6·2öbRW6V2—2×2àÐ¢6VÆbæÖg&3c3÷F–ÖW%÷6WE÷fÇVR‡F–ÖW%öf÷%÷F–ÖV÷WBÂ#Ð Ð¢—'÷fÇVRÒ Ð ØÈœ˜[YHØZ][™È[YNˆ•ÕH
MˆM‹Ù˜ÊHˆ•ÒCBˆÈ•ÒHY˜][ÈÈ›Ý\‹‹‹ˆÛÈ]ÛÝ[YX[ˆØZ]›ÜˆHX^[][HÙˆˆ[\ÃBƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ü™[ØY
[Y\—Ù›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›YŸ time: FWT = (256 x 16/fc) x 2 FWI
        # FWI defaults to four... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 ticks of 5 usec is 10 ms.
        self.mfrc630_timer_set_value(timer_for_timeout, 2000)

        irq1_value = 0

        self.mfrc630_clear_irq0(Øà€ÄØ½™Œ¤à€È]$4(€€€€€€€€Œ]$‘•™…Õ±ÑÌÑ¼™½ÕÈ¸¸¸Í¼Ñ¡…ÐÝ½Õ±µ•…¸Ý…¥Ð™½È„µ…á¥µÕ´½˜ø€ÕµÌ4(4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}Ñ¥µ•É}Í•Ñ}É•±½…¡Ñ¥µ•É}™½É}Ñ¥µ•½ÕÐ°€ÈÀÀÀ¤€€Œ€ÈÀÀÀÑ¥­Ì½˜€ÔÕÍ•Œ¥Ì€ÄÀµÌ¸4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}Ñ¥µ•É}Í•Ñ}Ù…±Õ”¡Ñ¥µ•É}™½É}Ñ¥µ•½ÕÐ°€ÈÀÀÀ¤4(4(€€€€€€€¥ÉÄÅ}Ù…±Õ”€ô€À4(4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}±•…É}¥ÉÄÀ ¤€€Œ±•…È¥ÉÄÀ5tÐ¢2et’FVfVÇG2Fòf÷W"âââ6òF†Bv÷VÆBÖVâv—Bf÷"Ö†–×VÒöbâV×0Ð Ð¢6VÆbæÖg&3c3÷F–ÖW%÷6WE÷&VÆöB‡F–ÖW%öf÷%÷F–ÖV÷WBÂ#’2#F–6·2öbRW6V2—2×2àÐ¢6VÆbæÖg&3c3÷F–ÖW%÷6WE÷fÇVR‡F–ÖW%öf÷%÷F–ÖV÷WBÂ#Ð Ð¢—'÷fÇVRÒ Ð Ð¢6VÆbæÖg&3c3ö6ÆV%ö—'‚’26ÆV"—' Ð¢6VÆbæÖfHY˜][ÈÈ›Ý\‹‹‹ˆÛÈ]ÛÝ[YX[ˆØZ]›ÜˆHX^[][HÙˆˆ[\ÃBƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ü™[ØY
[Y\—Ù›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
... so that would mean wait for a maximum of ~ 5ms

        self.mfrc630_timer_set_reload(timer_for_timeout, 2000)  # 2000 ticks of 5 usec is 10 ms.
        self.mfrc630_timer_set_value(timer_for_timeout, 2000)

        irq1_value = 0

        self.mfrc630_clear_irq0()  # clear irq0
        self.mfrc630_clear_irq1()  # clear irq9YX[ˆØZ]›ÜˆHX^[][HÙˆˆ[\ÃBƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ü™[ØY
[Y\—Ù›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # stHX^[][HÙˆˆ[\ÃBƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ü™[ØY
[Y\—Ù›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentilÃBƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ü™[ØY
[Y\—Ù›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ü™[ØY
[Y\—Ù›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.lÙ]Ü™[ØY
[Y\—Ù›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(Y›Ü—Ý[Y[Ý]Œ
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block,
HÈŒXÚÜÈÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

       (ÙˆH\ÙXÈ\ÈL\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we\ËƒBˆÙ[‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
    #‹›Yœ˜ÍŒÌÝ[Y\—ÜÙ]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (ir\Ù]Ý˜[YJ[Y\—Ù›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 <<!›Ü—Ý[Y[Ý]Œ
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeo|
CBƒBˆ\œLWÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
           WÝ˜[YHHBƒBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = seHÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1((ÌØÛX\—Ú\œL

HÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            ihÈÛX\ˆ\œLBˆÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFXÙ[‹›Yœ˜ÍŒÌØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBALØÛX\—Ú\œLJ
  # clear irq1

        # start the authentication procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):
         €Œ±•…È¥ÉÄÄ4(4(€€€€€€€€ŒÍÑ…ÉÐÑ¡”…ÕÑ¡•¹Ñ¥…Ñ¥½¸ÁÉ½•‘ÕÉ”¸4(€€€€€€€Í•±˜¹µ™ÉŒØÌÁ}µ‘}…ÕÑ ¡­•å}ÑåÁ”°‰±½¬°Õ¥¤4(4(€€€€€€€€Œ‰±½¬Õ¹Ñ¥°Ý”…É”‘½¹”4(€€€€€€€Ý¡¥±”¹½Ð€¡¥ÉÄÅ}Ù…±Õ”€˜€ Ä€ððÑ¥µ•É}™½É}Ñ¥µ•½ÕÐ¤¤è4(€€€€€€€€€€€¥ÉÄÅ}Ù…±Õ”€ôÍ•±˜¹µ™ÉŒØÌÁ}¥ÉÄÄ ¤4(€€€€€€€€€€€¥˜€¡¥ÉÄÅ}Ù…±Õ”€˜5IØÌÁ}%IDÅ}1=	1}%ID¤è4(€€€€€€€€€€€€€€€‰É•…¬€€Œ€¢27F'BF†RWF†VçF–6F–öâ&ö6VGW&RàÐ¢6VÆbæÖg&3c3ö6ÖEöWF‚†¶W•÷G—RÂ&Æö6²ÂV–BÐ Ð¢2&Æö6²VçF–ÂvR&RFöæPÐ¢v†–ÆRæ÷B†—'÷fÇVRbƒÃÂF–ÖW%öf÷%÷F–ÖV÷WB’“ Ð¢—'÷fÇVRÒ6VÆbæÖg&3c3ö—'‚Ð¢–b†—'÷fÇVRbÔe$3c3ô•%ôtÄô$Åô•%“ Ð¢'&V²27F÷öÆÆ–ær—'H]][XØ][Ûˆ›ØÙY\™KƒBˆÙ[‹›Yœ˜ÍŒÌØÛYØ]]
Ù^WÝ\K›ØÚËZY
CBƒBˆÈ›ØÚÈ[[ÙH\™HÛ™CBˆÚ[H›Ý
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆ\œLWÝ˜[YHHÙ[‹›Yœ˜ÍŒÌÚ\œLJ
CBˆYˆ
\œLWÝ˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]Hon procedure.
        self.mfrc630_cmd_auth(key_type, block, uid)

        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):
                break  # stop polling irq1 and quit the timeout loop.

 €€€€€€Í•±˜¹µ™ÉŒØÌÁ}µ‘}…ÕÑ ¡­•å}ÑåÁ”°‰±½¬°Õ¥¤4(4(€€€€€€€€Œ‰±½¬Õ¹Ñ¥°Ý”…É”‘½¹”4(€€€€€€€Ý¡¥±”¹½Ð€¡¥ÉÄÅ}Ù…±Õ”€˜€ Ä€ððÑ¥µ•É}™½É}Ñ¥µ•½ÕÐ¤¤è4(€€€€€€€€€€€¥ÉÄÅ}Ù…±Õ”€ôÍ•±˜¹µ™ÉŒØÌÁ}¥ÉÄÄ ¤4(€€€€€€€€€€€¥˜€¡¥ÉÄÅ}Ù…±Õ”€˜5IØÌÁ}%IDÅ}1=	1}%ID¤è4(€€€€€€€€€€€€€€€‰É•…¬€€ŒÍÑ½ÀÁ½±±¥¹œ¥ÉÄÄ…¹ÅÕ¥ÐÑ¡”Ñ¥µ•½ÕÐ±½½À¸4(4(€€€€€€€¥˜€¡¥ÉÄÅ}c3ö6ÖEöWF‚†¶W•÷G—RÂ&Æö6²ÂV–BÐ Ð¢2&Æö6²VçF–ÂvR&RFöæPÐ¢v†–ÆRæ÷B†—'÷fÇVRbƒÃÂF–ÖW%öf÷%÷F–ÖV÷WB’“ Ð¢—'÷fÇVRÒ6VÆbæÖg&3c3ö—'‚Ð¢–b†—'÷fÇVRbÔe$3c3ô•%ôtÄô$Åô•%“ Ð¢'&V²27F÷öÆÆ–ær—'æBV—BF†RF–ÖV÷WBÆö÷àÐ Ð¢–b†—'÷fÇVRbƒÃÂF–Ý\K›ØÚËZY
CBƒBˆÈ›ØÚÈ[[ÙH\™HÛ™CBˆÚ[H›Ý
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆ\œLWÝ˜[YHHÙ[‹›Yœ˜ÍŒÌÚ\œLJ
CBˆYˆ
\œLWÝ˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒB
        # block until we are done
        while not (irq1_value & (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):
                break  # stop polling irq1 and quit the timeout loop.

        if (irq1_value & (1 << timer_for_timeout)):
            # thhÕ¹Ñ¥°Ý”…É”‘½¹”4(€€€€€€€Ý¡¥±”¹½Ð€¡¥ÉÄÅ}Ù…±Õ”€˜€ Ä€ððÑ¥µ•É}™½É}Ñ¥µ•½ÕÐ¤¤è4(€€€€€€€€€€€¥ÉÄÅ}Ù…±Õ”€ôÍ•±˜¹µ™ÉŒØÌÁ}¥ÉÄÄ ¤4(€€€€€€€€€€€¥˜€¡¥ÉÄÅ}Ù…±Õ”€˜5IØÌÁ}%IDÅ}1=	1}%ID¤è4(€€€€€€€€€€€€€€€‰É•…¬€€ŒÍÑ½ÀÁ½±±¥¹œ¥ÉÄÄ…¹ÅÕ¥ÐÑ¡”Ñ¥µ•½ÕÐ±½½À¸4(4(€€€€€€€¥˜€¡¥ÉÄÅ}Ù…±Õ”€˜€ Ä€ððÑ¥µ•É}™½É}Ñ¥µ•½ÕÐ¤¤è4(€€€€€€€€€€€€ŒÑ¡¥Ì¥¹‘¥…Ñ•Ì„Ñ¥æPÐ¢v†–ÆRæ÷B†—'÷fÇVRbƒÃÂF–ÖW%öf÷%÷F–ÖV÷WB’“ Ð¢—'÷fÇVRÒ6VÆbæÖg&3c3ö—'‚Ð¢–b†—'÷fÇVRbÔe$3c3ô•%ôtÄô$Åô•%“ Ð¢'&V²27F÷öÆÆ–ær—'æBV—BF†RF–ÖV÷WBÆö÷àÐ Ð¢–b†—'÷fÇVRbƒÃÂF–ÖW%öf÷%÷F–ÖV÷WB’“ Ð¢2F†—2–æF–6FW2F–ÖV÷W@Ð¢›Ý
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆ\œLWÝ˜[YHHÙ[‹›Yœ˜ÍŒÌÚ\œLJ
CBˆYˆ
\œLWÝ˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙ@& (1 << timer_for_timeout)):
            irq1_value = self.mfrc630_irq1()
            if (irq1_value & MFRC630_IRQ1_GLOBAL_IRQ):
                break  # stop polling irq1 and quit the timeout loop.

        if (irq1_value & (1 << timer_for_timeout)):
            # this indicates a timeout
            return 0  # we have no authkÜ—Ý[Y[Ý]
JNƒBˆ\œLWÝ˜[YHHÙ[‹›Yœ˜ÍŒÌÚ\œLJ
CBˆYˆ
\œLWÝ˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

   \œLWÝ˜[YHHÙ[‹›Yœ˜ÍŒÌÚ\œLJ
CBˆYˆ
\œLWÝ˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status iq˜[YHHÙ[‹›Yœ˜ÍŒÌÚ\œLJ
CBˆYˆ
\œLWÝ˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, iMŒÌÚ\œLJ
CBˆYˆ
\œLWÝ˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in hYˆ
\œLWÝ˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentic˜[YH	ˆQ”ÍŒÌÒT”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
$”LWÑÓÐSÒT”JNƒBˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = Bˆœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_reahœ™XZÈÈÝÜÛ[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_RE[Û[™È\œLH[™]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
      ]Z]H[Y[Ý]ÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (statusÛÜƒBƒBˆYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUPYˆ
\œLWÝ˜[YH	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)
	ˆ
H[Y\—Ù›Ü—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_—Ý[Y[Ý]
JNƒBˆÈ\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):È\È[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc[™XØ]\ÈH[Y[Ý]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MF]]Bˆ™]\›ˆÈÙHve no authentication

        # status is always valid, it is set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MFRC630_REG_STATUS™]\›ˆÈÙHve no authentication

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

    def format_block(sela¥…Ñ¥½¸4(4(€€€€€€€€ŒÍÑ…ÑÕÌ¥Ì…±Ý…åÌÙ…±¥°¥Ð¥ÌÍ•ÐÑ¼€À¥¸…Í”½˜…ÕÑ¡•¹Ñ¥…Ñ¥½¸™…¥±ÕÉ”¸4(€€€€€€€ÍÑ…ÑÕÌ€ôÍ•±˜¹µ™ÉŒØÌÁ}É•…‘}É•œ¡5IØÌÁ}I}MQQUL¤4(€€€€€€€É•ÑÕÉ¸€¡ÍÑ…ÑÕÌ€˜5IØÌÁ}MQQUM}IeAQ<Å}=8¤4(4(€€€‘•˜µ™ÉŒØÌÁ}5}‘•…ÕÑ ¡Í•±˜¤è4(€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I}MQQUL°€À¤4(4(€€€‘•˜™½Éµ…Ñ}‰±½¬¡Í•±˜°‰±½¬°±•¹Ñ ¦27FGW2—2Çv—2fÆ–BÂ—B—26WBFò–â66RöbWF†VçF–6F–öâf–ÇW&RàÐ¢7FGW2Ò6VÆbæÖg&3c3÷&VE÷&Vr„Ôe$3c3õ$Tuõ5DEU2Ð¢&WGW&â‡7FGW2bÔe$3c3õ5DEU5ô5%•DóôôâÐ Ð¢FVbÖg&3c3ôÔeöFVWF‚‡6VÆb“ Ð¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuõ5DEU2ÂÐ Ð¢FVbf÷&ÖEö&Æö6²‡6VÆbÂ&Æö6²ÂÆVæwF‚“ Ð¢&WE÷fØ^\È˜[Y]\ÈÙ]È[ˆØ\ÙHÙˆ]][XØ][Ûˆ˜Z[\™KƒBˆÝ]\ÈHÙ[‹›Yœ˜ÍŒÌÜ™XYÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTÊCBˆ™]\›ˆ
Ý]\È	ˆQ”ÍŒÌÔÕUT×ÐÔ–TÌWÓÓŠCBƒBˆYˆYœ˜ÍŒÌÓQ—ÙX]]
Ù[ŠNƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTË
CBƒBˆYˆ›Ü›X]Ø›ØÚÊÙ[‹›ØÚË[™Ý
NƒBˆ™]Ý˜[HˆƒBˆ set to 0 in case of authentication failure.
        status = self.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MFRC630_REG_STATUS, 0)

    def format_block(self, block, length):
        ret_val = ""
        for i in range(0,½˜…ÕÑ¡•¹Ñ¥…Ñ¥½¸™…¥±ÕÉ”¸4(€€€€€€€ÍÑ…ÑÕÌ€ôÍ•±˜¹µ™ÉŒØÌÁ}É•…‘}É•œ¡5IØÌÁ}I}MQQUL¤4(€€€€€€€É•ÑÕÉ¸€¡ÍÑ…ÑÕÌ€˜5IØÌÁ}MQQUM}IeAQ<Å}=8¤4(4(€€€‘•˜µ™ÉŒØÌÁ}5}‘•…ÕÑ ¡Í•±˜¤è4(€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I}MQQUL°€À¤4(4(€€€‘•˜™½Éµ…Ñ}‰±½¬¡Í•±˜°‰±½¬°±•¹Ñ ¤è4(€€€€€€€É•Ñ}Ù…°€ô€ˆˆ4(€€€€€€€™½È¤¥¸É…¹” À°±•¹Ñ ¤è4(€€€€‚–öâf–ÇW&RàÐ¢7FGW2Ò6VÆbæÖg&3c3÷&VE÷&Vr„Ôe$3c3õ$Tuõ5DEU2Ð¢&WGW&â‡7FGW2bÔe$3c3õ5DEU5ô5%•DóôôâÐ Ð¢FVbÖg&3c3ôÔeöFVWF‚‡6VÆb“ Ð¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuõ5DEU2ÂÐ Ð¢FVbf÷&ÖEö&Æö6²‡6VÆbÂ&Æö6²ÂÆVæwF‚“ Ð¢&WE÷fÂÒ" Ð¢f÷"’–â&ævRƒÂÆVæwF‚“ Ð¢–b†&Æö6µ´Ý]\ÈHÙ[‹›Yœ˜ÍŒÌÜ™XYÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTÊCBˆ™]\›ˆ
Ý]\È	ˆQ”ÍŒÌÔÕUT×ÐÔ–TÌWÓÓŠCBƒBˆYˆYœ˜ÍŒÌÓQ—ÙX]]
Ù[ŠNƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTË
CBƒBˆYˆ›Ü›X]Ø›ØÚÊÙ[‹›ØÚË[™Ý
NƒBˆ™]Ý˜[HˆƒBˆ›ÜˆH[ˆ˜[™ÙJ[™Ý
NƒBˆYˆ
›ØÚÖÚWHMŠNƒBˆ,f.mfrc630_read_reg(MFRC630_REG_STATUS)
        return (status & MFRC630_STATUS_CRYPTO1_ON)

    def mfrc630_MF_deauth(self):
      self.mfrc630_write_reg(MFRC630_REG_STATUS, 0)

    def format_block(self, block, length):
        ret_val = ""
        for i in range(0, length):
            if (block[i] < 16):
                ret_vi•œ¡5IØÌÁ}I}MQQUL¤4(€€€€€€€É•ÑÕÉ¸€¡ÍÑ…ÑÕÌ€˜5IØÌÁ}MQQUM}IeAQ<Å}=8¤4(4(€€€‘•˜µ™ÉŒØÌÁ}5}‘•…ÕÑ ¡Í•±˜¤è4(€€€€€Í•±˜¹µ™ÉŒØÌÁ}ÝÉ¥Ñ•}É•œ¡5IØÌÁ}I}MQQUL°€À¤4(4(€€€‘•˜™½Éµ…Ñ}‰±½¬¡Í•±˜°‰±½¬°±•¹Ñ ¤è4(€€€€€€€É•Ñ}Ù…°€ô€ˆˆ4(€€€€€€€™½È¤¥¸É…¹” À°±•¹Ñ ¤è4(€€€€€€€€€€€¥˜€¡‰±½­m¥t€ð€ÄØ¤è4(€€€€€€€€€€€€€€€É•Ñ}Ù…°€¬ô€ ˆÀ•à€ˆ€”‰DEU2Ð¢&WGW&â‡7FGW2bÔe$3c3õ5DEU5ô5%•DóôôâÐ Ð¢FVbÖg&3c3ôÔeöFVWF‚‡6VÆb“ Ð¢6VÆbæÖg&3c3÷w&—FU÷&Vr„Ôe$3c3õ$Tuõ5DEU2ÂÐ Ð¢FVbf÷&ÖEö&Æö6²‡6VÆbÂ&Æö6²ÂÆVæwF‚“ Ð¢&WE÷fÂÒ" Ð¢f÷"’–â&ævRƒÂÆVæwF‚“ Ð¢–b†&Æö6µ¶•ÒÂb“ Ð¢&WE÷fÂ³Ò‚#W‚"R&Æö6µ¶•ÒÐ¢™]\›ˆ
Ý]\È	ˆQ”ÍŒÌÔÕUT×ÐÔ–TÌWÓÓŠCBƒBˆYˆYœ˜ÍŒÌÓQ—ÙX]]
Ù[ŠNƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTË
CBƒBˆYˆ›Ü›X]Ø›ØÚÊÙ[‹›ØÚË[™Ý
NƒBˆ™]Ý˜[HˆƒBˆ›ÜˆH[ˆ˜[™ÙJ[™Ý
NƒBˆYˆ
›ØÚÖÚWHMŠNƒBˆ™]Ý˜[
ÏH
Œ	^ˆ	H›ØÚÖÚWJCBˆ[Ù:
  ”ÍŒÌÔÕUT×ÐÔ–TÌWÓÓŠCBƒBˆYˆYœ˜ÍŒÌÓQ—ÙX]]
Ù[ŠNƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTË
CBƒBˆYˆ›Ü›X]Ø›ØÚÊÙ[‹›ØÚË[™Ý
NƒBˆ™]Ý˜[HˆƒBˆ›ÜˆH[ˆ˜[™ÙJ[™Ý
NƒBˆYˆ
›ØÚÖÚWHMŠNƒBˆ™]Ý˜[
ÏH
Œ	^ˆ	H›ØÚÖÚWJCBˆ[Ù:
                revTÌWÓÓŠCBƒBˆYˆYœ˜ÍŒÌÓQ—ÙX]]
Ù[ŠNƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTË
CBƒBˆYˆ›Ü›X]Ø›ØÚÊÙ[‹›ØÚË[™Ý
NƒBˆ™]Ý˜[HˆƒBˆ›ÜˆH[ˆ˜[™ÙJ[™Ý
NƒBˆYˆ
›ØÚÖÚWHMŠNƒBˆ™]Ý˜[
ÏH
Œ	^ˆ	H›ØÚÖÚWJCBˆ[Ù:
                ret_val += ("%x " %YˆYœ˜ÍŒÌÓQ—ÙX]]
Ù[ŠNƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTË
CBƒBˆYˆ›Ü›X]Ø›ØÚÊÙ[‹›ØÚË[™Ý
NƒBˆ™]Ý˜[HˆƒBˆ›ÜˆH[ˆ˜[™ÙJ[™Ý
NƒBˆYˆ
›ØÚÖÚWHMŠNƒBˆ™]Ý˜[
ÏH
Œ	^ˆ	H›ØÚÖÚWJCBˆ[Ù:
                ret_val += ("%x " % block[i])
    !X]]
Ù[ŠNƒBˆÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTË
CBƒBˆYˆ›Ü›X]Ø›ØÚÊÙ[‹›ØÚË[™Ý
NƒBˆ™]Ý˜[HˆƒBˆ›ÜˆH[ˆ˜[™ÙJ[™Ý
NƒBˆYˆ
›ØÚÖÚWHMŠNƒBˆ™]Ý˜[
ÏH
Œ	^ˆ	H›ØÚÖÚWJCBˆ[Ù:
                ret_val += ("%x " % block[i])
        return ret_vaHÙ[‹›Yœ˜ÍŒÌÝÜš]WÜ™YÊQ”ÍŒÌÔ‘Q×ÔÕUTË
CBƒBˆYˆ›Ü›X]Ø›ØÚÊÙ[‹›ØÚË[™Ý
NƒBˆ™]Ý˜[HˆƒBˆ›ÜˆH[ˆ˜[™ÙJ[™Ý
NƒBˆYˆ
›ØÚÖÚWHMŠNƒBˆ™]Ý˜[
ÏH
Œ	^ˆ	H›ØÚÖÚWJCBˆ[Ù:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
w&—FU÷&Vr„Ôe$3c3õ$Tuõ5DEU2ÂÐ Ð¢FVbf÷&ÖEö&Æö6²‡6VÆbÂ&Æö6²ÂÆVæwF‚“ Ð¢&WE÷fÂÒ" Ð¢f÷"’–â&ævRƒÂÆVæwF‚“ Ð¢–b†&Æö6µ¶•ÒÂb“ Ð¢&WE÷fÂ³Ò‚#W‚"R&Æö6µ¶•ÒÐ¢VÇ6:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
8¤e_reg(MFRC630_REG_STATUS, 0)

    def format_block(self, block, length):
        ret_val = ""
        for i in range(0, length):
            if (block[i] < 16):
                ret_val += ("0%x " % block[i])
            else:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
8¤e_reg(MFRC630_REG_STATUS, 0)

    def format_block(self, block, length):
        ret_val = ""
        for i in range(0, length):
            if (block[i] < 16):
                ret_val += ("0%x " % block[i])
            else:
                ret_val += ("%x " % block[i])
        return ret_val.upper()
8¤e_reg(MFRC630_RE