"""Handles the interactive shell for the user"""

import os, pyaudio, wave, shutil, numpy as np, time
import pash.shell, pash.cmds, pash.command as pcmd, colorama as cr
cr.init()
from asciimatics.screen import Screen
from typing import List

from lib import params, utils
from lib.sound import Sound
from lib.device import Device
from lib.channel import Channel
from lib.interpreter import Interpreter

"""The basic prompt for the figaro shell"""
BPROMPT: str = cr.Fore.LIGHTBLUE_EX + 'figaro' + cr.Fore.LIGHTBLACK_EX + '$ ' + cr.Fore.RESET
"""The shell itself"""
sh: pash.shell.Shell = pash.shell.Shell(prompt=BPROMPT)
"""The main PyAudio object"""
pa: pyaudio.PyAudio = pyaudio.PyAudio()
"""The main audio channel"""
ch: Channel = Channel()
"""A list of all running interpreters"""
interpreters: List[Interpreter] = []

def on_exit(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `exit` - quits the shell"""
    if ch.is_alive():
        ch.kill()
    ch.kill_all()
    pa.terminate()
    sh.exit()

def on_show_devices(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `show devices` - lists all audio devices"""
    print('Devices:\n ', end='')
    devs = [pa.get_device_info_by_host_api_device_index(0, i) for i in range(pa.get_host_api_info_by_index(0).get('deviceCount'))]
    print('\r Input:\n   ', end='')
    print('\n   '.join(['{:02d}: {}'.format(i, d['name']) for i, d in enumerate(devs) if d['maxInputChannels'] > 0]))
    print('\r Output:\n   ', end='')
    print('\n   '.join(['{:02d}: {}'.format(i, d['name']) for i, d in enumerate(devs) if d['maxOutputChannels'] > 0]))

def on_show_status(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `show status` - shows the audio channel's status"""
    print(ch)

def on_show_audio(cmd: pcmd.Command, args: List[str], scale: float, char: str) -> None:
    """Callback for `show audio` - shows the detected input"""
    if not ch.is_alive():
        utils.printerr('The audio channel isn\'t running at the moment ... ')
        return
    w, h = shutil.get_terminal_size()
    bw, bh = w//4*3, h
    def disp_audio(screen: Screen) -> None:
        while True:
            screen.clear()
            b = ch.buff
            sw = len(b)//bw
            b = np.asarray([np.average(b[i:i+sw]) for i in range(0, len(b), sw)])
            for i, v in enumerate(b):
                screen.move((w-bw)//2+i, int(h//2-bh*v*scale))
                screen.draw((w-bw)//2+i, h//2, char=char, colour=1 if np.max(b) > .2 else 7)
            e = screen.get_key()
            if e in (ord('Q'), ord('q')):
                break
            screen.refresh()
            time.sleep(.01)
    Screen.wrapper(disp_audio)

def on_show_sounds(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `show sounds` - shows all currently playing sounds"""
    if not ch.sounds:
        utils.printwrn('No sounds are playing at the moment ... ')
        return
    print('Sounds: ')
    for i, s in enumerate(ch.get_sounds()):
        print(' #{:02d} | {}'.format(i, str(s)))

def on_show_interpreters(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `show interpreters` - shows all running interpreters"""
    if not interpreters:
        utils.printwrn('No interpreters running ... ')
        return
    print('Interpreters: ')
    for i, p in enumerate(interpreters):
        print(' #{:02d} | {}'.format(i, str(p)))

def on_start_sound(cmd: pcmd.Command, args: List[str], fname: str) -> None:
    """Callback for `start sound` - adds a sound effect"""
    if not os.path.isfile(fname):
        utils.printerr('File "{}" doesn\'t exist ... '.format(fname))
        return
    try:
        ch.add_sound(Sound(fname))
    except Exception as e:
        utils.printerr(str(e))

def on_start_output(cmd: pcmd.Command, args: List[str], indo: int) -> None:
    """Callback for `start output` - adds an output device"""
    try:
        ch.add_ost(Device(pa, format=pyaudio.paFloat32, channels=1, rate=params.SMPRATE, output=True, output_device_index=indo))
    except Exception as e:
        utils.printerr(str(e))

def on_start_input(cmd: pcmd.Command, args: List[str], indi: int) -> None:
    """Callback for `start input` - adds an input device"""
    try:
        ch.add_ist(Device(pa, format=pyaudio.paFloat32, channels=1, rate=params.SMPRATE, input=True, input_device_index=indi))
    except Exception as e:
        utils.printerr(str(e))

def on_start_interpreter(cmd: pcmd.Command, args: List[str], fname: str) -> None:
    """Callback for `start interpreter` - interprets a .fig file"""
    try:
        interpreters.append(Interpreter(fname, ch))
        interpreters[-1].exec()
    except Exception as e:
        utils.printerr(str(e))

def on_stop_sound(cmd: pcmd.Command, args: List[str], ind: str) -> None:
    """Callback for `stop sound` - removes a sound effect"""
    if ind.lower() in ('a', 'all'):
        ch.del_all_sounds()
        return
    try:
        ind = int(ind)
    except ValueError:
        utils.printerr('"{}" is not a valid index!'.format(ind))
        return
    mxind = len(ch.get_sounds())-1
    if ind > mxind:
        utils.printerr('Index {} is out of bounds (max: {})!'.format(ind, mxind))
        return
    ch.del_sound(ind)

def on_stop_output(cmd: pcmd.Command, args: List[str], indo: int) -> None:
    """Callback for `stop output` - removes an output device"""
    if not indo in [d.indo for d in ch.get_osts()]:
        utils.printwrn('Device isn\'t currently being used ... ')
        return
    ch.del_ost(indo)

def on_stop_input(cmd: pcmd.Command, args: List[str], indi: int) -> None:
    """Callback for `stop input` - removes an input device"""
    if not indi in [d.indi for d in ch.get_ists()]:
        utils.printwrn('Device isn\'t currently being used ... ')
        return
    ch.del_ist(indi)

def on_stop_interpreter(cmd: pcmd.Command, args: List[str], ind: str) -> None:
    """Callback for `stop interpreter` - stops a running interpreter"""
    global interpreters
    if ind.lower() in ('a', 'all'):
        for i in interpreters:
            i.kill()
        interpreters = []
        return
    try:
        ind = int(ind)
    except ValueError:
        utils.printerr('"{}" is not a valid index!'.format(ind))
        return
    if ind >= len(interpreters):
        utils.printerr('Index {} is out of bounds (max: {})!'.format(ind, len(interpreters)-1))
        return
    interpreters[ind].kill()
    del interpreters[ind]

def on_start(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `start` - starts the channel"""
    global ch
    if ch.is_alive():
        utils.printwrn('Already running ... ')
        return
    ch = Channel(ch.transf, ch.ist, ch.ost)
    try:
        ch.start()
    except IOError as e:
        utils.printerr(e)

def on_stop(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `stop` - stops the channel"""
    if not ch.is_alive():
        utils.printwrn('Not running ... ')
        return
    ch.kill()

def start() -> None:
    """Start prompting the user for input."""
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.add_cmd(pcmd.Command('clear', 'cls', callback=pash.cmds.clear, hint='Clear the console ... '))
    # ---------------------------------------------------------------------------------------------------------------------- # 
    sh.add_cmd(pcmd.Command('exit', 'quit', 'exit()', callback=on_exit, hint='Quit the shell ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    show_audio = pcmd.Command('audio', callback=on_show_audio, hint='Show what audio input is detected ... ')
    show_audio.add_arg('-s', '--scale', type=float, dest='scale', default=5., help='Specify output scale ... ')
    show_audio.add_arg('-c', '--char', type=str, dest='char', default='▬', help='Specify the character to be used for the graph ... ')
    sh.add_cmd(pcmd.CascCommand('show', 'sh', cmds=[
        pcmd.Command('devices', 'dev', callback=on_show_devices, hint='List all devices ... '),
        pcmd.Command('status', 'stat', callback=on_show_status, hint='Show the audio channel\'s status ... '),
        show_audio,
        pcmd.Command('sounds', callback=on_show_sounds, hint='List all currently playing sounds ... '),
        pcmd.Command('interpreters', 'in', callback=on_show_interpreters, hint='List all running interpreters ... ')
    ], hint='Show info ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    start_sound = pcmd.Command('sound', callback=on_start_sound, hint='Play a soundeffect ... ')
    start_sound.add_arg('fname', type=str, help='Specify the sound effect\'s filename ... ')
    start_output = pcmd.Command('output', 'ost', callback=on_start_output, hint='Add an output device ... ')
    start_output.add_arg('indo', type=int, help='Specify the output device\'s index ... ')
    start_input = pcmd.Command('input', 'ist', callback=on_start_input, hint='Add an input device ... ')
    start_input.add_arg('indi', type=int, help='Specify the input device\'s index ... ')
    start_interpreter = pcmd.Command('interpreter', 'in', callback=on_start_interpreter, hint='Interpret a .fig file ... ')
    start_interpreter.add_arg('fname', type=str, help='Specify the filename ... ')
    sh.add_cmd(pcmd.CascCommand('start', cmds=[
        start_sound,
        start_output,
        start_input,
        start_interpreter,
    ], callback=on_start, hint='Start channeling audio / other things ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    stop_sound = pcmd.Command('sound', callback=on_stop_sound, hint='Remove a soundeffect ... ')
    stop_sound.add_arg('ind', type=str, help='Specify the sound effect\'s index ... ')
    stop_output = pcmd.Command('output', 'ost', callback=on_stop_output, hint='Remove an output device ... ')
    stop_output.add_arg('indo', type=int, help='Specify the output device\'s index ... ')
    stop_input = pcmd.Command('input', 'ist', callback=on_stop_input, hint='Remove an input device ... ')
    stop_input.add_arg('indi', type=int, help='Specify the input device\'s index ... ')
    stop_interpreter = pcmd.Command('interpreter', 'in', callback=on_stop_interpreter, hint='Stop a running interpreter ... ')
    stop_interpreter.add_arg('ind', type=str, help='Specify the interpreter\'s index ... ')
    sh.add_cmd(pcmd.CascCommand('stop', 'kill', cmds=[
        stop_sound,
        stop_output,
        stop_input,
        stop_interpreter,
    ], callback=on_stop, hint='Stop channeling audio / other things ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.prompt_until_exit()