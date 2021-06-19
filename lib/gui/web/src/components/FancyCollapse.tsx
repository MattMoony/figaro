import { faCaretDown, faCaretUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import style from './FancyCollapse.module.scss';

interface FancyCollapseProps {
  title: string;
  titleElements?: string|React.ReactElement|React.ReactElement[];
  children?: string|React.ReactElement|React.ReactElement[];
}

interface FancyCollapseState {
  expanded: boolean;
}

export default class FancyCollapse extends React.Component<FancyCollapseProps, FancyCollapseState> {
  
  constructor (props) {
    super(props);
    this.state = {
      expanded: false,
    };
  }

  private hasBody (): boolean {
    return this.props.children.toString().trim() !== '';
  }

  private onBannerClick (): void {
    this.setState({
      expanded: this.hasBody() && !this.state.expanded,
    });
  }

  public render (): React.ReactElement {
    return (
      <div className={style.root}>
        <div onClick={this.onBannerClick.bind(this)} style={{
          paddingBottom: this.state.expanded ? '5px' : '0',
          borderBottom: this.state.expanded ? '2px solid #1a6594' : 'none',
        }}>
          {this.props.title}
          <div>
            {this.hasBody() ? <i><FontAwesomeIcon icon={this.state.expanded ? faCaretUp : faCaretDown}/></i> : ''}
            {this.props.titleElements}
          </div>
        </div>
        <div style={{
          display: this.state.expanded ? 'block' : 'none',
        }}>
          {this.props.children}
        </div>
      </div>
    );
  }
}