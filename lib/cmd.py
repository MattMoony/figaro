"""Handles the interactive shell for the user"""

import pyaudio, pash.shell, pash.cmds, pash.command as pcmd, colorama as cr
cr.init()
from typing import List

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

def on_set_input(cmd: pcmd.Command, args: List[str], indi: int) -> None:
    """Callback for `set input` - sets the input device"""
    ch.set_ist(Device(pa, format=pyaudio.paFloat32, channels=1, rate=44100, input=True, input_device_index=indi))

def on_set_output(cmd: pcmd.Command, args: List[str], indo: int) -> None:
    """Callback for `set output` - sets the output device"""
    global ch
    r = ch.is_alive()
    if r:
        ch.kill()
    try:
        ch = Channel(transf=ch.transf, ist=ch.ist, ost=[Device(pa, format=pyaudio.paFloat32, channels=1, rate=44100, output=True, output_device_index=indo)])
    except Exception as e:
        print(e)
        ch = Channel(transf=ch.transf, ist=ch.ist, ost=ch.ost)
    if r:
        ch.start()

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
    sh.add_cmd(pcmd.CascCommand('show', 'sh', cmds=[
        pcmd.Command('devices', 'dev', callback=on_show_devices, hint='List all devices ... '),
        pcmd.Command('status', callback=on_show_status, hint='Show the audio channel\'s status ... '),
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
    sh.add_cmd(pcmd.Command('start', callback=on_start, hint='Start channeling audio ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.add_cmd(pcmd.Command('stop', 'kill', callback=on_stop, hint='Stop channeling audio ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.prompt_until_exit()