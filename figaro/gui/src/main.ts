import { app, BrowserWindow } from 'electron';
import fs from 'fs';
import path from 'path';

import conf from './config/conf.json';

function createWindow (): void {
  const sconf: string = path.resolve(__dirname, '..', '..', 'server', 'conf.json');
  const win: BrowserWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });
  // win.webContents.openDevTools();
  win.removeMenu();
  win.loadURL(`http://${conf.host}:${conf.port}`);
  win.webContents.executeJavaScript(`localStorage.setItem('no-logout', true);`);
  win.webContents.executeJavaScript(`localStorage.setItem('tkn', '${fs.readFileSync(path.resolve(__dirname, '..', '.tkn'))}');`);
}

app.whenReady().then(createWindow);