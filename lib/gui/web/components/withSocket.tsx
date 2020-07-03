import React from 'react';

const sock: WebSocket = new WebSocket('ws://localhost:51966');

export interface InjectedSocketProps {
  sock: WebSocket;
};

const withSocket = (Component: React.ComponentType<InjectedSocketProps>) => 
  class WithSocket extends React.Component<InjectedSocketProps> {
    render() {
      return <Component sock={sock} />
    }
  };

export default withSocket;