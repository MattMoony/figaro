import React from 'react';
import style from './FiltersManager.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

export default class FiltersManager extends React.Component {
  public render (): React.ReactElement {
    return (
      <div className={style.root}>

        <div className={style.add}>
          <i><FontAwesomeIcon icon={faPlus} /></i>
          Add
        </div>
      </div>
    );
  }
};