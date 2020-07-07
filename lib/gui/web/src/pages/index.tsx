import React from 'react';
import style from './index.module.scss';
import { faWaveSquare, faPlus, faDrum } from '@fortawesome/free-solid-svg-icons';
import DragWorkspace from '../components/DragWorkspace';
import DragWindow from '../components/DragWindow';
import AudioWave from '../components/AudioWave';
import { AppConsumer, AppContextProps } from '../components/AppContext';
import Controls from '../components/Controls';

class Index extends React.Component {
  private windows: Set<DragWindow> = new Set();

  private wave: AudioWave;
  public context: AppContextProps;

  public render () {
    return (
      <AppConsumer>
        {ctx => (
          <article className={style.article}>
            <DragWorkspace windows={this.windows}>
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
              <Controls />
            </footer>
            <div className={style.overlay} style={{
              display: ctx.authenticated ? 'none' : 'flex',
            }}>
              Please login first!
            </div>
          </article>
        )}
      </AppConsumer>
    );
  }
};

export default Index;