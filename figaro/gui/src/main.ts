import { app, BrowserWindow } from 'electron';
import fs from 'fs';
import path from 'path';
import serve from 'electron-serve';

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
  });

  // process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';
  // win.webContents.openDevTools();
  win.removeMenu();
  // win.loadURL(`http://${conf.host}:${conf.port}`);
  // win.loadURL(`http://localhost:5000/`);
  loadURL(win);
  win.webContents.executeJavaScript(`localStorage.setItem('no-logout', true);`);
  win.webContents.executeJavaScript(`localStorage.setItem('tkn', '${fs.readFileSync(path.resolve(__dirname, '..', '.tkn'))}');`);

  win.once('ready-to-show', () => win.show());
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (win === null) createWindow();
});