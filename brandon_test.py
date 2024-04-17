import cv2
from VideoGet import VideoGet
from VideoShow import VideoShow
from Inference import Inference
from SoundGen import SoundGen
import serial

octave = 4
key_sig = 0
accidental = False
synth_mode = True
gamma_adjustment = 2.0

# Define labels for synth mode
synth_labels_no_accidental = ["A", "B", "C", "D", "E", "F", "G", "Octave", "Accidental", " "]
synth_labels_accidental = ['Bb', 'C', 'C#', 'Eb', 'F', 'F#', 'Ab', "Octave", "Accidental", " "]
chord_labels = ["1", "2", "3", "4", "5", "6", "7", "KeySig", " ", " "]

# Serial Set up
serial_port_vid = 'COM3'
baud_rate = 9600

global ser
try:
    ser = serial.Serial(serial_port_vid, baud_rate, timeout=0.001)
    print("serial port opened successfully.")
except serial.SerialException as e:
    print(f"Failed to open serial port {e}")
    ser = None
except Exception as e:
    print(f"An error occurred: {e}")
    ser = None

def enhance_clarity(image):
    # Use GaussianBlur to reduce noise
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Normalize the image
    cv2.normalize(image, image, 0, 500, cv2.NORM_MINMAX)

    # Apply color correction (example)
    b, g, r = cv2.split(image)
    # b = cv2.add(b, 30)  # Increase blue
    g = cv2.add(g, 60)  # Decrease green
    image = cv2.merge((b, g, r))

    return image

def threadStart(source=1):
    video_getter = VideoGet(source, gamma_adjustment).start()
    video_shower = VideoShow(video_getter.frame, ser=ser).start()
    inference = Inference(video_getter.frame).start()
    generator = SoundGen(synth_mode, octave, key_sig, accidental, ser=ser).start()

    while True:

        if video_getter.stopped or video_shower.stopped or inference.stopped or generator.stopped:
            video_shower.stop()
            video_getter.stop()
            inference.stop()
            generator.stop()
            break

        frame = video_getter.frame
        frame = enhance_clarity(frame)  # Apply clarity enhancement
        inference.frame = frame
        inference.synth_mode = video_shower.synth_mode
        generator.synth_mode = video_shower.synth_mode
        generator.sustain = video_shower.sustain

        index = inference.index
        generator.prediction = inference.prediction
        generator.index = inference.index

        if video_shower.synth_mode is True:
            if generator.accidental is False:
                cv2.putText(frame, "Inference: " + str(synth_labels_no_accidental[index]), (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
            else:
                cv2.putText(frame, "Inference: " + str(synth_labels_accidental[index]), (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
        else:
            cv2.putText(frame, "Inference: " + str(chord_labels[index]), (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
        cv2.putText(frame, "FPS: " + str(inference.framerate), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
        video_shower.frame = frame
        video_shower.hand_image = inference.hand_image

threadStart(0)
