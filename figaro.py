"""The main entry point"""

import pyaudio, struct
import numpy as np
from argparse import ArgumentParser

from lib.filters.pitch import Pitch
from lib.filters.volume import Volume

BUF = 4096

def main():
    parser = ArgumentParser()
    parser.add_argument('-l', '--loopback', action='store_true', help='Hear what you\'re saying on your default output device?')
    args = parser.parse_args()

    pa = pyaudio.PyAudio()
    print('\n'.join(['{:02}: {}'.format(i, pa.get_device_info_by_host_api_device_index(0, i)['name']) for i in range(pa.get_host_api_info_by_index(0).get('deviceCount'))]))
    indi = int(input('Select input device: '))
    indo = int(input('Select output device: '))

    ist = pa.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, input_device_index=indi)
    ost = pa.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True, output_device_index=indo)
    if args.loopback:
        dost = pa.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)

    filters = [Pitch(1),Volume(1),]

    try:
        while True:
            data = np.array(struct.unpack('f'*BUF, ist.read(BUF)))
            for f in filters:
                data = f(data)
            if args.loopback:
                dost.write(struct.pack('f'*len(data), *data))
            ost.write(struct.pack('f'*len(data), *data))
    except KeyboardInterrupt:
        pass

    ist.stop_stream()
    ost.stop_stream()
    ist.close()
    ost.close()

    pa.terminate()

if __name__ == '__main__':
    main()