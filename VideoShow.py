from threading import Thread
import serial
import cv2

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None, synth_mode=True, ser=None):
        self.frame = frame
        self.stopped = False
        self.synth_mode = synth_mode
        self.sustain = False
        self.ser = ser

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            # handle all keyboard input through this thread
            key = cv2.waitKey(1) & 0xFF

            # Toggle between synth and chord mode using 'm' key
            if key == ord("m"):

                if self.synth_mode is True:
                    self.synth_mode = False
                    serial_message = "MODE:Chord\n"
                else:
                    self.synth_mode = True
                    serial_message = "MODE:Synthesizer\n"

                print(serial_message)

                try:
                    self.ser.write(serial_message.encode())
                except:
                    print("Serial send failed")

            # quit program using 'q' key
            elif key == ord("q"):
                try:
                    self.ser.write(b'Quit\n')
                except:
                    print("Serial send failed")

                self.stopped = True

    def stop(self):
        self.stopped = True
