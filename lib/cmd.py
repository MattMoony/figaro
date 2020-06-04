"""Handles the interactive shell for the user"""

import os, pyaudio, wave, shutil, numpy as np, time
import pash.shell, pash.cmds, pash.command as pcmd, colorama as cr
cr.init()
from asciimatics.screen import Screen
from typing import List

from lib import params
from lib.sound import Sound
from lib.device import Device
from lib.channel import Channel

"""The basic prompt for the figaro shell"""
BPROMPT: str = cr.Fore.LIGHTBLUE_EX + 'figaro' + cr.Fore.LIGHTBLACK_EX + '$ ' + cr.Fore.RESET
"""The shell itself"""
sh: pash.shell.Shell = pash.shell.Shell(prompt=BPROMPT)
"""The main PyAudio object"""
pa: pyaudio.PyAudio = pyaudio.PyAudio()
"""The main audio channel"""
ch: Channel = Channel()

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
    print('\n '.join(['{:02}: {}'.format(i, pa.get_device_info_by_host_api_device_index(0, i)['name']) for i in range(pa.get_host_api_info_by_index(0).get('deviceCount'))]))

def on_show_status(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `show status` - shows the audio channel's status"""
    print(ch)

def on_show_audio(cmd: pcmd.Command, args: List[str], scale: float) -> None:
    """Callback for `show audio` - shows the detected input"""
    if not ch.is_alive():
        return
    w, h = shutil.get_terminal_size()
    bw, bh = w//2, h
    def disp_audio(screen: Screen) -> None:
        while True:
            screen.clear()
            b = ch.buff
            sw = len(b)//bw
            b = np.asarray([np.average(b[i:i+sw]) for i in range(0, len(b), sw)])
            for i, v in enumerate(b):
                screen.move((w-bw)//2+i, int(h//2-bh*v*scale))
                screen.draw((w-bw)//2+i, h//2, char='▬', colour=1 if np.max(b) > .2 else 7)
            e = screen.get_key()
            if e in (ord('Q'), ord('q')):
                break
            screen.refresh()
            time.sleep(.01)
    Screen.wrapper(disp_audio)

def on_set_input(cmd: pcmd.Command, args: List[str], indi: int) -> None:
    """Callback for `set input` - sets the input device"""
    ch.set_ist(Device(pa, format=pyaudio.paFloat32, channels=1, rate=params.SMPRATE, input=True, input_device_index=indi))

def on_set_output(cmd: pcmd.Command, args: List[str], indo: int) -> None:
    """Callback for `set output` - sets the output device"""
    global ch
    r = ch.is_alive()
    if r:
        ch.kill()
    try:
        ch = Channel(transf=ch.transf, ist=ch.ist, ost=[Device(pa, format=pyaudio.paFloat32, channels=1, rate=params.SMPRATE, output=True, output_device_index=indo)])
    except Exception as e:
        print(e)
        ch = Channel(transf=ch.transf, ist=ch.ist, ost=ch.ost)
    if r:
        ch.start()

def on_add_sound(cmd: pcmd.Command, args: List[str], fname: str) -> None:
    """Callback for `add sound` - adds a sound effect"""
    if not os.path.isfile(fname):
        return
    try:
        wf = wave.open(fname, 'rb')
        ch.add_sound(Sound(wf, pa.get_format_from_width(wf.getsampwidth()), wf.getsampwidth()))
    except Exception as e:
        print(e)

def on_start(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `start` - starts the channel"""
    global ch
    if not ch.is_alive():
        ch = Channel(ch.transf, ch.ist, ch.ost)
        ch.start()

def on_stop(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `stop` - stops the channel"""
    if ch.is_alive():
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
    sh.add_cmd(pcmd.CascCommand('show', 'sh', cmds=[
        pcmd.Command('devices', 'dev', callback=on_show_devices, hint='List all devices ... '),
        pcmd.Command('status', callback=on_show_status, hint='Show the audio channel\'s status ... '),
        show_audio,
    ], hint='Show info ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    set_input = pcmd.Command('input', 'ist', callback=on_set_input, hint='Set the input device ... ')
    set_input.add_arg('indi', type=int, help='Specify the input device\'s index ... ')
    set_output = pcmd.Command('output', 'ost', callback=on_set_output, hint='Set the output device ... ')
    set_output.add_arg('indo', type=int, help='Specify the output device\'s index ... ')
    sh.add_cmd(pcmd.CascCommand('set', cmds=[
        set_input,
        set_output,
    ], hint='Set attributes ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    add_sound = pcmd.Command('sound', callback=on_add_sound, hint='Play a soundeffect ... ')
    add_sound.add_arg('fname', type=str, help='Specify the sound effect\'s filename ... ')
    sh.add_cmd(pcmd.CascCommand('add', cmds=[
        add_sound,
    ], hint='Add attributes ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.add_cmd(pcmd.Command('start', callback=on_start, hint='Start channeling audio ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.add_cmd(pcmd.Command('stop', 'kill', callback=on_stop, hint='Stop channeling audio ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.prompt_until_exit()