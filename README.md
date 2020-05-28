# Figaro

---

## About

Real-time open-source voice modification program. Can be useful for many things, especially when used in combination with virtual sound i/o devices.

## Setup

If you have Python 3.x installed, try installing the requirements:

```bash
$ python -m pip install -r requirements.txt
```

... if you're on Windows and you get an error when installing `PyAudio` try downloading a PIP wheel suitable for your Python version from the link provided in [References](##References).

If everything works out, you're good to go!

### Advanced setup

The following steps will explain how to use this program with the commonly used voice-chat application `Discord` on Windows:

1. Download and install a virtual audio input device (if you don't know any specific one, try the one mentioned in [References](##References)).
2. When selecting an output device at the startup of `Figaro`, choose the virtual input device you just installed (e.g.: `CABLE Input`).
3. In Discord, go to `User Settings > Voice & Video > Input Device` and select the virtual input device from the dropdown (e.g.: `CABLE Output`).
4. There you go, your friends should only be able to hear your filtered voice now.

## Usage

_Coming soon ..._

## Roadmap

Just a small preview of what is about to come. It's very likely that this roadmap will continue to grow in the future, as I get more ideas or if somebody wants to contribute.

- [ ] CLI
  - [x] I/O device selection
  - [ ] Filter control
- [ ] GUI
  - [ ] Functionality
  - [ ] Design
- [ ] Filters
  - [x] Volume
  - [ ] Pitch-Shift
  - [ ] Randomized

## References

Windows Virtual Sound I/O ... [vb-audio](https://www.vb-audio.com/Cable/)

PyAudio Windows Wheel ... [uci](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

---

... MattMoony (May 2020)