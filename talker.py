import time
import wave
import queue
import pygame
import socket
import pyaudio
import os.path
import threading

import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext, font

from handy.llm.ollama_llm import Ollama


TMP_FOLDER = Path(__file__).parent / 'tmp'
SOUND_FILE = TMP_FOLDER / 'output_default.wav'
BORDER_SIZE = 6
SOUND_TIMEOUT = 40
MIN_SPOKEN_LENGTH = 20
END_STRING = '87nusey9tfr0w89w74yt5f'

SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
AUDIO_CAPTURE_FILE = './tmp/capture.wav'
MAX_RECORD_LENGTH = 20


def play_audio(text):
    # delete all files in audio folder
    all_files = os.listdir(TMP_FOLDER)
    for i in all_files:
        os.remove(TMP_FOLDER / i)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(SOUND_TIMEOUT)
    try:
        client.connect(('127.0.0.1', 65432))
        full_message = f'{TMP_FOLDER.resolve()}:{text}'
        client.send(full_message.encode('utf-8'))
        client.recv(1024)
    except socket.timeout:
        print('* Did not get audio')
        return
    client.close()
    # play the sound if the file exists
    if os.path.exists(SOUND_FILE):
        print('* Playing audio')
        sound = pygame.mixer.Sound(SOUND_FILE)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)


def merge_short_strings(strings):
    merged = []
    i = 0
    while i < len(strings):
        current_string = strings[i]
        # Keep appending the next string until current_string is long enough
        while len(current_string) < MIN_SPOKEN_LENGTH and i + 1 < len(strings):
            i += 1
            current_string += strings[i]
        merged.append(current_string)
        i += 1
    return merged


def text_thread(text, que):
    # when this is finished, tell the window to accept user input
    # must be run as a separate thread
    sentences = text.split('.')
    sentences = [x.strip() for x in text.split('.')]
    correct_lengths = merge_short_strings(sentences)
    for i in correct_lengths:
        final_text = f'{i.strip()}.'
        que.put(final_text)
        play_audio(final_text)
    que.put(END_STRING)


def convert_audio_to_text():
    pass


class AudioRecorder:
    def __init__(self):
        self.audio = None
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.recording_thread = None

    def start_recording(self):
        self.delete_old_file()
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1, rate=SAMPLE_RATE,
                                      input=True, frames_per_buffer=CHUNK_SIZE)
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def delete_old_file(self):
        if os.path.exists(AUDIO_CAPTURE_FILE):
            os.remove(AUDIO_CAPTURE_FILE)

    def record(self):
        start_time = time.time()
        while self.is_recording:
            data = self.stream.read(CHUNK_SIZE)
            self.frames.append(data)
            if time.time() - start_time >= MAX_RECORD_LENGTH:
                self.is_recording = False
                self.stream.stop_stream()
                self.stream.close()
                self.audio.terminate()

    def stop_recording(self):
        if not self.is_recording:
            return
        self.is_recording = False
        self.recording_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        with wave.open(AUDIO_CAPTURE_FILE, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(b''.join(self.frames))


class AIDisplay:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title('AI Chat')

        # Configure grid rows and columns to resize with the window
        self.root.grid_rowconfigure(0, weight=1)  # Allow the display area to expand more
        self.root.grid_rowconfigure(1, weight=0)  # Input area doesn't need to expand vertically
        self.root.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion

        # Create a scrolled text widget for the display area
        self.display_area = scrolledtext.ScrolledText(self.root)
        self.display_area.grid(row=0, column=0, sticky='nsew', padx=BORDER_SIZE, pady=BORDER_SIZE)
        self.display_area.config(state='disabled')

        # Create a text entry widget for user input
        self.input_area = tk.Text(self.root, height=4)
        self.input_area.grid(row=1, column=0, sticky='nsew', padx=BORDER_SIZE, pady=BORDER_SIZE)
        self.input_area.bind('<Return>', self.on_user_input)

        self.setup_tags()

        # setup llm
        self.llm = Ollama('mistral:7b-instruct-v0.2-q8_0')
        self.llm_history = []
        self.que = queue.Queue()
        self.accept_input = True

        self.recorder = AudioRecorder()
        self.root.bind('<KeyPress-F5>', self.record_keypress)

    def record_keypress(self, event):
        if self.recorder.is_recording:
            self.recorder.stop_recording()
            text = convert_audio_to_text()
        else:
            self.recorder.start_recording()

    def setup_tags(self):
        bold_font = font.Font(self.display_area, self.display_area.cget('font'), weight='bold')
        self.display_area.tag_configure('llm', foreground='blue', font=bold_font)

    def add_text(self, new_text, llm=False):
        self.display_area.config(state='normal')
        current_end = self.display_area.index(tk.END)
        self.display_area.insert(tk.END, new_text + '\n')
        if llm:
            self.display_area.tag_add('llm', current_end, f'{current_end}+{len(new_text)}c')
        self.display_area.config(state='disabled')
        self.display_area.yview(tk.END)

    def on_user_input(self, event):
        if not self.accept_input:
            # do nothing
            return False
        # Get text from input_area, process it, etc.
        input_text = self.input_area.get('1.0', 'end-1c')
        self.add_text(f'[User]: {input_text}')
        response = self.llm.message_with_history(input_text, self.llm_history)
        self.llm_history.append(response)
        talk_thread = threading.Thread(target=text_thread, args=(response.get_text_response(), self.que))
        talk_thread.start()
        # Clear the text in input_area
        self.input_area.delete('1.0', 'end')
        # Prevent the default newline character
        return 'break'

    def check_queue(self):
        try:
            # Retrieve the next item and update the label
            display_text = self.que.get_nowait()
            if display_text == END_STRING:
                self.accept_input = True
            else:
                self.add_text(f'[LLM]: {display_text}.', llm=True)
        except queue.Empty:
            pass
        finally:
            # Check the queue again after 100ms
            self.root.after(100, self.check_queue)

    def run(self):
        self.root.after(100, self.check_queue)
        self.root.mainloop()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    window = AIDisplay()
    window.run()
