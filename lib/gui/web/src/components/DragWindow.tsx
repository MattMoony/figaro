import React, { MouseEvent } from 'react';
import style from './DragWindow.module.scss';
import DragWorkspace from './DragWorkspace';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, IconDefinition } from '@fortawesome/free-solid-svg-icons';

interface DragWindowProps {
  title: string;
  icon?: IconDefinition;
  style?: object;
  onShow?: ()=>void;
  onHide?: ()=>void;
};

interface DragWindowState {
  x: number;
  y: number;
  ox: number;
  oy: number;
  moving: boolean;
  visible: boolean;
};

export default class DragWindow extends React.Component<DragWindowProps, DragWindowState> {
  private root: HTMLDivElement;
  private workspace: DragWorkspace;
  
  public zMin: number;

  constructor (props) {
    super(props);
    this.state = {
      x: 0,
      y: 0,
      ox: 0,
      oy: 0,
      moving: false,
      visible: false,
    };
  }

  public componentDidMount () {
    this.zIndex(this.zMin);
  }
  
  public setWorkspace (workspace: DragWorkspace) {
    this.workspace = workspace;
    this.workspace.root.addEventListener('mousemove', this.move.bind(this));
    window.addEventListener('resize', this.workspaceResize.bind(this));
  }

  public zIndex (i: number): void {
    this.root.style.zIndex = i + '';
  }

  public intoBackground (): void {
    this.zIndex(Math.max(this.zMin, +this.root.style.zIndex - 1));
  }

  public intoForeground (): void {
    this.zIndex(this.workspace.winAmount()+this.zMin);
  }

  public setPos (): void;
  public setPos (x: number, y: number): void;

  public setPos (x?: number, y?: number): void {
    const rect: DOMRect = this.root.getBoundingClientRect();
    if (!x) {
      x = Math.random() * (this.workspace.size.width - rect.width);
      y = Math.random() * (this.workspace.size.height - rect.height);
    }
    this.setState({
      x: x < 0 ? 0 : x > this.workspace.size.width - rect.width ? this.workspace.size.width - rect.width : x,
      y: y < 0 ? 0 : y > this.workspace.size.height - rect.height ? this.workspace.size.height - rect.height : y,
    });
  }

  public show();
  public show(x: number, y: number);

  public show (x?: number, y?: number): void {
    this.workspace.allWindowsBackground();
    this.intoForeground();
    this.setState({
      visible: true,
    }, () => {
      this.setPos(x, y);
      if (this.props.onShow) this.props.onShow();
    });
  }

  public hide (): void {
    this.setState({
      visible: false,
    }, () => this.props.onHide ? this.props.onHide() : {});
  }

  private moveStart (e: MouseEvent): void {
    const rect: DOMRect = this.root.getBoundingClientRect();
    this.workspace.allWindowsBackground();
    this.intoForeground();
    this.setState({
      ox: e.clientX - rect.left,
      oy: e.clientY - rect.top,
      moving: true,
    });
  }

  private move (e: MouseEvent): void {
    if (!this.state.moving) return;
    this.setPos(e.clientX - this.workspace.size.left - this.state.ox, e.clientY - this.workspace.size.top - this.state.oy);
  }

  private moveEnd (): void {
    this.setState({
      moving: false,
    })
  }

  private workspaceResize (): void {
    this.setPos(this.state.x, this.state.y);
  }

  public render () {
    return (
      <div ref={e => this.root = e} className={style.root} style={{
        left: this.state.x + 'px',
        top: this.state.y + 'px',
        display: this.state.visible ? 'flex' : 'none',
        ...(this.props.style ? this.props.style : {}),
      }} onContextMenu={e => e.stopPropagation()}>
        <div className={style.head} onMouseDown={this.moveStart.bind(this)} onMouseUp={this.moveEnd.bind(this)}>
          <div>
            {this.props.icon ? <i><FontAwesomeIcon icon={this.props.icon} /></i> : ''}
            {this.props.title}
          </div>
          <i><FontAwesomeIcon icon={faTimes} onClick={() => this.hide()} /></i>
        </div>
        <div className={style.body}>
          {this.props.children}
        </div>
      </div>
    );
  }
};