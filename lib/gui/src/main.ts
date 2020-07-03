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
}

app.whenReady().then(createWindow);