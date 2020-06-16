<img align="right" src="media/figaro.png" width="125" height="125" />

# Figaro

---

## About

Real-time open-source voice modification program. Can be useful for many things, especially when used in combination with virtual sound i/o devices.

## Table of Contents

* [About](#about)
* [Table of Contents](#table-of-contents)
* [Setup](#setup)
  * [Advanced setup](#advanced-setup)
* [Usage](#usage)
  * [CLI](#cli)
  * [Figaro-Script](#figaro-script)
* [Roadmap](#roadmap)
* [References](#references)

## Setup

First of all, for `Figaro` to be able to work with audio files other than `wav`, you need to download and install `ffmpeg` (see [References](##References) for the link to the official download page).

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

### CLI

All you need to do is to run the following ...

```bash
$ python figaro.py
```

... and whenever you feel lost, just type `help` or `?` and hit enter.

Still, I want you to present with some of the very basic features, to make life a little easier for you and to make this readme more complete. So... here we go!

#### CLI parameters

Before even entering the Figaro CLI, you can already configure your audio setup by using CLI parameters. The following is a table of all available parameters and their purpose:

| Parameter                        | Help                                                                                                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -h, --help                       | Display a list of all parameters and what they're used for.                                                                                             |
| -g, --gui                        | Start with a GUI.                                                                                                                                        |
| -f <filename>, --file <filename> | Interpret the file with name `<filename>` as a Figaro script and run it.                                                                                |
| -i <ist>, --ist <ist>            | Start an input stream (`ist`) using the device with the index `<ist>`. More on devices and their indices [here](#display-all-available-audio-devices).  |
| -o <ost>, --ost <ost>            | Start an output stream (`ost`) using the device with the index `<ost>`. More on devices and their indices [here](#display-all-available-audio-devices). |

#### Basic CLI usage

The two most essential commands when using the Figaro CLI are `help` and `clear`. You might be able to guess their respective meanings already.

* `help` or `?` ... can be used in pretty much any place in the CLI. It will (hopefully) always be able to provide you with some useful info to help you navigate your way through the vast depths of this interface.
* `clear` or `cls` ... simply clears the console - I tend to use this command nearly obsessively. After displaying some info - `clear` - after configuring input and output - `clear` - and so on and so forth.

#### Display all available audio devices

To see which devices are available, use this very simple command ...

```bash
figaro$ show devices
```

#### Configure input/output

Use the `start` command to configure your basic input / output settings. In order to change your microphone, use ...

```bash
figaro$ start input <device-index>
```

... you can use the same syntax for configuring one output device. Keep in mind however that audio will only be forwared to this device then (previously added devices will be stopped, unless added again) ...

```bash
figaro$ start output <device-index>
```

#### Inspect current configuration

To display the audio channel's current setup, use the `show` command ...

```bash
figaro$ show status
```

... this will tell you, which microphone is currently being used and where the audio is being written to (possibly multiple output devices). It will also tell you, whether the channel is active or not.

#### Show live audio feed

To get a CLI preview of the audio feed in real-time, you have to use the `show` command once again ...

```bash
figaro$ show audio
```

... this will present you with a live console preview of the audio that is being processed and forwarded.

<p align="center">
  <img width="975" height="475" src="media/audio.png">
</p>

#### Start/stop the audio channeling

This part is very easy, you can probably guess what the commands will be. To start the channeling process, use ...

```bash
figaro$ start
```

... and to stop reading, processing and writing audio, simply enter ...

```bash
figaro$ stop
```

... very difficult and hard to remember... I know!

#### Using sound effects

You can also use `Figaro` for soundboard-like functionality now. To play any sound file (`wav`, `mp3`, `ogg`, ...) in real-time, simply use ...

```bash
figaro$ start sound <path-to-sound-effect>
```

... by the way, if you want to amplify the sound's volume, just pass the scaling factor after the `<path-to-sound-effect>` parameter like so:

```bash
figaro$ start sound <path-to-sound-effect> <scaling-factor>
```

... if you want to stop a sound effect, what you have to do first is find its `index` ...

```bash
figaro$ show sounds
```

... this command will provide you with everything you need. It shows you a list of the currently playing sound effects and their respective filenames and `indices`. After that, use ...

```bash
figaro$ stop sound <sound-index>
```

... to stop the sound effect.

#### Start/stop interpreting a Figaro Script

To start interpreting a Figaro Script (`<filename>`) from inside the Figaro CLI, use the following command:

```bash
figaro$ start interpreter <filename>
```

... to then stop this script from running, use ...

```bash
figaro$ stop interpreter <intrp-index>
```

... replacing `<intrp-index>` with the index of the interpreter you want to stop. How to get an interpreter's index is explained [here](#show-all-running-interpreters). More on Figaro Script can be found [here](#figaro-script).

#### Show all running interpreters

This is quite simple. In a similar fashion to all other commands for displaying info, use the `show` command, this time in conjunction with the keyword `interpreters`, which will either present you with a list of all currently running interpreters (+ their respective indices) or tell you that none are in fact active at the moment ...

```bash
figaro$ show interpreters
```

#### Using voice-filters [beta]

This part of Figaro will allow you to alter your voice's (or rather the audio input stream's) volume, pitch, etc.

First, to see which filters are available to you, use the proper `show` command:

```bash
figaro$ show filters
```

_More voice-filter capabilities (and their respective documentation) will be added in future updates. As soon as I get a little more spare time to work on this project :p._

### Figaro-Script

You can now also use figaro script (.fig) for defining hotkeys and their behaviour. Whether you want a sound effect to be played, or an attribute to be shown, it can all be bound to a certain keypress.

#### General Syntax

Figaro-Script was heavily inspired by [AutoHotkey](https://www.autohotkey.com/), so, if you are capable of defining hotkeys and their functionality with ahk-script, think of this as a very, very simplified version of that.

But, if you aren't aware of ahk, let me introduce you to the basic syntax very quickly:

Your script, the .fig file, consists of multiple hotkey-definition blocks which tell Figaro which key combinations should result in what behaviour. Apart from that, you can also have comments, to make your script more readable and easier to understand for a future you.

#### Defining a Hotkey

In order to define which keys make up your hotkey, you just need to write all of them in one line and end it with `::`. After this first line, you write all your commands and end the definition block with `return`. This could look something like the following:

```text
...

q::
start sound tmp/asdf.mp3 2
return

...
```

... this hotkey would be triggered every time the `q` is pressed.

Certain control keys need alternative symbols (this is equalivalent to ahk-script):

* `alt` is represented by `!`
* `ctrl` is represented by `^`
* `shift` is represented by `+`

... keep in mind that the definition of hotkeys is usually case insensitive, which means in order to, for example, only trigger the hotkey on an uppercase `Q`, you would need to use `+q::` as your definition.

#### Comments

This is fairly easy to explain. If you have ever used a popular programming language such as C, C++, Java, etc. you already know how to use comments. The only thing to bear in mind is that so far, I have only implemented `single-line` comments.

For people who have never used such a programming language before, this is the correct syntax for comments in Figaro-Script:

```text
...

// triggered by pressing `lower-case q`
// will play the mp3 file "tmp/asdf.mp3" at 200% of the original volume ...
q::
start sound tmp/asdf.mp3 2
return

...
```

#### Builtins

Despite the CLI commands, certain builtin functions are also available to you (at the moment there aren't many, but I will at more should the need to do so arise):

##### Pause

You can use this command in order play a sound effect, or do anything else for that matter, after waiting for a given amount of `milliseconds`. E.g.:

```text
...
start sound tmp/1.mp3
pause 3000
start sound tmp/2.mp3
...
```

... this would play the sound effect `tmp/1.mp3`, wait for `3 seconds` and then play the next sound effect `tmp/2.mp3`.

_More docs coming soon! Disclaimer: Some of the commands described above might still be removed or altered..._

## Roadmap

Just a small preview of what is about to come. It's very likely that this roadmap will continue to grow in the future, as I get more ideas or if somebody wants to contribute.

* [ ] [CLI](#cli)
  * [x] I/O device selection
  * [x] Live status (live audio graph in console)
  * [ ] Filter control
  * [x] Sound effects (soundboard-like abilities)
* [ ] GUI
  * [ ] Functionality
  * [ ] Design
* [ ] Filters
  * [x] Volume
  * [ ] Pitch-Shift
  * [ ] Randomized
* [ ] [Figaro-Script](#figaro-script)
  * [x] Using CLI commands
  * [x] Hotkeys
  * [ ] Advanced builtins

## References

* Windows Virtual Sound I/O ... [vb-audio](https://www.vb-audio.com/Cable/)
* PyAudio Windows Wheel ... [uci](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
* FFmpeg download ... [ffmpeg.org](https://ffmpeg.org/download.html)

---

... MattMoony (June 2020)
