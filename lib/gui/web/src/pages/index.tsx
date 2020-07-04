import React from 'react';
import style from './index.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faStop } from '@fortawesome/free-solid-svg-icons';
import withSocket from '../components/withSocket';

interface IndexProps {
  sock: WebSocket;
}

class Index extends React.Component<IndexProps, void> {
  public render () {
    return (
      <article className={style.article}>
        <footer>
          <i><FontAwesomeIcon icon={faPlay} /></i>
        </footer>
      </article>
    );
  }
};

export default Index;