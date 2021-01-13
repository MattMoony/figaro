import React from 'react';
import style from './FancyInput.module.scss';

interface FancyInputProps {
  type: string;
  hint?: string;
  value?: string;
  onClick?: React.MouseEventHandler;
  onKeyUp?: React.KeyboardEventHandler;
};

interface FancyInputState {
};

export default class FancyInput extends React.Component<FancyInputProps, FancyInputState> {
  private element: HTMLInputElement;

  public get value () {
    return this.element.value;
  }

  public clear (): void {
    this.element.value = '';
  }
  
  public render () {
    return <input className={style.root} ref={e => this.element = e} type={this.props.type} placeholder={this.props.hint} value={this.props.value} onClick={this.props.onClick} onKeyUp={this.props.onKeyUp} />;
  }
};