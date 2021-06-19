import { app, BrowserWindow, ipcMain, IpcMainEvent } from 'electron';
import fs from 'fs';
import path from 'path';
import serve from 'electron-serve';
import { spawn, ChildProcessWithoutNullStreams } from 'child_process';

const loadURL = serve({ directory: path.resolve(__dirname, '..', 'web', 'public'), });
let win: BrowserWindow;

import conf from './config/conf.json';

function createWindow (): void {
  const sconf: string = path.resolve(__dirname, '..', '..', 'server', 'conf.json');
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
    show: false,
    frame: false,
    resizable: true,
    backgroundColor: '#0B3954',
  });
  const figaro: ChildProcessWithoutNullStreams = spawn(process.platform === 'win32' ? 'python' : '/usr/bin/env python3', [ path.resolve(__dirname, '..', '..', '..', 'figaro.py'), '-s', ]);
  figaro.stdout.once('data', () => {
    console.log('Got data ... ');

    // process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';
    // win.webContents.openDevTools();
    win.removeMenu();
    
    // win.loadURL('about:blank');
    // win.webContents.executeJavaScript(`localStorage.setItem('no-logout', true);`);
    // win.webContents.executeJavaScript(`localStorage.setItem('tkn', '${fs.readFileSync(path.resolve(__dirname, '..', '.tkn'))}');`);
    // win.webContents.executeJavaScript(`localStorage.setItem('key', '${fs.readFileSync(path.resolve(__dirname, '..', '.key'))}');`);

    ipcMain.on('comms', (e: IpcMainEvent, action: string) => {
      if (action === 'get-key') e.returnValue = fs.readFileSync(path.resolve(__dirname, '..', '.key')).toString();
      else e.returnValue = '';
    });
    
    // loadURL(win);
    // win.loadURL(`http://${conf.host}:${conf.port}`);
    win.loadURL(`http://localhost:8000/`);
    win.once('ready-to-show', () => win.show());
  });
  figaro.stdout.on('data', (data) => console.log(data.toString()));
  figaro.stderr.on('data', (data) => console.log(data.toString()));
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (win === null) createWindow();
});
