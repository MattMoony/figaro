const React = require('react');
const Layout = require('./src/components/BaseLayout').default;

exports.wrapPageElement = ({ element, props }) => {
  return <Layout {...props}>{element}</Layout>
};