const dURL: string = 'ws://localhost:51966';
const id: string = Date.now() + Math.random().toString(36).substr(1,8);
let tkn: string = undefined;

const onLoginCbs: Array<()=>void> = [];
const onLogoutCbs: Array<()=>void> = [];

export function connect (url: string = dURL): Promise<WebSocket> {
  return new Promise((resolve, reject) => {
    const sock: WebSocket = new WebSocket(url);
    waitUntilOpen(sock).then(() => resolve(sock));
  });
};

export function waitUntilOpen (sock: WebSocket): Promise<void> {
  return new Promise((resolve, reject) => {
    if (sock.readyState !== sock.OPEN) return sock.onopen = () => resolve();
    resolve();
  });
};

export function tryLoadToken (): void {
  tkn = (typeof window !== 'undefined' && localStorage.getItem('tkn')) || undefined;
  if (tkn) hasLoggedIn();
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
    });
  });
};

export function onLogin (cb: ()=>void): void {
  tryLoadToken();
  if (tkn) return cb();
  onLoginCbs.push(cb);
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
    });
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
    });
  });
};

export function getUname (token: string = tkn): string {
  return JSON.parse(atob(token.split('.')[1])).uname;
};