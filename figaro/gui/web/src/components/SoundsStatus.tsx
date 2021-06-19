import React from 'react';
import style from './SoundsStatus.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMusic, faTimes, faTrash } from '@fortawesome/free-solid-svg-icons';
import { AppConsumer, AppContextProps, AppProvider, Response } from './AppContext';

interface FigaroSound {
  name: string;
  cuplay: number;
  maxplay: number;
}

interface SoundsStatusProps {
}

interface SoundsStatusState {
  sounds: FigaroSound[];
}

export default class SoundsStatus extends React.Component<SoundsStatusProps, SoundsStatusState> {
  public context: AppContextProps;

  constructor (props) {
    super(props);
    this.state = {
      sounds: [],
    };
  }

  componentDidMount (): void {
    this.getSoundsUpdates();
  }

  private getSoundsUpdates (): void {
    const sock: WebSocket = new WebSocket(AppProvider.dURL);
    sock.onmessage = (e: MessageEvent) => {
      // console.log(e.data);
      const sounds: object = JSON.parse(e.data);
      if (!(sounds instanceof Array)) return;
      this.setState({
        sounds: (sounds as FigaroSound[]),
      });
    };
    this.context.send(sock, 'get-sounds', {});
  }

  private onStop (id?: number): void {
    this.context.req<Response>(`stop sound ${id !== undefined ? id : 'a'}`, {});
  }

  public render () {
    return (
      <AppConsumer>
        {ctx => {
          this.context = ctx;
          return (
            <div className={style.root}>
              <div className={style.sounds}>
                { this.state.sounds.map((s: FigaroSound, i: number) => (
                  <div className={style.sound} key={i}>
                    <div>
                      <i><FontAwesomeIcon icon={faMusic}/></i><span>{s.name}</span>
                    </div>
                    <i onClick={() => this.onStop(i)}><FontAwesomeIcon icon={faTimes}/></i>
                    <div style={{
                      width: Math.min(100, (s.cuplay/s.maxplay)*100) + '%',
                    }}></div>
                  </div>
                )) }
              </div>
              { this.state.sounds.length 
                ? <div onClick={() => this.onStop()} className={style.stop}>
                    <i><FontAwesomeIcon icon={faTrash}/></i>
                    Stop all
                  </div> 
                : '' 
              }
            </div>
          );
        }}
      </AppConsumer>
    )
  }
}