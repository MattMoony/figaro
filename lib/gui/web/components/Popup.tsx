import React from 'react';

interface PopupProps {
  style: { [key: string]: any; };
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
      <div className="root" onClick={this.outerClick.bind(this)}>
        <div onClick={this.innerClick.bind(this)} style={this.props.style}>
          {this.props.children}
        </div>
        <style jsx>{`
          div.root {
            position: fixed;
            display: ${this.state.visible ? 'flex' : 'none'};
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
            background-color: rgba(0, 0, 0, .3);
          }

          div.root > div {
            display: inline-block;
            margin: 25px 0;
            border: 5px solid #072435;
            border-radius: 3px;
            padding: 15px;
            box-sizing: border-box;
            background-color: #0B3954;
          }
        `}</style>
      </div>
    );
  }
};