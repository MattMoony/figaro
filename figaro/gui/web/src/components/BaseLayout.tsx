import React, { FormEvent } from 'react';
import '../style/global.scss';
import style from './BaseLayout.module.scss';
import Popup from '../components/Popup';
import FancyInput from '../components/FancyInput';
import QrCode from 'react-qr-code';
import forge from 'node-forge';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBiohazard, faQrcode } from '@fortawesome/free-solid-svg-icons';
import { AppProvider, AppConsumer, AppContextProps } from './AppContext';
import TitleBar from './TitleBar';

interface BaseLayoutProps {
  children: React.ReactElement|React.ReactElement[];
};

interface BaseLayoutState {
  loginError?: string;
};

export default class BaseLayout extends React.Component<BaseLayoutProps, BaseLayoutState> {
  private loginPopup: Popup;
  private loginUname: FancyInput;
  private loginPassw: FancyInput;
  private logoutPopup: Popup;
  private qrPopup: Popup;

  public context: AppContextProps;

  constructor (props) {
    super(props);
    this.state = {
    };
  }

  private onShowLogin (): void {
    if (this.context.authenticated) {
      if (localStorage.getItem('no-logout')) return;
      return this.logoutPopup.show();
    }
    this.setState({
      loginError: undefined,
    });
    this.loginUname.clear();
    this.loginPassw.clear();
    this.loginPopup.show();
  }

  private onLogin (e: React.FormEvent): void {
    e.preventDefault();
    const [ uname, pwd ] = [ this.loginUname.value.trim(), this.loginPassw.value ];
    if (!uname || !pwd) return this.setState({ loginError: 'Please enter both username and password!', });
    this.context.login(uname, pwd)
          .then(() => {
            this.loginPopup.hide();
          })
          .catch(e => {
            if (typeof e === 'string') return this.setState({ loginError: e, });
            this.setState({
              loginError: 'Failed to connect to server! Please try again later and/or make sure the Figaro server is running.',
            });
          });
  }

  private onLogout (): void {
    this.context.logout();
    this.logoutPopup.hide();
  }

  public render() {
    return (
      <AppProvider>
        <AppConsumer>
          {ctx => {
            this.context = ctx;
            return (
              <>
                <TitleBar />
                <header className={style.header}>
                  <h1>Figaro</h1>
                  <div className={style.loginBut} onClick={() => this.qrPopup.show()}>
                    { this.context.authenticated
                      ? <i><FontAwesomeIcon icon={faQrcode} /></i>
                      : <i><FontAwesomeIcon icon={faBiohazard} /></i>
                    }
                  </div>
                  <Popup ref={e => this.loginPopup = e}>
                    <h1 style={{
                      paddingBottom: '10px',
                      borderBottom: '3px solid #072435',
                      marginBottom: '10px',
                    }}>Login</h1>
                    <form onSubmit={this.onLogin.bind(this)}>
                      <FancyInput ref={e => this.loginUname = e} type="text" hint="What's your username?" />
                      <FancyInput ref={e => this.loginPassw = e} type="password" hint="What's your password?" />
                      <FancyInput type="submit" value="Login" />
                    </form>
                    <div style={{
                      display: this.state.loginError ? 'block' : 'none',
                      backgroundColor: 'rgba(242, 29, 58, .15)',
                      color: '#F21D3A',
                      padding: '5px',
                      textAlign: 'center',
                      borderRadius: '3px',
                    }}>
                      { this.state.loginError }
                    </div>
                  </Popup>
                  <Popup ref={e => this.qrPopup = e}>
                    <h1 style={{
                      paddingBottom: '10px',
                      borderBottom: '3px solid #072435',
                      marginBottom: '15px',
                    }}>Auth-Key</h1>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center',
                    }}>
                      <div style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        padding: '7px',
                        backgroundColor: '#eef1ff',
                      }}>
                        <QrCode value={forge.util.encode64(this.context.key)} fgColor='#0B3954' bgColor='#eef1ff' />
                      </div>
                    </div>
                    <p>Scan the QR-Code above with your <i>Figaro</i> app to connect this PC to your phone.</p>
                  </Popup>
                  <Popup ref={e => this.logoutPopup = e}>
                    <p style={{
                      marginBottom: '10px',
                      fontSize: '1.2em',
                    }}>
                      Are you sure you want to log out?
                    </p>
                    <FancyInput type="button" value="Yes" onClick={this.onLogout.bind(this)} />
                    <FancyInput type="button" value="No" onClick={() => this.logoutPopup.hide()} />
                  </Popup>
                </header>
                <article className={style.article}>
                  { this.props.children }
                </article>
              </>
            );
          }}
        </AppConsumer>
      </AppProvider>
    );
  }
};