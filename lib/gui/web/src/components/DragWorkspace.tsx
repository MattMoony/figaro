import React from 'react';
import style from './DragWorkspace.module.scss';
import DragWindow from './DragWindow';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck } from '@fortawesome/free-solid-svg-icons';
import { AppConsumer } from './AppContext';

interface DragWorkspaceProps {
  windows: Set<DragWindow>;
  zMin?: number;
}

interface DragWorkspaceState {
  contextMenu: boolean;
  cx: number;
  cy: number;
}

export default class DragWorkspace extends React.Component<DragWorkspaceProps, DragWorkspaceState> {
  public root: HTMLDivElement;
  private contextMenu: HTMLDivElement;

  constructor (props) {
    super(props);
    this.state = {
      contextMenu: false,
      cx: 0,
      cy: 0,
    };
  }

  public componentDidMount (): void {
    this.props.windows.forEach(w => {
      w.setWorkspace(this);
      w.zMin = this.props.zMin || 0;
      // w.setPos();
    });
    window.addEventListener('click', this.hideContextMenu.bind(this));
  }

  public get size (): DOMRect {
    return this.root.getBoundingClientRect();
  }

  public winAmount (): number {
    return this.props.windows.size;
  }

  public allWindowsBackground (): void {
    this.props.windows.forEach(w => w&&w.intoBackground());
  }

  public allAbsoluteBackground (): void {
    this.props.windows.forEach(w => w&&w.zIndex(0));
  }

  public hideAll (): void {
    this.props.windows.forEach(w => w&&w.hide());
  }

  public showContextMenu (e: React.MouseEvent): void {
    e.preventDefault();
    const { clientX, clientY } = e;
    this.setState({
      contextMenu: true,
    }, () => this.setContextPos(clientX - this.size.left, clientY - this.size.top));
  }

  public hideContextMenu (): void {
    this.setState({
      contextMenu: false,
    });
  }

  public setContextPos (x: number, y: number) {
    const rect: DOMRect = this.contextMenu.getBoundingClientRect();
    this.setState({
      cx: x < 0 ? 0 : x > this.size.width - rect.width ? this.size.width - rect.width : x,
      cy: y < 5 ? 5 : y > this.size.height - rect.height ? this.size.height - rect.height - 5 : y,
    });
  }

  public render () {
    return (
      <AppConsumer>
        {ctx => (
          <div className={style.workspace} ref={e => this.root = e} onContextMenu={this.showContextMenu.bind(this)}>
            { ctx.authenticated && (
                <div className={style.background}>
                  Right click anywhere to get started!
                </div>
              )
            }
            <div style={{
              display: ctx.authenticated ? 'block' : 'none',
            }}>
              { this.props.children}
              <div className={style.context} ref={e => this.contextMenu = e} style={{
                display: this.state.contextMenu ? 'block' : 'none',
                left: this.state.cx + 'px',
                top: this.state.cy + 'px',
                zIndex: this.props.zMin+this.winAmount()+1,
              }}>
                { Array.from(this.props.windows).map(w => 
                    w&&w.props.title&&
                    <div key={w.props.title} onClick={(e: React.MouseEvent) => w.state.visible ? w.hide() : w.show(e.clientX-this.size.left, e.clientY-this.size.top)}>
                      <i style={{
                        opacity: w.state.visible ? 1 : 0,
                      }}><FontAwesomeIcon icon={faCheck} /></i>
                      {w.props.title}
                    </div>
                ) }
              </div>
            </div>
          </div>
        )}
      </AppConsumer>
    );
  }
};