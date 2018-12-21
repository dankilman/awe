import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import App from './App';
import Pages from './Pages';
import Processor from './Processor';
import store from './store';

Pages.start({processor: new Processor(store)});
ReactDOM.render(
  <Provider store={store}>
    <App/>
  </Provider>,
  document.getElementById('root')
);
