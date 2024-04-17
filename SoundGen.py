import time
import serial
from Note import Note
from threading import Thread

key_signature_array = \
    [
        ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5'],
        ['C#4', 'Eb4', 'F4', 'F#4', 'Ab4', 'Bb4', 'B4', 'C#5', 'Eb5', 'F5', 'F#5'],
        ['D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G5'],
        ['Eb4', 'F4', 'G4', 'Ab4', 'Bb4', 'C5', 'D5', 'Eb5', 'F5', 'G5', 'Ab5'],
        ['E4', 'F#4', 'Ab4', 'A4', 'B4', 'C#5', 'Eb5', 'E5', 'F#5', 'Ab5', 'A5'],
        ['F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'Bb5'],
        ['F#4', 'Ab4', 'Bb4', 'B4', 'C#5', 'Eb5', 'F5', 'F#5', 'Ab5', 'Bb5', 'B5'],
        ['G3', 'A3', 'B3', 'C#4', 'D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5'],
        ['Ab3', 'Bb3', 'C4', 'C#4', 'Eb4', 'F4', 'G4', 'Ab4', 'Bb4', 'C4', 'C#4'],
        ['A3', 'B3', 'C#4', 'D4', 'E4', 'F#4', 'Ab4', 'A4', 'B4', 'C#5', 'D5'],
        ['Bb3', 'C4', 'D4', 'Eb4', 'F4', 'G4', 'A4', 'Bb4', 'C4', 'D4', 'Eb4'],
        ['B3', 'C#4', 'Eb4', 'E4', 'F#4', 'Ab4', 'Bb4', 'B4', 'C#5', 'Eb5', 'E5'],
    ]

key_signature_names_array = ['CMajor', 'C#Major', 'DMajor', 'EbMajor', 'EMajor', 'FMajor', 'F#Major', 'GMajor', 'AbMajor', 'AMajor', 'BbMajor', 'BMajor']

note_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
note_array_accidental = ['Bb', 'C', 'C#', 'Eb', 'F', 'F#', 'Ab']

volume_array = [1.5, 1.5, 1, 0.6, 0.3, 0.4]


class SoundGen:

    def __init__(self, synth_mode=True, octave=4, key_sig=0, accidental=False, ser=None):
        self.synth_mode = synth_mode
        self.stopped = False
        self.sustain = False
        self.prediction = None
        self.index = 9
        self.note_index = 0
        self.octave = octave
        self.key_sig = key_sig
        self.accidental = accidental
        self.C1 = Note()
        self.C2 = Note()
        self.C3 = Note()
        self.note_arr = [self.C1, self.C2, self.C3]
        self.ser = ser

    def start(self):
        Thread(target=self.play_sound, args=()).start()
        return self

    def play_sound(self):
        current_index = None

        while not self.stopped:
            idx = self.index
            pred = self.prediction
            octa = self.octave
            acci = self.accidental

            if self.synth_mode is True:
                # Playing any single notes
                if 0 <= idx < 7 and pred[idx] > 0.8 and self.note_arr[self.note_index].stopped is True:
                    time.sleep(0.1)

                    if self.index != idx:
                        continue

                    current_index = idx

                    self.note_arr[self.note_index].stop()

                    if acci is True:
                        note_to_play = note_array_accidental[idx] + str(octa)
                    else:
                        note_to_play = note_array[idx] + str(octa)

                    self.note_arr[self.note_index].start(note_to_play, volume_array[octa - 2])

                    serial_message = note_to_play[0:0] + "\n"
                    print(serial_message)

                    try:
                        self.ser.write(serial_message.encode())
                    except:
                        print("Serial send failed")

                # Updating the octave
                elif idx == 7 and pred[7] > 0.80:
                    time.sleep(0.2)
                    if self.index == 7:
                        self.note_arr[0].stop()
                        self.note_arr[1].stop()
                        self.note_arr[2].stop()

                        if self.octave >= 7:
                            self.octave = 2
                        else:
                            self.octave += 1

                        # serial_message = "OCTAVE:" + str(self.octave) + "\n"
                        # print(serial_message)

                        # try:
                            # self.ser.write(serial_message.encode())
                        # except:
                            # print("Serial send failed")

                        time.sleep(0.8)

                # Updating the accidental
                elif idx == 8 and pred[8] > 0.80:
                    time.sleep(0.2)
                    if self.index == 8:
                        self.note_arr[0].stop()
                        self.note_arr[1].stop()
                        self.note_arr[2].stop()

                        if self.accidental is True:
                            self.accidental = False
                        else:
                            self.accidental = True

                        # serial_message = "ACCIDENTAL:" + str(self.accidental) + "\n"
                        # print(serial_message)
                        # try:
                            # self.ser.write(serial_message.encode())
                        # except:
                            # print("Serial send failed")

                        time.sleep(0.8)
                # Don't play note if it's already being played
                elif current_index == idx or self.note_arr[0].stopped is True:
                    time.sleep(0.2)
                    continue
                # Stop sound if no hands are on screen anymore
                else:
                    self.note_arr[0].stop()
                    self.note_arr[1].stop()
                    self.note_arr[2].stop()

            # Chord Mode
            else:
                # Playing any of the chords
                if 0 <= idx < 7 and pred[idx] > 0.9 and self.note_arr[0].stopped is True:

                    time.sleep(0.1)
                    if self.index != idx:
                        continue

                    current_index = idx

                    self.note_arr[0].stop()
                    self.note_arr[1].stop()
                    self.note_arr[2].stop()

                    self.note_arr[0].start(key_signature_array[self.key_sig][idx], 0.5)
                    self.note_arr[1].start(key_signature_array[self.key_sig][idx + 2], 0.25)
                    self.note_arr[2].start(key_signature_array[self.key_sig][idx + 4], 0.5)

                    serial_message = str(idx + 1) + "\n"
                    print(serial_message)

                    try:
                        self.ser.write(serial_message.encode())
                    except:
                        print("Serial send failed")

                # Updating the key signature
                elif idx == 7 and pred[7] > 0.9:
                    time.sleep(0.2)
                    if self.index != idx:
                        continue

                    self.note_arr[0].stop()
                    self.note_arr[1].stop()
                    self.note_arr[2].stop()

                    if self.key_sig == 11:
                        self.key_sig = 0
                    else:
                        self.key_sig += 1

                    # serial_message = "KEY:" + key_signature_names_array[self.key_sig] + "\n"
                    # print(serial_message)

                    # try:
                        # self.ser.write(serial_message.encode())
                    # except:
                        # print("Serial send failed")

                    time.sleep(1)
                # Don't play chord again if it's currently being played
                elif current_index == idx or self.note_arr[0].stopped is True:
                    time.sleep(0.2)
                    continue
                # Stop sound if hand is no longer on screen
                else:
                    self.note_arr[0].stop()
                    self.note_arr[1].stop()
                    self.note_arr[2].stop()

    def stop(self):
        self.stopped = True
