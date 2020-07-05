const dURL: string = 'ws://localhost:51966';
const id: string = Date.now() + Math.random().toString(36).substr(1,8);
let tkn: string = undefined;

const onLoginCbs: Array<()=>void> = [];
const onLogoutCbs: Array<()=>void> = [];

export function connect (url: string = dURL): Promise<WebSocket> {
  return new Promise((resolve, reject) => {
    const sock: WebSocket = new WebSocket(url);
    waitUntilOpen(sock).then(() => resolve(sock)).catch(reject);
  });
};

export function waitUntilOpen (sock: WebSocket): Promise<void> {
  return new Promise((resolve, reject) => {
    if (sock.readyState !== sock.OPEN) {
      sock.onopen = () => resolve();
      sock.onerror = e => [sock.CLOSING,sock.CLOSED].includes(sock.readyState) && reject(e);
      return;
    }
    resolve();
  });
};

export function tryLoadToken (): void {
  tkn = (typeof window !== 'undefined' && localStorage.getItem('tkn')) || undefined;
  if (tkn) isLoggedIn().then(b => hasLoggedIn()).catch(() => {});
};

interface Response {
  success: boolean;
  msg?: string;
};

export function req<T extends Response> (cmd: string, body: object, sock?: WebSocket): Promise<T> {
  return new Promise((resolve, reject) => {
    const sockP: boolean = Boolean(sock);
    if (!sockP) sock = new WebSocket(dURL);
    waitUntilOpen(sock).then(() => {
      sock.onmessage = (e: MessageEvent) => {
        if (!sockP) sock.close();
        resolve(<T>JSON.parse(e.data));
      };
      sock.send(JSON.stringify({ cmd, id, tkn, ...body, }));
    }).catch(reject);
  });
};

export function onLogin (cb: ()=>void): void {
  onLoginCbs.push(cb);
  tryLoadToken();
};

function hasLoggedIn (): void {
  onLoginCbs.forEach(cb => cb());
}

interface LoginResponse {
  success: boolean;
  msg?: string;
  tkn?: string;
};

export function login (uname: string, pwd: string): Promise<void> {
  return new Promise((resolve, reject) => {
    req<LoginResponse>('auth', { uname: uname, pwd: pwd, }).then(res => {
      if (!res.success) return reject(res.msg!);
      tkn = res.tkn!;
      localStorage.setItem('tkn', tkn);
      hasLoggedIn();
      resolve();
    }).catch(reject);
  });
};

export function onLogout (cb: ()=>void): void {
  onLogoutCbs.push(cb);
};

function hasLoggedOut (): void {
  onLogoutCbs.forEach(cb => cb());
}

export function logout (): void {
  tkn = undefined;
  localStorage.removeItem('tkn');
  hasLoggedOut();
}

interface IsLoggedInResponse {
  success: boolean;
  msg?: string;
  logged_in: boolean;
};

export function isLoggedIn (token: string = tkn): Promise<boolean> {
  return new Promise((resolve, reject) => {
    if (!token) resolve(false);
    req<IsLoggedInResponse>('auth-status', {}).then(res => {
      if (!res.logged_in) {
        tkn = undefined;
        localStorage.removeItem('tkn');
      }
      resolve(res.logged_in);
    }).catch(reject);
  });
};

export function getUname (token: string = tkn): string {
  return JSON.parse(atob(token.split('.')[1])).uname;
};

interface GetConfResponse {
  success: boolean;
  msg?: string;
  BUF?: number;
  SMPRATE?: number;
  CHNNLS?: number;
}

export interface FigaroConf {
  BUF: number;
  SMPRATE: number;
  CHNNLS: number;
}

export function getConf (): Promise<FigaroConf> {
  return new Promise((resolve, reject) => {
    req<GetConfResponse>('get-conf', {}).then(res => {
      if (!res.success) return reject(res.msg!);
      resolve({ BUF: res.BUF!, SMPRATE: res.SMPRATE!, CHNNLS: res.CHNNLS! })
    });
  });
}

export function getAudioUpdates (scale: number, cb: (data: Array<number>)=>boolean): Promise<void> {
  return new Promise((resolve, reject) => {
    const sock = new WebSocket(dURL);
    waitUntilOpen(sock).then(() => {
      sock.onmessage = (e: MessageEvent) => {
        (<Blob>e.data).arrayBuffer().then(b => {
          if (!cb(Array.from(new Float32Array(b)))) {
            sock.close(1000);
          }
        });
      };
      sock.send(JSON.stringify({ cmd: 'get-audio', id, tkn, scale, }));
      resolve();
    }).catch(reject);
  });
}