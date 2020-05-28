import pyaudio, struct
import numpy as np

from lib.filters.volume import Volume

BUF = 4096

def main():
    pa = pyaudio.PyAudio()
    print('\n'.join(['{:02}: {}'.format(i, pa.get_device_info_by_host_api_device_index(0, i)['name']) for i in range(pa.get_host_api_info_by_index(0).get('deviceCount'))]))
    indi = int(input('Select input device: '))
    indo = int(input('Select output device: '))

    ist = pa.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, input_device_index=indi)
    ost = pa.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True, output_device_index=indo)

    filters = [Volume(2),]

    try:
        while True:
            data = np.array(struct.unpack('f'*BUF, ist.read(BUF)))
            for f in filters:
                data = f(data)
            ost.write(struct.pack('f'*BUF, *data))
    except KeyboardInterrupt:
        pass

    ist.stop_stream()
    ost.stop_stream()
    ist.close()
    ost.close()

    pa.terminate()

if __name__ == '__main__':
    main()