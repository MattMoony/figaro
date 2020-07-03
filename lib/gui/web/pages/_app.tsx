import React from 'react';
import App from 'next/app';

export default class FigaroApp extends App {
  public render () {
    const { Component, pageProps } = this.props;
    return (
      <>
        <Component {...pageProps} />
        <style jsx global>{`
          @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap');
          @import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');
          
          html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: #0B3954;
            color: #EEF1FF;
          }
        `}</style>
      </>
    );
  }
};