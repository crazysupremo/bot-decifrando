// electron-main.js — faz o Bot Decifrando ser um app de desktop de VERDADE
// (janela própria, ícone na barra de tarefas), em vez de abrir uma aba no
// navegador. Mesmo esquema do NEXT GAME Desktop: Electron por fora, cuidando
// só da janela; o backend (o Flask empacotado em BotDecifrando.exe pelo
// PyInstaller) continua fazendo todo o trabalho de verdade por dentro,
// escondido — a pessoa nunca vê um terminal nem um navegador.

const { app, BrowserWindow, Menu } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const net = require('net');

const PORT = 5000;
let backendProcess = null;
let mainWindow = null;

function getBackendPath() {
  // Empacotado (instalado de verdade): o .exe do backend vai junto como
  // "recurso extra" (ver package.json → build.extraResources).
  if (app.isPackaged) {
    return path.join(process.resourcesPath, 'backend', 'BotDecifrando.exe');
  }
  // Rodando direto com "electron ." (desenvolvimento): usa o .exe que já
  // tiver sido buildado manualmente na pasta backend/ ao lado.
  return path.join(__dirname, 'backend', 'BotDecifrando.exe');
}

function startBackend() {
  backendProcess = spawn(getBackendPath(), [], {
    env: { ...process.env, PORT: String(PORT), ELECTRON_BACKEND: '1' },
    windowsHide: true,
  });
  backendProcess.on('error', (err) => {
    console.error('Erro ao iniciar o backend:', err);
  });
}

// O backend demora um pouquinho pra subir (Python empacotado é mais lento
// pra iniciar que um app nativo) — em vez de um tempo fixo "no chute", fica
// tentando conectar na porta até conseguir, e só então mostra a janela.
function waitForBackend(callback, tentativas = 40) {
  const socket = new net.Socket();
  socket.setTimeout(300);
  socket.once('connect', () => {
    socket.destroy();
    callback();
  });
  socket.once('error', () => {
    socket.destroy();
    if (tentativas <= 0) return callback(); // desiste de esperar, tenta abrir mesmo assim
    setTimeout(() => waitForBackend(callback, tentativas - 1), 300);
  });
  socket.once('timeout', () => {
    socket.destroy();
    if (tentativas <= 0) return callback();
    setTimeout(() => waitForBackend(callback, tentativas - 1), 300);
  });
  socket.connect(PORT, '127.0.0.1');
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 440,
    height: 760,
    minWidth: 360,
    minHeight: 500,
    title: 'Bot Decifrando',
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  Menu.setApplicationMenu(null);
  mainWindow.loadURL(`http://127.0.0.1:${PORT}/`);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startBackend();
  waitForBackend(createWindow);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill();
    backendProcess = null;
  }
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
    backendProcess = null;
  }
});
