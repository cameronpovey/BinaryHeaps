import morse, unittest, asyncio

class TestMorse(unittest.TestCase):
    tree = morse.MorseTree()
    tree.createTree()
    
    def test_bt(self):
        self.assertEqual(self.tree.decode_bt('..- ...'), 'US')#test HEAP
        
    def test_BIG_bt(self):
        self.assertEqual(self.tree.decode_bt('.... . .-.. .-.. --- -.-.-- / ...-..- .-.-. .-- --- .-. .-.. -.. -.--. -.--.- -....- -...-'), 'HELLO! $+WORLD()-=')#test complex characters
        
    def test_HAM_encode(self):
        self.assertEqual(morse.encode_ham("r1","w2","hello world"), '.-- ..--- -.. . .-. .---- -...- .... . .-.. .-.. --- / .-- --- .-. .-.. -.. -...- -.--.')#test HAM encode
        
    def test_HAM_decode(self):
        self.assertEqual(morse.decode_ham('.-- ..--- -.. . .-. .---- -...- .... . .-.. .-.. --- / .-- --- .-. .-.. -.. -...- -.--.'), ("r1","w2","hello world"))#test HAM decode - FAILURE CAPITALS
        
    def test_HAM_decode_fixed(self):
        self.assertEqual(morse.decode_ham('.-- ..--- -.. . .-. .---- -...- .... . .-.. .-.. --- / .-- --- .-. .-.. -.. -...- -.--.'), ("R1","W2","HELLO WORLD"))#test HAM decode - FIXED
    
    def test_HAM_en_dede(self):
        self.assertEqual(morse.encode_ham("dedede","dedede","dedede"), "-.. . -.. . -.. . -.. . -.. . -.. . -.. . -...- -.. . -.. . -.. . -...- -.--.")#test HAM encode - dedededede
        
    def test_HAM_de_dede(self):
        self.assertEqual(morse.decode_ham("-.. . -.. . -.. . -.. . -.. . -.. . -.. . -...- -.. . -.. . -.. . -...- -.--."), ("DEDEDE","DEDEDE","DEDEDE"))#test HAM decode - to many de's
    
    def test_echo(self):
        self.assertEqual(asyncio.run(morse.send_echo("c2", "testing")), ('ECHO', 'C2', 'TESTING'))
        
    def test_time(self):
        self.assertEqual(asyncio.run(morse.send_time("c2")), ('TIME', 'C2', '14:30:00'))

if __name__ == '__main__':
    unittest.main()