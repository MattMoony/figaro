import React from 'react';
import style from './Soundboard.module.scss';
import { AppConsumer, AppContextProps, Response } from './AppContext';
import FancyInput from './FancyInput';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFolder } from '@fortawesome/free-solid-svg-icons';

interface SoundboardProps {
}

interface SoundboardState {
  sounds: string[];
  filtered: string[];
}

export default class Soundboard extends React.Component<SoundboardProps, SoundboardState> {
  public context: AppContextProps;
  private electron: any;

  constructor (props) {
    super(props);
    this.state = {
      sounds: [],
      filtered: [],
    };
  }

  public componentDidMount (): void {
    this.context.onLogin(() => this.refresh());
    this.electron = window.require('electron');
  }

  public refresh (): void {
    interface SoundsResponse extends Response {
      sounds: string[];
    }
    this.context.req<SoundsResponse>('sh sounds a', {})
    .then(res => {
      if (!res.success) return;
      this.setState({
        sounds: res.sounds,
        filtered: res.sounds,
      });
    });
  }

  private onPlaySound (sound: string): void {
    this.context.req<Response>(`start sound "${sound}"`, {});
  }

  private onSearch (e: React.KeyboardEvent): void {
    if (e.key === 'Enter' && this.state.filtered.length) {
      this.onPlaySound (this.state.filtered[0]);
      return;
    }
    this.setState({ 
      filtered: this.state.sounds.filter(s => s.match(new RegExp(`^.*${(e.target as HTMLInputElement).value}.*$`, 'gi'))),
    });
  }

  public render () {
    return (
      <AppConsumer>
        {ctx => {
          this.context = ctx;
          return (
            <div className={style.root}>
              <div className={style.top}>
                <FancyInput type="text" onKeyUp={this.onSearch.bind(this)} />
                <i onClick={() => this.electron.ipcRenderer.send('comms', 'open-sounds')} title="Open sounds folder"><FontAwesomeIcon icon={faFolder} /></i>
              </div>
              <div className={style.sounds}>
              { 
                this.state.filtered.length > 0
                ? this.state.filtered.map(s => <button className={style.sound} key={s} title={s} onClick={() => this.onPlaySound(s)}>{s[0].toUpperCase()}</button>)
                : (<span className={style.noMatch}>No sounds found!</span>)
              }
              </div>
            </div>
          );
        }}
      </AppConsumer>
    );
  }
};