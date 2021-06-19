import React from "react";
import style from './TitleBar.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSquare } from '@fortawesome/free-regular-svg-icons';
import { faMinus, faTimes } from "@fortawesome/free-solid-svg-icons";

export default class TitleBar extends React.Component {
  private electron: any;

  componentDidMount() {
    this.electron = window.require('electron');
  }
  
  private onMaximize (): void {
    if (this.electron.remote.getCurrentWindow().isMaximized()) {
      this.electron.remote.getCurrentWindow().unmaximize();
    } else {
      this.electron.remote.getCurrentWindow().maximize();
    }
  }

  public render() {
    return (
      <nav className={style.titlebar}>
        <i className={style.minimize} onClick={() => this.electron.remote.getCurrentWindow().minimize()}><FontAwesomeIcon icon={faMinus} /></i>
        <i className={style.maximize} onClick={this.onMaximize.bind(this)}><FontAwesomeIcon icon={faSquare} /></i>
        <i className={style.close} onClick={() => this.electron.remote.getCurrentWindow().close()}><FontAwesomeIcon icon={faTimes} /></i>
      </nav>
    );
  }
}