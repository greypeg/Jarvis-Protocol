import speech_recognition as sr     # import the library
 
r = sr.Recognizer()                 # initialize recognizer
mic = sr.Microphone(device_index=2)

while 2 < 3:
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print(r.recognize_google(audio))