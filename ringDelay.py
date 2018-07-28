import mido, time

inport = mido.open_input("OSoTASPort", virtual=True)
outport = mido.open_output("TiMidity port 0")

buffer = []

try:
    while True:
        clock = time.time()
        
        for msg in inport.iter_pending():
            buffer.append([msg, clock + 1])

        for msg in buffer:
            print(msg)
            if clock >= msg[1]:
                outport.send(msg[0])
                buffer.remove(msg)

except KeyboardInterrupt:
    inport.close()
    outport.close()
