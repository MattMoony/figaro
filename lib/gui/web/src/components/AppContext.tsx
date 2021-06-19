import React from 'react';
import forge from 'node-forge';

export interface AppContextProps {
  authenticated: boolean;
  tkn?: string;
  key?: string;
  status: FigaroStatus;
  error?: Error;
  login: (uname: string, pwd: string) => Promise<void>;
  logout: () => void;
  onLogin: (cb: ()=>void)=>void;
  waitUntilOpen: (sock: WebSocket) => Promise<void>;
  send: (sock: WebSocket, cmd: string, body: object, arg0?: string|number, arg1?: number) => Promise<void>;
  req: <T extends Response>(cmd: string, body: object) => Promise<T>;
  uname?: () => string;
  conf: () => Promise<FigaroConf>;
  start: () => Promise<void>;
  stop: () => Promise<void>;
  toggleInput: (index: number) => Promise<void>;
  toggleOutput: (index: number) => Promise<void>;
};

const AppContext: React.Context<AppContextProps> = React.createContext<AppContextProps>({
  authenticated: false,
  key: '',
  status: { input: [], output: [], running: false, },
  login: (uname: string, pwd: string) => new Promise((resolve, reject) => resolve()),
  logout: () => {},
  onLogin: (cb: ()=>void)=>{},
  waitUntilOpen: () => new Promise((resolve, reject) => resolve()),
  send: (sock: WebSocket, cmd: string, body: object, arg0?: string|number, arg1?: number) => new Promise((resolve, reject) => resolve()),
  req: <T extends Response>(cmd: string, body: object) => new Promise((resolve, reject) => resolve(null)),
  conf: () => new Promise((resolve, reject) => resolve(null)),
  start: () => new Promise((resolve, reject) => resolve()),
  stop: () => new Promise((resolve, reject) => resolve()),
  toggleInput: () => new Promise((resolve, reject) => resolve()),
  toggleOutput: () => new Promise((resolve, reject) => resolve()),
});

export default AppContext;

export interface Response {
  rid: string;
  success: boolean;
  msg?: string;
};

export interface FigaroConf {
  BUF: number;
  SMPRATE: number;
  CHNNLS: number;
};

export interface FigaroDevice {
  type: string;
  index: number;
  name: string;
};

export interface FigaroStatus {
  input: FigaroDevice[];
  output: FigaroDevice[];
  running: boolean;
};

interface AppProviderProps {
  children: React.ReactElement|React.ReactElement[];
};

interface AppProviderState extends AppContextProps {
};

export class AppProvider extends React.Component<AppProviderProps, AppProviderState> {
  public static id: string = Date.now() + Math.random().toString(36).substr(1,8);
  public static dURL: string = 'ws://localhost:51966';

  private electron: any;
  private sock: WebSocket;
  private resolvers: { [key: string]: (res: object)=>void } = {};
  private cbs: (()=>void)[] = [];

  constructor (props) {
    super(props);
    this.state = {
      authenticated: false,
      key: '',
      status: { input: [], output: [], running: false, },
      login: this.login.bind(this),
      logout: this.logout.bind(this),
      onLogin: this.onLogin.bind(this),
      waitUntilOpen: this.waitUntilOpen.bind(this),
      send: this.send.bind(this),
      req: this.req.bind(this),
      uname: this.uname.bind(this),
      conf: this.conf.bind(this),
      start: this.start.bind(this),
      stop: this.stop.bind(this),
      toggleInput: this.toggleInput.bind(this),
      toggleOutput: this.toggleOutput.bind(this),
    };
  }

  public componentDidMount (): void {
    this.electron = window.require('electron');
    this.setState({
      key: forge.util.decode64(this.electron.ipcRenderer.sendSync('comms', 'get-key')),
    }, () => {
      this.isLoggedIn().then(b => b && this.setState({ authenticated: true, })).catch(e => this.setState({ error: e, }));
      this.status();
    });
  }

  private waitUntilOpen (sock: WebSocket): Promise<void> {
    return new Promise((resolve, reject) => {
      if (sock.readyState !== sock.OPEN) {
        sock.addEventListener('open', () => resolve());
        sock.addEventListener('error', e => [sock.CLOSING, sock.CLOSED].includes(sock.readyState) && reject(e));
        return;
      }
      resolve();
    });
  }

  private send (sock: WebSocket, cmd: string, body: object);
  private send (sock: WebSocket, cmd: string, body: object, key: string);
  private send (sock: WebSocket, cmd: string, body: object, tmpstmp: number);
  private send (sock: WebSocket, cmd: string, body: object, key: string, tmpstmp: number);

  private send (sock: WebSocket, cmd: string, body: object, arg0?: string|number, arg1?: number): Promise<void> {
    return new Promise((resolve, reject) => {
      this.waitUntilOpen(sock).then(() => {
        const key: string = typeof arg0 === 'string' ? arg0 : this.state.key;
        const nonce: string = forge.random.getBytesSync(12);
        const cipher: forge.cipher.BlockCipher = forge.cipher.createCipher('AES-GCM', key);
        cipher.start({
          iv: nonce,
        });
        const tmstmp: number = typeof arg0 === 'number' ? arg0 : typeof arg1 === 'number' ? arg1 : Date.now();
        cipher.update(forge.util.createBuffer(forge.util.encodeUtf8(JSON.stringify({ cmd, id: AppProvider.id, timestamp: tmstmp, ...body, }))));
        cipher.finish();
        sock.send(forge.util.encode64(nonce + cipher.mode.tag.data + cipher.output.data));
        resolve();
      }).catch(reject);
    });
  }

