from threading import Thread
import serial
import cv2

# Serial Set up
# on Mac, use "python -m serial.tools.list_ports" to determine what port to use on the line below
try:
    ser = serial.Serial(port='COM1', baudrate=9600)
except:
    ser = None

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None, synth_mode=True):
        self.frame = frame
        self.stopped = False
        self.synth_mode = synth_mode
        self.sustain = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            # handle all keyboard input through this thread
            key = cv2.waitKey(1) & 0xFF
            # Toggle sustain using 's' key
            if key == ord("s"):
                if self.sustain is True:
                    self.sustain = False
                else:
                    self.sustain = True

                serial_message = "Sustain is" + str(self.sustain)
                print(serial_message)

                try:
                    ser.write(serial_message.encode())
                except:
                    print("Serial send failed")
            # Toggle between synth and chord mode using 'm' key
            elif key == ord("m"):

                if self.synth_mode is True:
                    self.synth_mode = False
                else:
                    self.synth_mode = True

                serial_message = "Synth mode is" + str(self.synth_mode)
                print(serial_message)

                try:
                    ser.write(serial_message.encode())
                except:
                    print("Serial send failed")
            # quit program using 'q' key
            elif key == ord("q"):

                try:
                    ser.write(b'Quit')
                except:
                    print("Serial send failed")

                self.stopped = True

    def stop(self):
        self.stopped = True
