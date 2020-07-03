import React from 'react';
import Popup from '../components/Popup';
import FancyInput from '../components/FancyInput';
import withSocket from '../components/withSocket';

interface IndexProps {
  sock: WebSocket;
};

class Index extends React.Component<IndexProps> {
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

  public render () {
    return (
      <>
        <header>
          <h1>Figaro</h1>
          <div className="login-but" onClick={this.onShowLogin.bind(this)}>
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
        <article>
  
        </article>
        <style jsx global>{`
          header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            background-color: #072435;
          }
  
          header h1 {
            font-weight: normal;
            font-family: 'Playfair Display', serif;
            margin: 0;
            transition: .2s ease;
          }
  
          header h1:hover {
            cursor: default;
            text-shadow: 0 0 .5px #EEF1FF;
          }
  
          header div.login-but {
            background-color: #D14081;
            color: #EEF1FF;
            font-family: 'Open Sans', sans-serif;
            font-size: 1.1em;
            padding: 5px 10px;
            border-radius: 5px;
            transition: .2s ease;
          }
  
          header div.login-but:hover {
            cursor: pointer;
            transform: scale(1.1) rotate(2.5deg);
          }
        `}</style>
      </>
    );
  }
}

export default withSocket(Index);