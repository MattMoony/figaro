import Document, { Html, Head, Main, NextScript } from 'next/document';

export default class FigaroDocument extends Document {
  public static async getInitialProps (ctx) {
    const initialProps = await Document.getInitialProps(ctx);
    return { ...initialProps };
  }

  public render () {
    return (
      <Html>
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
};