  private req<T extends Response> (cmd: string, body: object): Promise<T> {
    if (!this.sock) {
      this.sock = new WebSocket(AppProvider.dURL);
      this.sock.onmessage = async (e: MessageEvent) => {
        const msg: string = forge.util.decode64(await e.data.text());
        const nonce: string = msg.substr(0, 12);
        const tag: string = msg.substr(12, 16);
        const enc: string = msg.substr(28);
        const decipher: forge.cipher.BlockCipher = forge.cipher.createDecipher('AES-GCM', this.state.key);
        decipher.start({
          iv: nonce,
          tag,
        });
        decipher.update(forge.util.createBuffer(enc));
        if (decipher.finish()) {
          const body: string = forge.util.decodeUtf8(decipher.output.data);
          const rid: string = JSON.parse(body).rid;
          // console.log(`[*] BODY: ${body}`);
          if (!Object.keys(this.resolvers).includes(rid)) return;
          this.resolvers[rid](JSON.parse(body));
          delete this.resolvers[rid];
        }
      };
    }
    return new Promise((resolve, reject) => {
      const tmstmp: number = Date.now();
      this.resolvers[btoa(cmd + tmstmp)] = (res: object) => resolve(res as T);
      this.send(this.sock, cmd, body, tmstmp).catch(reject);
    });
  }

  private isLoggedIn (): Promise<boolean> {
    interface IsLoggedInResponse extends Response {
      logged_in: boolean;
    };
    return new Promise((resolve, reject) => {
      // if (!this.state.tkn) return resolve(false);
      if (!this.state.key) return resolve(false);
      this.req<IsLoggedInResponse>('auth-status', {}).then(res => {
        if (!res.logged_in) {
          this.logout();
        }
        this.cbs.forEach(cb => cb());
        resolve(res.logged_in);
      }).catch(reject);
    });
  }

  private login (uname: string, pwd: string): Promise<void> {
    interface LoginResponse extends Response {
      tkn?: string;
    };
    return new Promise((resolve, reject) => {
      this.req<LoginResponse>('auth', { uname, pwd, }).then(res => {
        if (!res.success) return reject(res.msg!);
        this.setState({
          authenticated: true,
          tkn: res.tkn!,
        }, () => {
          localStorage.setItem('tkn', this.state.tkn);
          this.cbs.forEach(cb => cb());
          resolve();
        });
      }).catch(reject);
    });
  }

  private logout (): void {
    this.setState({
      tkn: undefined,
      authenticated: false,
    }, () => localStorage.removeItem('tkn'));
  }

  private onLogin (cb: ()=>void): void {
    this.cbs.push(cb);
  }

  private uname (): string {
    if (!this.state.tkn) return undefined;
    return JSON.parse(atob(this.state.tkn.split('.')[1])).uname;
  }

  private conf (): Promise<FigaroConf> {
    interface GetConfResponse extends Response {
      BUF?: number;
      SMPRATE?: number;
      CHNNLS?: number;
    };
    return new Promise((resolve, reject) => {
      this.req<GetConfResponse>('get-conf', {}).then(res => {
        if (!res.success) return reject(res.msg!);
        resolve({ BUF: res.BUF!, SMPRATE: res.SMPRATE!, CHNNLS: res.CHNNLS!, });
      }).catch(reject);
    });
  }

  private status (): Promise<FigaroStatus> {
    interface GetStatusResponse extends Response, FigaroStatus {
    };
    return new Promise((resolve, reject) => {
      this.req<GetStatusResponse>('sh stat', {}).then(res => {
        if (!res.success) return reject(res.msg!);
        const status: FigaroStatus = { input: res.input, output: res.output, running: res.running, };
        this.setState({ status, }, () => resolve(status));
      }).catch(reject);
    });
  }

  private start (): Promise<void> {
    return new Promise((resolve, reject) => {
      this.req<Response>('start', {}).then(res => {
        if (!res.success) return reject(res.msg!);
        this.status().then(() => resolve());
      }).catch(reject);
    })
  }

  private stop (): Promise<void> {
    return new Promise((resolve, reject) => {
      this.req<Response>('stop', {}).then(res => {
        if (!res.success) return reject(res.msg!);
        this.status().then(() => resolve());
      })
    });
  }

  private toggleInput (index: number): Promise<void> {
    return new Promise((resolve, reject) => {
      this.req<Response>(`${this.state.status.input.map(i => i.index).includes(index) ? 'stop' : 'start'} ist ${index}`, {}).then(res => {
        if (!res.success) reject(res.msg!);
        this.status().then(() => resolve());
      }).catch(reject);
    });
  }

  private toggleOutput (index: number): Promise<void> {
    return new Promise((resolve, reject) => {
      this.req<Response>(`${this.state.status.output.map(o => o.index).includes(index) ? 'stop' : 'start'} ost ${index}`, {}).then(res => {
        if (!res.success) reject(res.msg!);
        this.status().then(() => resolve());
      }).catch(reject);
    });
  }

  public render () {
    return (
      <AppContext.Provider value={this.state}>
        {this.props.children}
      </AppContext.Provider>
    );
  }
}

export const AppConsumer: React.Consumer<AppContextProps> = AppContext.Consumer;