import { app, BrowserWindow } from 'electron';

function createWindow (): void {
  const win: BrowserWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });
  win.webContents.openDevTools();
  win.removeMenu();
  win.loadURL('http://localhost:9000');
}

app.whenReady().then(createWindow);