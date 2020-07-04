import React, { ReactElement } from 'react';
import style from './DragWorkspace.module.scss';
import DragWindow from './DragWindow';

interface DragWorkspaceProps {
  windows: Array<DragWindow>;
}

export default class DragWorkspace extends React.Component<DragWorkspaceProps> {
  public root: HTMLDivElement;

  public componentDidMount (): void {
    this.props.windows.forEach(w => {
      w.setWorkspace(this)
      w.setPos();
    });
  }

  public get size (): DOMRect {
    return this.root.getBoundingClientRect();
  }

  public winAmount (): number {
    return this.props.windows.length;
  }

  public allWindowsBackground (): void {
    this.props.windows.forEach(w => w&&w.intoBackground());
  }

  public allAbsoluteBackground (): void {
    this.props.windows.forEach(w => w&&w.zIndex(0));
  }

  public render () {
    return (
      <div className={style.workspace} ref={e => this.root = e}>
        {this.props.children}
      </div>
    );
  }
};