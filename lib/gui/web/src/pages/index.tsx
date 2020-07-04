import React from 'react';
import style from './index.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faStop, faWaveSquare } from '@fortawesome/free-solid-svg-icons';
import DragWorkspace from '../components/DragWorkspace';
import DragWindow from '../components/DragWindow';
import * as socket from '../utils/socket';

interface IndexProps {
  sock: WebSocket;
}

interface IndexState {
  loggedIn: boolean;
};

class Index extends React.Component<IndexProps, IndexState> {
  private windows: Array<DragWindow> = [];
  private workspace: DragWorkspace;

  constructor (props) {
    super(props);
    this.state = {
      loggedIn: false,
    };
  }

  public componentDidMount (): void {
    socket.onLogin(() => this.setState({ loggedIn: true, }));
    socket.onLogout(() => {
      this.workspace.allAbsoluteBackground();
      this.setState({ loggedIn: false, })
    });
  }

  public render () {
    return (
      <article className={style.article}>
        <DragWorkspace ref={e => this.workspace = e} windows={this.windows}>
          <DragWindow ref={e => this.windows.push(e)} title="First">

          </DragWindow>
          <DragWindow ref={e => this.windows.push(e)} title="Second">

          </DragWindow>
          <DragWindow ref={e => this.windows.push(e)} icon={faWaveSquare} title="Third">

          </DragWindow>
        </DragWorkspace>
        <footer>
          <i><FontAwesomeIcon icon={faPlay} /></i>
        </footer>
        <div className={style.overlay} style={{
          display: this.state.loggedIn ? 'none' : 'flex',
        }}>
          Please login first!
        </div>
      </article>
    );
  }
};

export default Index;