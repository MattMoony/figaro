import React from 'react';

interface FancyInputProps {
  type: string;
  hint?: string;
  value?: string;
  onClick?: React.MouseEventHandler;
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
    return (
      <>
        <input ref={e => this.element = e} type={this.props.type} placeholder={this.props.hint} value={this.props.value} onClick={this.props.onClick} />
        <style jsx>{`
          input {
            border: none;
            background-color: #0B4466;
            padding: 10px;
            font-size: 1em;
            font-family: 'Open Sans', sans-serif;
            border-bottom: 2.5px solid #6096B6;
            transition: .15s ease;
            min-width: 150px;
            width: 100%;
            box-sizing: border-box;
            color: #EEF1FF;
            margin: 5px 0;
          }

          input[type="submit"], input[type="button"] {
            background: linear-gradient(to right, #E1448B 0%, #E1448B 50%, #D14081 50%, #D14081 100%);
            background-size: 200% 100%;
            background-position: 100% 0;
            color: #EEF1FF;
            border: none;
            font-size: 1.1em;
          }

          input::placeholder {
            color: #6096B6;
          }

          input:focus {
            outline: none;
            border-color: #D14081;
          }

          input[type="submit"]:hover, input[type="button"]:hover,
          input[type="submit"]:focus, input[type="button"]:focus {
            cursor: pointer;
            background-position: 0 0;
          }
        `}</style>
      </>
    )
  }
};