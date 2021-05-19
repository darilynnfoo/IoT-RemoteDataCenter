ڃ�ly��Ɍ���}5}��Ѡ\  $\A���}����)������    %8	D�� ��xn.��El���Ɍ���}5}����Ѡ,  &	 ,    9<	D�А��4� �X � Ԏ ��ІC\�6�X �����Їۗ�*�X����Їۗ���\�]����x��la��ɵ��}�����  $41����Ѡ8�rrpХ�66��d2Ɩ'&'�Ф6��&�v�B�2�#���6��Ɩ֗FVB�РФ&6VB��Ɩ'&'�f�"�w2�e$3c3�d2�2�GG3���v�F�V"�6����v�FW'2��e$3c3 РХF�RԕBƖ6V�6R�ԕB�РФ6��&�v�B�2�#b�f�"v�FW'0РХW&֗76����2�W&V'�w&�FVB�g&VR�b6�&vR�F��W'6���'F���r6��Ц�bF��26�gGv&R�B76�6�FVBF�7V�V�FF���f��W2�F�R%6�gGv&R"��F�FV�Ц��F�R6�gGv&Rv�F��WB&W7G&�7F������6�VF��rv�F��WBƖ֗FF���F�R&�v�G0ЧF�W6R�6�����F�g���W&vR�V&Ɨ6��F�7G&�'WFR�7V&Ɩ6V�6R��B��"6ll
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import time, binascii

class MFRC630:

    NFC_I2CADDR = const(0x28)
    # commands
    MFRC630_CMD_IDLE = const(0x00)  # (no arguments) ; no action, cancels current command execution. */
    MFRC630_CMD_LPCD = const(0x01)  # (no arguments) ; low-power card detection. */
    MFRC630_CMD_LOADKEY = const(0x02)  # (keybyte1), (keybyte2), (keybyte3), (keybyte4), (keybyte5),
    MFRC630_CMD_MFAUTHENT = const(0x03)  # 60h or 61h, (block address), (card serial number byte0), (card
    MFRC630_CMD_RECEIVE = const(0x05)  # (no arguments) ; activ