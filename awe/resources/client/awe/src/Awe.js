let instance = null;

class Awe {
  constructor({processor, host, port}) {
    this.processor = processor;
    this.finishedInitialFetch = false;
    this.clientId = null;
    this.pendingActions = [];
    this.ws = new WebSocket(`ws://${host}:${port}`);
    this.ws.onmessage = this.onMessage.bind(this);
    this.ws.onerror = (error) => console.error('ws error', error);
    Awe.fetchInitialState().then((initialState) => {
      this.processor.processInitialState(initialState);
      const {version} = initialState;
      for (const pendingAction of this.pendingActions) {
        if (pendingAction.version > version) {
          this.processor.dispatch(pendingAction);
        }
      }
      this.pendingActions = [];
      this.finishedInitialFetch = true;
    });
  }

  static start({processor, host = '127.0.0.1', port = 9000, initialState}) {
    if (initialState) {
      const notSupported = () => console.warn('This is not supported in offline mode');
      instance = {
        call: notSupported,
        updateVariable: notSupported,
        fetchExport: notSupported
      };
      setTimeout(() => processor.processInitialState(initialState), 0);
    } else {
      instance = new Awe({processor, host, port});
    }
    return instance;
  }

  static async fetchInitialState() {
    return await (await fetch('/initial-state')).json();
  }

  async fetchExport() {
    return await fetch('/export');
  }

  call(functionId, kwargs) {
    this.sendMessage({type: 'call', functionId, kwargs, clientId: this.clientId})
  }

  updateVariable(variableId, value) {
    this.sendMessage({type: 'updateVariable', variableId, value, clientId: this.clientId})
  }

  sendMessage(message) {
    this.ws.send(JSON.stringify(message));
  }

  onMessage(message) {
    const action = JSON.parse(message.data);
    if (action.type === 'setClientId') {
      this.clientId = action.clientId;
    } else if (!this.finishedInitialFetch) {
      this.pendingActions.push(action);
    } else {
      this.processor.dispatch(action);
    }
  };

}

export default Awe;
export {instance};
