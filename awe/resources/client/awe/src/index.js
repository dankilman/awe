import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Babel from '@babel/standalone';
import * as antd from 'antd';
import {Provider} from 'react-redux';
import App from './App';
import Awe from './Awe';
import store from './store';

// Add some globals
window.React = React;
window.Component = Component;
window.Babel = Babel;
window.antd = antd;

Awe.start({store, port: window.aweWebsocketPort, initialState: window.frozenState});
ReactDOM.render(
  <Provider store={store}>
    <App/>
  </Provider>,
  document.getElementById('root')
);
