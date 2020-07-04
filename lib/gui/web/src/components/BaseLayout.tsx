import React from 'react';
import '../style/global.scss';
import style from './BaseLayout.module.scss';
import Popup from '../components/Popup';
import FancyInput from '../components/FancyInput';
import * as socket from '../utils/socket';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser } from '@fortawesome/free-solid-svg-icons';

interface BaseLayoutProps {
  sock: WebSocket;
};

interface BaseLayoutState {
  loggedIn: boolean;
  loginError?: string;
};

class BaseLayout extends React.Component<BaseLayoutProps, BaseLayoutState> {
  private loginPopup: Popup;
  private loginUname: FancyInput;
  private loginPassw: FancyInput;
  private logoutPopup: Popup;

  constructor (props) {
    super(props);
    this.state = {
      loggedIn: false,
    };
    socket.tryLoadToken();
    socket.isLoggedIn().then(v => this.setState({ loggedIn: v, }));
  }

  private onShowLogin (): void {
    if (this.state.loggedIn) return this.logoutPopup.show();
    this.setState({
      loginError: undefined,
    });
    this.loginUname.clear();
    this.loginPassw.clear();
    this.loginPopup.show();
  }

  private onLogin (): void {
    const [ uname, pwd ] = [ this.loginUname.value.trim(), this.loginPassw.value ];
    if (!uname || !pwd) return this.setState({ loginError: 'Please enter both username and password!', });
    socket.login(uname, pwd)
          .then(() => {
            this.setState({
              loggedIn: true,
            });
            this.loginPopup.hide();
          })
          .catch(msg => {
            this.setState({
              loginError: msg,
            });
          });
  }

  private onLogout (): void {
    socket.logout();
    this.setState({
      loggedIn: false,
    });
    this.logoutPopup.hide();
  }

  public render() {
    return (
      <>
        <header className={style.header}>
          <h1>Figaro</h1>
          <div className={style.loginBut} onClick={this.onShowLogin.bind(this)}>
            { this.state.loggedIn 
              ? <>{ socket.getUname() } <i><FontAwesomeIcon icon={faUser} /></i></> 
              : 'Login' 
            }
          </div>
          <Popup ref={e => this.loginPopup = e}>
            <h1 style={{
              paddingBottom: '10px',
              borderBottom: '3px solid #072435',
              marginBottom: '10px',
            }}>Login</h1>
            <FancyInput ref={e => this.loginUname = e} type="text" hint="What's your username?" />
            <FancyInput ref={e => this.loginPassw = e} type="password" hint="What's your password?" />
            <FancyInput type="submit" value="Login" onClick={this.onLogin.bind(this)} />
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
  }
}

export default BaseLayout;