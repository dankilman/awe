import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import App from './App';
import Awe from './Awe';
import Processor from './Processor';
import store from './store';

Awe.start({processor: new Processor(store)});
ReactDOM.render(
  <Provider store={store}>
    <App/>
  </Provider>,
  document.getElementById('root')
);
