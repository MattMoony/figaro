import React from 'react';
import style from './AudioWave.module.scss';
import { Line } from 'react-chartjs-2';
import { AppConsumer, AppContextProps, AppProvider } from './AppContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPause } from '@fortawesome/free-solid-svg-icons';

interface AudioWaveProps {
};

interface AudioWaveState {
  graph: {
    labels: Array<number>;
    datasets: Array<object>;
  };
  running: boolean;
  errorMsg?: string;
};

export default class AudioWave extends React.Component<AudioWaveProps, AudioWaveState> {
  private static graphScale: number = 5;
  public context: AppContextProps;

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
  }

  public start (): void {
    this.context.conf().then(conf => {
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
      }, () => this.getAudioUpdates());
    }).catch(() => this.setState({ errorMsg: 'Failed to retrieve updates ... ', }));
  }

  private getAudioUpdates (): void {
    const sock: WebSocket = new WebSocket(AppProvider.dURL);
    sock.onmessage = (e: MessageEvent) => {
      (e.data as Blob).arrayBuffer().then(b => {
        if (!this.update(Array.from(new Float32Array(b)))) {
          sock.close(1000);
        }
      });
    };
    this.context.send(sock, 'get-audio', { scale: AudioWave.graphScale, })
                .catch(() => this.setState({ errorMsg: 'Failed to retrieve updates ... ', }));
  }

  public update (data: Array<number>): boolean {
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
      <AppConsumer>
        {ctx => {
          this.context = ctx;
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
              <div className={style.overlay} style={{
                display: this.state.errorMsg || !this.context.status.running ? 'flex' : 'none',
              }} title={this.state.errorMsg ? 'Error' : 'Paused'}>
                {this.state.errorMsg || !this.context.status.running && <i><FontAwesomeIcon icon={faPause} /></i>}
              </div>
            </div>
          );
        }}
      </AppConsumer>
    );
  }
};