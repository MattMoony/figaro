import React from 'react';
import style from './AudioWave.module.scss';
import { Line } from 'react-chartjs-2';
import * as socket from '../utils/socket';

interface AudioWaveProps {
};

interface AudioWaveState {
  graph: {
    labels: Array<number>;
    datasets: Array<object>;
  };
  running: boolean;
};

export default class AudioWave extends React.Component<AudioWaveProps, AudioWaveState> {
  private static graphScale: number = 5;

  constructor (props) {
    super(props);
    this.state = {
      graph: {
        labels: [0, 1, 2, 3, 4, 5],
        datasets: [
          {
            label: 'Sound Wave',
            data: [65, 59, 80, 81, 56, 55, ],
          },
        ],
      },
      running: false,
    };
    socket.onLogout(() => this.stop());
  }

  public start (): void {
    socket.getConf().then(conf => {
      const lbls: Array<number> = new Array(conf.BUF).fill(null).map((_, i) => i);
      this.setState({
        graph: {
          labels: lbls,
          datasets: [
            {
              label: 'Sound Wave',
              data: lbls,
            },
          ],
        },
        running: true,
      }, () => socket.getAudioUpdates(AudioWave.graphScale, this.update.bind(this))
                     .catch(e => window.alert(e)));
    });
  }

  public update (data: Array<number>): boolean {
    // console.log(data, this.state.running);
    this.setState({
      graph: {
        labels: this.state.graph.labels,
        datasets: [
          {
            label: 'Sound Wave',
            data,
          }
        ]
      },
    });
    return this.state.running;
  }

  public stop (): void {
    this.setState({
      running: false,
    });
  }

  public render () {
    return (
      <div className={style.root}>
        <Line data={this.state.graph} options={{
          animation: {
            duration: 0,
          },
          hover: {
            animationDuration: 0,
          },
          responsiveAnimationDuration: 0,
          elements: {
            line: {
              tension: 0,
            },
          },
          showLines: false,
          scales: {
            yAxes: [{
              display: true,
              ticks: {
                min: -1/AudioWave.graphScale*2,
                max: 1/AudioWave.graphScale*2,
              },
            }],
          },
        }} />
      </div>
    );
  }
};