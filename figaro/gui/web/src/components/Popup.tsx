import React from 'react';
import style from './Popup.module.scss';

interface PopupProps {
  style?: { [key: string]: any; };
};

interface PopupState {
  visible: boolean;
};

export default class Popup extends React.Component<PopupProps, PopupState> {
  constructor(props) {
    super(props);
    this.state = {
      visible: false,
    };
  }

  public show (): void {
    this.setVisible(true);
  }

  public hide (): void {
    this.setVisible(false);
  }

  private setVisible (b: boolean): void {
    this.setState({
      visible: b,
    });
  }

  private outerClick (): void {
    this.setVisible(false);
  }

  private innerClick (e: React.MouseEvent<HTMLDivElement, MouseEvent>): void {
    e.stopPropagation();
  }

  public render () {
    return (
      <div className={style.root} onClick={this.outerClick.bind(this)} style={{
        display: this.state.visible ? 'flex' : 'none',
        zIndex: 254,
      }}>
        <div onClick={this.innerClick.bind(this)} style={this.props.style}>
          {this.props.children}
        </div>
      </div>
    );
  }
};