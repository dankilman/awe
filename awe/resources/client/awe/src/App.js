import React, {Component} from 'react';
import {connect} from 'react-redux';
import {HotKeys} from 'react-hotkeys';
import components from './components';
import Error from './components/internal/Error'
import Options, {doExport} from './components/internal/Options'
import DisplayOptionsButton from './components/internal/DisplayOptionsButton';
import {instance} from './Awe';
import actions from './actions';
import './App.css';

function processElement(element) {
  element.children = element.children.map(processElement);
  return components[element.elementType](element);
}

class App extends Component {
  render() {
    const elements = this.props.elements.toJS();
    const variables = this.props.variables.toJS();
    const style = this.props.style.toJS();
    const {updateVariable, displayOptions, doExport} = this.props;
    const sortedElements = Object.values(elements).sort((a, b) => a.index - b.index);
    const rootElement = {elementType: 'div', children: [], props: {style}};
    for (const element of sortedElements) {
      element.variables = variables;
      element.updateVariable = updateVariable;
      const parentElement = elements[element.parentId] || rootElement;
      parentElement.children.push(element);
    }
    const processedRoot = processElement(rootElement);
    return (
      <HotKeys
        focused
        keyMap={{displayOptions: 'A A A', doExport: 'A A E'}}
        handlers={{displayOptions, doExport}}>
        <div>
          {processedRoot}
          <Error/>
          <Options/>
          <DisplayOptionsButton/>
        </div>
      </HotKeys>
    )
  }
}

export default connect(
  state => ({
    elements: state.get('elements'),
    variables: state.get('variables'),
    style: state.get('style')
  }),
  dispatch => ({
    updateVariable: (id, value) => {
      dispatch(actions.updateVariable(id, value));
      instance.updateVariable(id, value);
    },
    displayOptions: () => dispatch(actions.displayOptions),
    doExport: doExport(dispatch, true),
  })
)(App);
