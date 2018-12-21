import {fromJS} from 'immutable';
import {createStore} from 'redux';

const initialState = fromJS({elements: {}, variables: {}, style: {}});

function addChartData(data) {
  return (existingData) => {
    return existingData.withMutations(map => {
      for (const config of data.values()) {
        const title = config.get('title');
        const newSeriesObject = {};
        for (const singleSeries of config.get('series').values()) {
          newSeriesObject[singleSeries.get('name')] = singleSeries.get('data');
        }
        const seriesPath = [title, 'series'];
        let existingSeries = map.getIn(seriesPath);
        for (const [index, singleSeries] of existingSeries.entries()) {
          const existingData = singleSeries.get('data');
          const newData = newSeriesObject[singleSeries.get('name')];
          const newExistingData = existingData.concat(newData);
          existingSeries = existingSeries.set(index, singleSeries.set('data', newExistingData));
          map = map.setIn(seriesPath, existingSeries);
        }
      }
      return map;
    });
  };
}


const updateElementActions = {
  append: data => list => list.push(data),
  prepend: data => list => list.unshift(data),
  addChartData
};

function setStyle(state, {style}) {
  return state.set('style', style);
}

function newElement(state, {id, index, data, parentId, elementType, props = {}}) {
  return state.setIn(['elements', id], fromJS({index, id, parentId, data, elementType, props, children: []}));
}

function newVariable(state, {id, value, version}) {
  return state.setIn(['variables', id], fromJS({id, value, version}));
}

function updateVariable(state, {id, value, version = -1}) {
  const internal = version === -1;
  const currentVersion = state.getIn(['variables', id, 'version']);
  if (!internal && currentVersion >= version) {
    return state;
  }
  const update = {value};
  if (!internal) {
    update.version = version;
  }
  return state.mergeIn(['variables', id], fromJS(update));
}

function updatePath(prefix) {
  return (state, {id, updateData}) => {
    const {path = [], action, data} = updateData;
    const fullPath = [prefix, id].concat(path);
    if (action === 'set') {
      return state.setIn(fullPath, fromJS(data));
    } else {
      return state.updateIn(fullPath, updateElementActions[action](fromJS(data)));
    }
  }
}

const reducers = {
  setStyle,
  newElement,
  newVariable,
  updateElement: updatePath('elements'),
  updateVariable
};

function reducer(state = initialState, action) {
  const actionReducer = reducers[action.type];
  return actionReducer ? actionReducer(state, action) : state;
}

export default createStore(reducer);
