import React from 'react';
import '../style/global.scss';
import style from './BaseLayout.module.scss';

import Popup from '../components/Popup';
import FancyInput from '../components/FancyInput';

export default class BaseLayout extends React.Component {
  private loginPopup: Popup;
  private loginUname: FancyInput;
  private loginPassw: FancyInput;

  private onShowLogin (): void {
    this.loginPopup.show();
    this.loginUname.clear();
    this.loginPassw.clear();
  }

  private onLogin (): void {
    console.log(this.loginUname.value, this.loginPassw.value);
  }

  public render() {
    return (
      <>
        <header className={style.header}>
          <h1>Figaro</h1>
          <div className={style.loginBut} onClick={this.onShowLogin.bind(this)}>
            Login
          </div>
          <Popup ref={e => this.loginPopup = e} style={{
          }}>
            <h1 style={{
              paddingBottom: '10px',
              borderBottom: '3px solid #072435',
              marginBottom: '10px',
            }}>Login</h1>
            <FancyInput ref={e => this.loginUname = e} type="text" hint="What's your username?" />
            <FancyInput ref={e => this.loginPassw = e} type="password" hint="What's your password?" />
            <FancyInput type="submit" value="Login" onClick={this.onLogin.bind(this)} />
          </Popup>
        </header>
        { this.props.children }
      </>
    );
  }
}