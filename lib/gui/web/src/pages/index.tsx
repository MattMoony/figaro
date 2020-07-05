import React from 'react';
import style from './index.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faStop, faWaveSquare, faPlus, faDrum } from '@fortawesome/free-solid-svg-icons';
import DragWorkspace from '../components/DragWorkspace';
import DragWindow from '../components/DragWindow';
import * as socket from '../utils/socket';
import AudioWave from '../components/AudioWave';

interface IndexProps {
  sock: WebSocket;
}

interface IndexState {
  loggedIn: boolean;
};

class Index extends React.Component<IndexProps, IndexState> {
  private windows: Set<DragWindow> = new Set();
  private workspace: DragWorkspace;

  private wave: AudioWave;

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
      this.workspace.hideAll();
      this.setState({ loggedIn: false, })
    });
  }

  public render () {
    return (
      <article className={style.article}>
        <DragWorkspace ref={e => this.workspace = e} windows={this.windows}>
          <DragWindow ref={e => this.windows.add(e)} icon={faPlus} title="Filters">
          </DragWindow>
          <DragWindow ref={e => this.windows.add(e)} icon={faDrum} title="Sounds">
          </DragWindow>
          <DragWindow ref={e => this.windows.add(e)} icon={faWaveSquare} title="Audio Wave" style={{
            width: '60%',
            maxWidth: '600px',
          }} onShow={() => this.wave.start()} onHide={() => this.wave.stop()}>
            <AudioWave ref={e => this.wave = e} />
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