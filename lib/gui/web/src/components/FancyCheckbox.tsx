import React from 'react';
import style from './FancyCheckbox.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckSquare, faSquare } from '@fortawesome/free-solid-svg-icons';

interface FancyCheckboxProps {
  label: string;
  checked?: boolean;
  style?: { [key: string]: any; };
  onClick?: (cb: FancyCheckbox) => void;
};

interface FancyCheckboxState {
  checked: boolean;
};

export default class FancyCheckbox extends React.Component<FancyCheckboxProps, FancyCheckboxState> {
  constructor (props) {
    super(props);
    this.state = {
      checked: Boolean(this.props.checked),
    };
  }

  public toggleChecked (): void {
    this.setState({
      checked: !this.state.checked,
    });
    if (this.props.onClick) this.props.onClick(this);
  }

  public render () {
    return (
      <div className={style.root} style={{
        ...this.props.style,
      }} onClick={this.toggleChecked.bind(this)}>
        <i style={{
          color: this.state.checked ? '#D14081' : '#2E6F97',
        }}><FontAwesomeIcon icon={this.state.checked ? faCheckSquare : faSquare} /></i>
        <span style={{
          color: this.state.checked ? '#D14081' : '#498db8',
        }}>
          {this.props.label}
        </span>
      </div>
    );
  }
}