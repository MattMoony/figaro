import React from 'react';

export interface AppContextProps {
  authenticated: boolean;
  tkn?: string;
  error?: Error;
  login: (uname: string, pwd: string) => Promise<void>;
  logout: () => void;
  waitUntilOpen: (sock: WebSocket) => Promise<void>;
  uname?: () => string;
  conf: () => Promise<FigaroConf>;
};

const AppContext: React.Context<AppContextProps> = React.createContext<AppContextProps>({
  authenticated: false,
  login: (uname: string, pwd: string) => new Promise((resolve, reject) => resolve()),
  logout: () => {},
  waitUntilOpen: () => new Promise((resolve, reject) => resolve()),
  conf: () => new Promise((resolve, reject) => resolve(null)),
});

export default AppContext;

interface Response {
  success: boolean;
  msg?: string;
};

export interface FigaroConf {
  BUF: number;
  SMPRATE: number;
  CHNNLS: number;
};

interface AppProviderProps {
  children: React.ReactElement|React.ReactElement[];
};

interface AppProviderState extends AppContextProps {
};

export class AppProvider extends React.Component<AppProviderProps, AppProviderState> {
  public static id: string = Date.now() + Math.random().toString(36).substr(1,8);
  public static dURL: string = 'ws://localhost:51966';

  constructor (props) {
    super(props);
    this.state = {
      authenticated: false,
      login: this.login.bind(this),
      logout: this.logout.bind(this),
      waitUntilOpen: this.waitUntilOpen.bind(this),
      conf: this.conf.bind(this),
      uname: this.uname.bind(this),
    };
  }

  public componentDidMount (): void {
    this.setState({
      tkn: localStorage.getItem('tkn'),
    }, () => this.isLoggedIn().then(b => b && this.setState({ authenticated: true, })).catch(e => this.setState({ error: e, })));
  }

  private waitUntilOpen (sock: WebSocket): Promise<void> {
    return new Promise((resolve, reject) => {
      if (sock.readyState !== sock.OPEN) {
        sock.onopen = () => resolve();
        sock.onerror = e => [sock.CLOSING, sock.CLOSED].includes(sock.readyState) && reject(e);
        return;
      }
      resolve();
    });
  }

  private req<T extends Response> (cmd: string, body: object): Promise<T> {
    return new Promise((resolve, reject) => {
      const sock: WebSocket = new WebSocket(AppProvider.dURL);
      this.waitUntilOpen(sock).then(() => {
        sock.onmessage = (e: MessageEvent) => {
          sock.close();
          resolve(JSON.parse(e.data) as T);
        };
        sock.send(JSON.stringify({ cmd, id: AppProvider.id, tkn: this.state.tkn, ...body, }));
      }).catch(reject);
    });
  }

  private isLoggedIn (): Promise<boolean> {
    interface IsLoggedInResponse extends Response {
      logged_in: boolean;
    };
    return new Promise((resolve, reject) => {
      if (!this.state.tkn) return resolve(false);
      this.req<IsLoggedInResponse>('auth-status', {}).then(res => {
        if (!res.logged_in) {
          this.logout();
        }
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

  public render () {
    return (
      <AppContext.Provider value={this.state}>
        {this.props.children}
      </AppContext.Provider>
    );
  }
}

export const AppConsumer: React.Consumer<AppContextProps> = AppContext.Consumer;