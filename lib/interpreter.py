"""An interpreter for .fig files"""

import os, re, time, threading
from pash.shell import Shell
from pynput import keyboard as kb
from typing import List, Dict, Union, Optional, Set, Callable

from lib import utils
from lib.channel import Channel
from lib.sounds.sound import Sound

class Interpreter(object):
    """
    The interpreter for .fig files

    ...

    Attributes
    ----------
    fname : str
        The filename of the file to be interpreted.
    chnnl : Channel
        A Figaro channel.
    sh : Shell
        The shell used for command interpretation.
    keys : List[Set[Union[pynput.keyboard.Key, pynput.keyboard.KeyCode]]]
        List of all mapped hotkeys.
    cmds : List[Tuple[int, List[str]]]
        List of all commands.
    builtins : Map[str, Callable[[int, List[str]], None]]
        Mapping of all builtin functions.
    lstn : pynput.keyboard.Listener
        The keystroke listener.
    cu : Set[Union[kb.Key, kb.KeyCode]]
        The currently pressed keys.
    """
    
    def __init__(self, fname: str, chnnl: Channel, sh: Shell):
        self.fname: str = fname
        self.chnnl: Channel = chnnl
        self.sh: Shell = sh
        if not os.path.isfile(self.fname):
            raise OSError('File "{}" doesn\'t exist!'.format(self.fname))
        self.keys: List[Set[Union[kb.Key, kb.KeyCode]]] = []
        self.cmds: List[Tuple[int, List[str]]] = []
        self.builtins: Map[str, Callbale[[int, List[str]], None]] = {
            'pause': self._cmd_pause,
        }
        self.lstn: kb.Listener = kb.Listener(on_press=self._on_press, on_release=self._on_release)
        self.cu: Set[Union[kb.Key, kb.KeyCode]] = set()

    def exec(self) -> None:
        """Interpret the commands in the file, and start listening for keystrokes"""
        with open(self.fname, 'r', encoding='utf-8') as f:
            lc = 0
            while True:
                l = f.readline()
                if not l:
                    break
                l = l.strip()
                lc += 1
                if l.startswith('//') or not l:
                    continue
                if not l.endswith('::'):
                    raise SyntaxError('{}:{} Syntax Error: Missing "::" after key definitions ... '.format(self.fname, lc))
                l = l[:-2]
                lns = [f.readline(),]
                while not lns[-1].strip() == 'return':
                    cl = f.readline()
                    if not cl:
                        break
                    lns.append(cl)
                if lns[-1].strip() != 'return':
                    raise SyntaxError('{}:{} Syntax Error: Missing "return" statement ... '.format(self.fname, lc))
                m = {
                    ' ': kb.Key.space,
                    '!': kb.Key.alt,
                    '^': kb.Key.ctrl,
                    '+': kb.Key.shift,
                }
                s = set()
                for c in l:
                    if c in m.keys():
                        s.add(m[c])
                        continue
                    if re.match(r'(?:\w|\d)+', c):
                        s.add(kb.KeyCode(char=c.lower()))
                self.keys.append(s)
                self.cmds.append((lc+1, lns))
                lc += len(lns)
        self.lstn.start()

    def kill(self) -> None:
        """Stop the Interpreter"""
        self.lstn.stop()

    def _run(self, lc: int, lines: List[str]) -> None:
        """Run a couple of .fig lines"""
        for i, l in enumerate(lines):
            l = l.strip()
            if not l or l.startswith('//') or l == 'return':
                continue
            if not l.count('"') % 2 == 0:
                raise SyntaxError('{}:{} Syntax Error: Unmatched " ... '.format(self.fname, lc+i))
            args = [a.replace('"', '') for a in re.split(r'\s(?:(?=(?:[^"]*"[^"]*")+[^"]*$)|(?=[^"]*$))', l)]
            if not args[0] in self.builtins.keys():
                self.sh.parse(l)
                continue
            self.builtins[args[0]](lc+i, args[1:])

    def _parse_key(self, key: Union[kb.Key, kb.KeyCode]) -> Union[kb.Key, kb.KeyCode]:
        """Parses a given key/keycode"""
        if key in (kb.Key.shift_l, kb.Key.shift_r):
            key = kb.Key.shift
        elif key in (kb.Key.ctrl_l, kb.Key.ctrl_r):
            key = kb.Key.ctrl
        elif key in (kb.Key.alt_l, kb.Key.alt_r):
            key = kb.Key.alt
        elif isinstance(key, kb.KeyCode) and isinstance(key.char, str) and re.match(r'\w', key.char):
            key = kb.KeyCode(char=key.char.lower())
        elif isinstance(key, kb.KeyCode) and key.vk >= 32 and key.vk <= 126:
            key = kb.KeyCode(char=chr(key.vk).lower())
        return key
        
    def _on_press(self, key: Optional[Union[kb.Key, kb.KeyCode]]) -> None:
        """Callback for the key pressed event"""
        if not key:
            return
        key = self._parse_key(key)
        self.cu.add(key)
        if self.cu in self.keys:
            threading.Thread(target=self._run, args=(*self.cmds[self.keys.index(self.cu)],)).start()

    def _on_release(self, key: Optional[Union[kb.Key, kb.KeyCode]]) -> None:
        """Callback for the key released event"""
        if not key:
            return
        key = self._parse_key(key)
        try:
            self.cu.remove(key)
        except KeyError:
            self.cu.clear()

    def _cmd_pause(self, lc: int, args: List[str]) -> None:
        """Builtin `pause` - waits for the given amount of ms"""
        if not args:
            raise SyntaxError('{}:{} Semantic Error: Missing arguments '.format(self.fname, lc))
        if not re.match(r'\d+', args[0]):
            raise SyntaxError('{}:{} Syntax Error: "{}" is not of type integer ... '.format(self.fname, lc, args[0]))
        time.sleep(int(args[0])/1000)

    def __str__(self) -> str:
        return self.fname