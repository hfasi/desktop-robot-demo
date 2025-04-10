import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024
AUDIO_PATH = "output.wav"

class AudioRecorder:
    def __init__(self, samplerate=RATE, channels=CHANNELS, dtype='int16'):
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.recording = []
        self.stream = None

    def start_record(self):
        try:
            print("开始录音...")
            self.recording = []
            self.stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=self._callback)
            self.stream.start()
        except Exception as e:
            print(f"录音启动失败: {e}")

    def _callback(self, indata, frames, time, status):
        try:
            self.recording.append(indata.copy())
        except Exception as e:
            print(f"录音回调失败: {e}")

    def stop_record(self):
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
                print("录音结束")
                self.save_recording(AUDIO_PATH)
        except Exception as e:
            print(f"录音停止失败: {e}")

    def save_recording(self, filename):
        try:
            if self.recording:
                recording_array = np.concatenate(self.recording, axis=0)
                wav.write(filename, self.samplerate, recording_array)
                print(f"录音已保存到 {filename}")
        except Exception as e:
            print(f"保存录音失败: {e}")
            
            
            
def main3():
    print("程序开始，请按 'S' 开始录音，'T' 停止录音，或 'Q' 退出程序")
    while True:
        try:
            key = input().strip().upper()
            if key == 'S':
                recorder.start_record()
            elif key == 'T':
                recorder.stop_record()
            elif key == 'Q':
                print("退出程序")
                break
            else:
                print("无效的输入，请按 'S' 开始录音，'T' 停止录音，或 'Q' 退出程序")
        except KeyboardInterrupt:
            print("\n程序被中断")
            break

if __name__ == "__main__":
    recorder = AudioRecorder()
    main3()
   