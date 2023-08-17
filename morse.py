import asyncio, websockets, json, time

class Node():
    def __init__(self,value=''):
        self.value = value
        self.left = None
        self.right = None
        

class MorseTree():
    def __init__(self):
        self.root = Node()
        self.maxLevel = 7
        self.maxValues = sum([2**i for i in range(self.maxLevel+1)])
        
    def __str__(self):
        return str(self.val)
        
    #just to create the initial tree
    def createTree(self):
        morseCode = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '+': '.-.-.', '¿': '..-.-','/': '-..-.', '=': '-...-', '.': '.-.-.-', '(': '-.--.', ')': '-.--.-', ',': '--..--', '?': '..--.', "'": '.----.', ':': '---...', '-': '-....-', '/': '-..-.', '!': '-.-.--', '@': '.--.-.', ';': '-.-.-.', '&': '.-...', '_': '..--.-', '"': '.-..-.', '$': '...-..-', ' ': '/'}
        for x in morseCode: #loops through the dict
            cur = self.root
            for char in morseCode[x]: #loops through each "morse"
                if char == '.':
                    if cur.left == None:
                        cur.left = Node()
                    cur = cur.left
                    
                elif char == '-':
                    if cur.right == None:
                        cur.right = Node()
                    cur = cur.right
            
            #check if node is taken
            if cur.value == "":
                cur.value = x
            else:
                print("Error, atleast 2 characters have the same code")
                exit()
                
    #pre order traversal
    def getMorse(self, node, character, code):
        if node == None:
            return False
        
        elif node.value == character:
            return True
        
        else:
            if self.getMorse(node.left, character, code):
                code.insert(0, ".")
                return True
            elif self.getMorse(node.right, character, code):
                code.insert(0, "-")
                return True

    #encode function
    def encode(self, message):
        encodedMessage = ''
        morse = []
        node = self.root
                
        for char in message.upper():
            if char == " ":
                encodedMessage += "/ "
            else:
                self.getMorse(node, char, morse)
                encodedMessage += "".join(morse) + " "
                morse = []
                
        return encodedMessage.rstrip()
            
    #--Create Heap--
    def getHeap(self):
        heap = []
        queue = [self.root]
        count = 0
        while queue:
            node = queue.pop(0)
            if node == None:
                node = Node()
                
            heap.append(node.value)
            
            queue.append(node.left)
            queue.append(node.right)
            count+=1
            if count == self.maxValues: break
        return(heap)
        
    #HEAPS
    def decode_bt(self, message):
        heap = self.getHeap()  # create the heap
        decodedMessage = ""
        cur = 0
        for char in message:
            if char == '.':
                cur = (cur * 2) + 1
            elif char == '-':
                cur = (cur * 2) + 2
            elif char == ' ':
                if cur < len(heap):
                    decodedMessage += heap[cur]
                    cur = 0
                    
        if cur < len(heap):
            decodedMessage += heap[cur]
            
        return decodedMessage
        
def encode_ham(sender, receiver, message) -> str:
    return(tree.encode(receiver+"de"+sender+"="+message+"=("))

def decode_ham(message) -> (str, str, str):
    msg=""
    decoded = tree.decode_bt(message)
    decoded = decoded.split("DE", 1)
    re = decoded.pop(0)
    decoded = decoded[0].rsplit("=",)
    to = decoded.pop(0)
    msg = decoded[0]
    return(to,re,msg)

tree = MorseTree()
tree.createTree()
print("-== DECODING VIA HEAP ==-")
print(tree.decode_bt(".... . .-.. .-.. --- / .-- --- .-. .-.. -.. -.-.--"))

#Ham in, ham out
print("-== HAM ENCODING ==-")
hamIN = encode_ham("s1","r2","hello world")
print(hamIN)
print("-== HAM DECODING ==-")
print(decode_ham(hamIN))

#W2P2T3
#echo response function
async def send_echo(sender: str, msg: str) -> str:
    encodedMessage = encode_ham(sender, 'echo', msg)
    
    async with websockets.connect(uri) as websocket:
        client = (json.loads(await websocket.recv()))['client_id']
        print("CONNECTED")
        
        outgoing = {'type': 'morse_evt', 'client_id': client, 'payload': encodedMessage}
        await websocket.send(json.dumps(outgoing))
        print("ENCODED MESSAGE SENT")
        
        response = (json.loads(await websocket.recv()))
        decoded = (decode_ham(response['payload']))
        print(decoded)
        
        return decoded

#Time response function
async def send_time(s: str) -> str:
    encodedMessage = encode_ham(s, 'time', "hello world")
    
    async with websockets.connect(uri) as websocket:
        client = (json.loads(await websocket.recv()))['client_id']
        print("CONNECTED")
        
        outgoing = {'type': 'morse_evt', 'client_id': client, 'payload': encodedMessage}
        await websocket.send(json.dumps(outgoing))
        print("ENCODED MESSAGE SENT")
        
        response = (json.loads(await websocket.recv()))
        decoded = (decode_ham(response['payload']))
        print(decoded)
        
        return decoded
    
client = ''
uri = "ws://localhost:10102"
print("-== HAM PACKETS ==-")
print("-== SENDING ECHO ==-")
asyncio.run(send_echo("c2", "testing"))
print("-== SENDING TIME ==-")
asyncio.run(send_time("c2"))
print("--------------------")