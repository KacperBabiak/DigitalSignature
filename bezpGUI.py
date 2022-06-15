from email.policy import default
from re import MULTILINE
from tkinter import COMMAND
import PySimpleGUI as sg
import GeneratorClass
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


#sg.Window(title="RSA", layout=[[]], margins=(400, 300)).read()

layout = [[sg.Button(button_text ="Wygeneruj klucz",k='generateKey',enable_events=True)],
            [sg.InputText(default_text='Public key',key='pubKey'),sg.InputText('Private key',key='privKey')],
            [sg.Text("Wpisz wiadomość:")],
            [sg.InputText(enable_events=True,key="messageChanged"),
            sg.Button(button_text ="Rozpocznij",k='start',enable_events=True)],
            [sg.Text("Zakodowana wiadomość:")],
            [sg.Multiline(key='encodedMess',enable_events=True,default_text='')],
            [sg.Text("Wiadomość po odkodowaniu:")],
            [sg.Text(text="",key='decodedMess',enable_events=True)]
            ]

# Create the window
window = sg.Window("Demo", layout)
isKeyGenerated = False
messageChanged = False
#generate keys
gen = GeneratorClass.Generator


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if  event == sg.WIN_CLOSED:
        break
    elif event == 'generateKey':
        gen.startGen()
        
        key = RSA.generate(2048,gen.oneRandomBitLoop)
        private_key = key.export_key("PEM")
        public_key = key.publickey().export_key("PEM")
        window.Element('pubKey').update(public_key)
        window.Element('privKey').update(private_key)
        gen.deleteScreenshots()
        isKeyGenerated=True
    elif event== 'messageChanged':
        messageChanged=True
    elif event=='start':
        
        if(isKeyGenerated and messageChanged):
            #privKey=bytes(values['privKey'][2:(len(values['privKey'])-1)],'utf-8')
            #publKey=bytes(values['pubKey'],'utf-8')
            
            #privKey=RSA.import_key(str(values['privKey']))
            #
            # publKey=RSA.import_key(values['pubKey'])

            message=values["messageChanged"]
            print("generuje wiadomości...")


            key = RSA.import_key(private_key)
            cipher = PKCS1_OAEP.new(key)
            ciphertext = cipher.encrypt(bytes(message,'utf-8'))
            #print(ciphertext)


            #decrypting
            key2 = RSA.import_key(public_key)
            cipher2 = PKCS1_OAEP.new(key2)
            plaintext = cipher.decrypt(ciphertext)
            print (plaintext.decode("utf-8"))
            window.Element('encodedMess').update(ciphertext)
            window.Element('decodedMess').update(plaintext.decode("utf-8"))



window.close()
