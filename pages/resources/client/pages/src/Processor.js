class Processor {
  constructor(store) {
    this.store = store;
  }

  processInitialState(initialState) {
    const {variables, children, style} = initialState;
    this.processStyle(style);
    for (const variable of Object.values(variables)) {
      this.processVariable(variable);
    }
    for (const child of children) {
      this.processElement(child);
    }
  }

  processStyle(style) {
    this.dispatch({type: 'setStyle', style})
  }

  processVariable(variable) {
    const {id, value, version} = variable;
    this.dispatch({type: 'newVariable', id, value, version})
  }

  processElement(element) {
    const {children, data, elementType, index, id, parentId, props} = element;
    this.dispatch({type: 'newElement', id, elementType, index, data, parentId, props});
    if (children) {
      for (const child of children) {
        child.parentId = id;
        this.processElement(child);
      }
    }
  }

  dispatch(action) {
    this.store.dispatch(action);
  }
}

export default Processor;
