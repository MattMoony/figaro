import { app, BrowserWindow, ipcMain, IpcMainEvent } from 'electron';
import open from 'open';
import path from 'path';
import serve from 'electron-serve';
import { spawn, ChildProcessWithoutNullStreams } from 'child_process';

const loadURL = serve({ directory: path.resolve(__dirname, process.env.NODE_ENV === 'dev' ? path.join('..', 'web') : path.join('..', '..', '..'), 'public'), });
let win: BrowserWindow;

// import conf from './config/conf.json';

function createWindow (): void {
  // const sconf: string = path.resolve(__dirname, '..', '..', 'server', 'conf.json');
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    show: false,
    frame: false,
    resizable: true,
    backgroundColor: '#0B3954',
    title: 'Figaro',
    icon: path.resolve(__dirname, '..', '..', '..', 'media', process.platform === 'win32' ? 'figaro.ico' : process.platform === 'darwin' ? 'figaro.icns' : 'figaro-256x256.png'),
  });
  let cmd: string;
  let args: string[];
  if (process.env.NODE_ENV === 'dev') {
    cmd = 'python';
    args = [ path.resolve(__dirname, '..', '..', '..', 'figaro.py'), '-s', ];
    if (process.platform !== 'win32') {
      cmd = '/usr/bin/env';
      args.unshift('python3');
    }
  } else {
    cmd = path.resolve(__dirname, '..', '..', '..', 'bin', process.platform === 'win32' ? 'figaro.exe' : 'figaro');
    args = [ '-s', ];
  }
  const figaro: ChildProcessWithoutNullStreams = spawn(cmd, args);
  figaro.stdout.once('data', () => {
    console.log('Got data ... ');

    if (process.env.NODE_ENV === 'dev') {
      process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';
      win.webContents.openDevTools();
    }
    win.removeMenu();
    
    if (process.env.NODE_ENV === 'dev' && !process.env.BUILT_WEB) {
      win.loadURL(`http://localhost:8000/`);
    } else {
      console.log(path.resolve(__dirname, process.env.NODE_ENV === 'dev' ? path.join('..', 'web') : path.join('..', '..', '..'), 'public'));
      loadURL(win);
    }
    win.once('ready-to-show', () => win.show());
  });
  figaro.stdout.on('data', (data) => {
    if (data.toString().includes('Use this QR code')) {
      const key: string = data.toString().split('devices: ')[1].split('\n')[0].trim();
      ipcMain.on('comms', (e: IpcMainEvent, action: string, ...args: string[]) => {
        if (action === 'get-key') e.returnValue = key;
        else if (action === 'open-sounds') open(path.resolve(__dirname, '..', '..', '..', 'res', 'sounds'));
        else e.returnValue = '';
      });
      // console.log(key);
    }
    console.log(data.toString());
  });
  figaro.stderr.on('data', (data) => console.log(data.toString()));
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (win === null) createWindow();
});
