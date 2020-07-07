import React from 'react';
import style from './Controls.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faStop } from '@fortawesome/free-solid-svg-icons';
import { AppConsumer, AppContextProps, FigaroDevice, Response } from './AppContext';
import Popup from './Popup';
import FancyCheckbox from './FancyCheckbox';

interface ControlsProps {
};

interface ControlsState {
  input: FigaroDevice[];
  output: FigaroDevice[];
};

interface GetDevicesResponse extends Response {
  input: [number, string][];
  output: [number, string][];
};

export default class Controls extends React.Component<ControlsProps, ControlsState> {
  private inDevPopup: Popup;
  private outDevPopup: Popup;
  
  public context: AppContextProps;

  constructor (props) {
    super(props);
    this.state = {
      input: [],
      output: [],
    };
  }

  private updateDevices (): Promise<void> {
    return new Promise((resolve, reject) => {
      this.context.req<GetDevicesResponse>('sh dev', {}).then(res => {
        if (!res.success) reject(res.msg!);
        this.setState({
          input: res.input.map(d => ({ type: 'input', index: d[0], name: d[1], })),
          output: res.output.map(d => ({ type: 'output', index: d[0], name: d[1], })),
        }, () => resolve());
      }).catch(reject);
    });
  }

  private onSelectInput (): void {
    this.inDevPopup.show();
    this.updateDevices();
  }

  private onSelectOutput (): void {
    this.outDevPopup.show();
    this.updateDevices();
  }

  private onToggleInput (index: number, cb: FancyCheckbox): void {
    this.context.toggleInput(index).catch(() => cb.toggleChecked());
  }

  private onToggleOutput (index: number, cb: FancyCheckbox): void {
    this.context.toggleOutput(index).catch(() => cb.toggleChecked());
  }

  public render () {
    return (
      <AppConsumer>
        {ctx => {
          this.context = ctx;
          return (
            <div className={style.root}>
              <div className={style.devDiv + ' ' + (ctx.status.input.length > 0 ? style.devices : '')}
                   onClick={this.onSelectInput.bind(this)}>
                { ctx.status.input.length > 0
                  ? ctx.status.input.length >= 3
                    ? `${ctx.status.input.length} Devices`
                    : ctx.status.input.map(i => i.name).join(', ')
                  : 'Input'
                }
              </div>
              <Popup ref={e => this.inDevPopup = e} style={{
                maxWidth: '60%',
              }}>
                <div className={style.popup}>
                  <h1>Input Devices</h1>
                  <div>
                    { this.state.input.map(d => <FancyCheckbox key={d.index} label={d.name} checked={this.context.status.input.map(i => i.index).includes(d.index)} onClick={cb => this.onToggleInput(d.index, cb)} />)}
                  </div>
                </div>
              </Popup>
              <i className={ctx.status.running ? style.stop : ''}
                 title={ctx.status.running ? 'Stop' : 'Start'}
                 onClick={() => ctx.status.running ? ctx.stop() : ctx.start()}>
                <FontAwesomeIcon icon={ctx.status.running ? faStop : faPlay} />
              </i>
              <div className={style.devDiv + ' ' + (ctx.status.output.length > 0 ? style.devices : '')}
                   onClick={this.onSelectOutput.bind(this)}>
                { ctx.status.output.length > 0
                  ? ctx.status.output.length >= 3
                    ? `${ctx.status.output.length} Devices`
                    : ctx.status.output.map(i => i.name).join(', ')
                  : 'Output'
                }
              </div>
              <Popup ref={e => this.outDevPopup = e} style={{
                maxWidth: '550px',
              }}>
                <div className={style.popup}>
                  <h1>Output Devices</h1>
                  <div>
                    { this.state.output.map(d => <FancyCheckbox key={d.index} label={d.name} checked={this.context.status.output.map(i => i.index).includes(d.index)} onClick={cb => this.onToggleOutput(d.index, cb)} />)}
                  </div>
                </div>
              </Popup>
            </div>
          );
        }}
      </AppConsumer>
    )
  }
}