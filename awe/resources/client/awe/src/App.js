import {Component} from 'react';
import {connect} from 'react-redux';
import components from './components';
import {instance} from './Awe';
import './App.css';

function processElement(element) {
  element.children = element.children.map(processElement);
  return components[element.elementType](element);
}

class App extends Component {
  render() {
    const {elements, variables, style} = this.props.state.toJS();
    const {updateVariable} = this.props;
    const sortedElements = Object.values(elements).sort((a, b) => a.index - b.index);
    const rootElement = {elementType: 'div', children: [], props: {style}};
    for (const element of sortedElements) {
      element.variables = variables;
      element.updateVariable = updateVariable;
      const parentElement = elements[element.parentId] || rootElement;
      parentElement.children.push(element);
    }
    return processElement(rootElement);
  }
}

export default connect(
  state => ({state}),
  dispatch => ({
    updateVariable: (id, value) => {
      dispatch({type: 'updateVariable', id, value});
      instance.updateVariable(id, value);
    }
  })
)(App);
