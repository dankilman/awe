let instance = null;

class Awe {
  constructor({processor, host, port}) {
    this.processor = processor;
    this.finishedInitialFetch = false;
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

  static start({processor, host = '127.0.0.1', port = 9000}) {
    instance = new Awe({processor, host, port});
    return instance;
  }

  static async fetchInitialState() {
    return await (await fetch('/initial-state')).json();
  }

  call(functionId, kwargs) {
    this.sendMessage({type: 'call', functionId, kwargs})
  }

  updateVariable(variableId, value) {
    this.sendMessage({type: 'updateVariable', variableId, value})
  }

  sendMessage(message) {
    this.ws.send(JSON.stringify(message));
  }

  onMessage(message) {
    const action = JSON.parse(message.data);
    if (!this.finishedInitialFetch) {
      this.pendingActions.push(action);
    } else {
      this.processor.dispatch(action);
    }
  };

}

export default Awe;
export {instance};
