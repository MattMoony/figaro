import React from 'react';
import style from './Controls.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faStop } from '@fortawesome/free-solid-svg-icons';
import { AppConsumer, AppContextProps } from './AppContext';

export default class Controls extends React.Component {
  public context: AppContextProps;

  public render () {
    return (
      <AppConsumer>
        {ctx => {
          this.context = ctx;
          return (
            <div className={style.root}>
              <div className={ctx.status.input.length > 0 ? style.devices : ''}>
                { ctx.status.input.length > 0
                  ? ctx.status.input.length >= 3
                    ? `${ctx.status.input.length} Devices`
                    : ctx.status.input.map(i => i.name).join(', ')
                  : 'Input'
                }
              </div>
              <i className={ctx.status.running ? style.stop : ''}
                 title={ctx.status.running ? 'Stop' : 'Start'}
                 onClick={() => ctx.status.running ? ctx.stop() : ctx.start()}>
                <FontAwesomeIcon icon={ctx.status.running ? faStop : faPlay} />
              </i>
              <div className={ctx.status.output.length > 0 ? style.devices : ''}>
                { ctx.status.output.length > 0
                  ? ctx.status.output.length >= 3
                    ? `${ctx.status.output.length} Devices`
                    : ctx.status.output.map(i => i.name).join(', ')
                  : 'Output'
                }
              </div>
            </div>
          );
        }}
      </AppConsumer>
    )
  }
}