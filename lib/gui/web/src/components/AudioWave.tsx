import React from 'react';
import style from './AudioWave.module.scss';
import { Line, ChartData } from 'react-chartjs-2';

interface AudioWaveProps {
};

interface AudioWaveState {
  labels: Array<number>;
  datasets: Array<object>;
};

export default class AudioWave extends React.Component<AudioWaveProps, AudioWaveState> {
  constructor (props) {
    super(props);
    this.state = {
      labels: [0, 1, 2, 3, 4, 5],
      datasets: [
        {
          label: 'Sound Wave',
          data: [65, 59, 80, 81, 56, 55, ],
        }
      ],
    };
  }

  public render () {
    return (
      <div className={style.root}>
        <Line data={this.state} />
      </div>
    );
  }
};