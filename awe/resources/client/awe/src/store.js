import {fromJS} from 'immutable';
import {createStore} from 'redux';

const initialState = fromJS({
  roots: {root: {}},
  variables: {},
  style: {},
  displayError: false,
  displayOptions: false,
  exportLoading: false,
  displayExportObjectResult: false,
});

function addChartData(data) {
  return (existingData) => {
    return existingData.withMutations(map => {
      for (const config of data.values()) {
        const title = config.get('title');
        const seriesPath = [title, 'series'];
        if (!map.has(title)) {
          map = map.set(title, fromJS({
            title,
            type: config.get('type'),
            series: [],
          }))
        }
        let existingSeries = map.getIn(seriesPath);
        const newSeriesObject = {};
        const existingSeriesObject = {};
        for (const singleSeries of existingSeries.values()) {
          existingSeriesObject[singleSeries.get('name')] = true;
        }
        for (const singleSeries of config.get('series').values()) {
          if (existingSeriesObject[singleSeries.get('name')]) {
            newSeriesObject[singleSeries.get('name')] = singleSeries.get('data');
          }
        }
        for (const [index, singleSeries] of existingSeries.entries()) {
          if (newSeriesObject[singleSeries.get('name')]) {
            const existingData = singleSeries.get('data');
            const newData = newSeriesObject[singleSeries.get('name')];
            const newExistingData = existingData.concat(newData);
            existingSeries = existingSeries.set(index, singleSeries.set('data', newExistingData));
            map = map.setIn(seriesPath, existingSeries);
          }
        }
        for (const singleSeries of config.get('series').values()) {
          if (!existingSeriesObject[singleSeries.get('name')]) {
            map = map.updateIn(seriesPath, list => list.push(fromJS(singleSeries)))
          }
        }
      }
      return map;
    });
  };
}


const updateElementActions = {
  append: data => list => list.push(data),
  prepend: data => list => list.unshift(data),
  extend: data => list => list.concat(data),
  addChartData
};

function processElement(map, element, rootId) {
  const {children, id, propChildren} = element;
  const newPropChildren = {};
  for (const [prop, {id: propChildRootId, children}] of Object.entries(propChildren)) {
    for (const child of children) {
      newPropChildren[prop] = propChildRootId;
      map = processElement(map, child, propChildRootId);
    }
  }
  element.propChildren = newPropChildren;
  element.rootId = rootId;
  map = newElement(map, element);
  if (children) {
    for (const child of children) {
      child.parentId = id;
      map = processElement(map, child, rootId);
    }
  }
  return map;
}

function processInitialState(state, {style, variables, children}) {
  return state.withMutations(map => {
    map = map.set('style', fromJS(style));
    for (const variable of Object.values(variables)) {
      map = newVariable(map, variable)
    }
    for (const child of children) {
      map = processElement(map, child, 'root');
    }
    return map;
  });
}

function newPropChild(state, {id, prop, elementRootId, elementId}) {
  return state.setIn(['roots', elementRootId, elementId, 'propChildren', prop], id);
}

function newElement(state, {id, rootId, index, data, parentId, elementType, props = {}, propChildren = {}}) {
  return state.setIn(['roots', rootId, id], fromJS({index, id, parentId, data, elementType, props, children: [], propChildren}));
}

function removeElements(state, {entries}) {
  return state.withMutations(map => {
    for (const entry of entries) {
      if (entry.type === 'element') {
        map = map.removeIn(['roots', entry.rootId, entry.id])
      } else if (entry.type === 'root') {
        map = map.removeIn(['roots', entry.id])
      } else if (entry.type === 'variable') {
        map = map.removeIn(['variables', entry.id])
      }

    }
    return map;
  });
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

function updatePath(state, {id, rootId, updateData}){
  const {path, action, data} = updateData;
  const finalPath = ['roots', rootId, id].concat(path);
  if (action === 'set') {
    return state.setIn(finalPath, fromJS(data));
  } else {
    return state.updateIn(finalPath, updateElementActions[action](fromJS(data)));
  }
}

function displayError(state, {error}) {
  return state.set('displayError', error);
}

function displayOptions(state, {displayOptions}) {
  return state.set('displayOptions', displayOptions);
}

function exportLoading(state, {exportLoading}) {
  return state.set('exportLoading', exportLoading);
}

function displayExportObjectResult(state, {displayExportObjectResult}) {
  return state.set('displayExportObjectResult', fromJS(displayExportObjectResult));
}

const reducers = {
  processInitialState,
  newElement,
  newPropChild,
  removeElements,
  newVariable,
  updatePath,
  updateVariable,
  displayError,
  displayOptions,
  exportLoading,
  displayExportObjectResult,
};

function reducer(state = initialState, action) {
  const actionReducer = reducers[action.type];
  return actionReducer ? actionReducer(state, action) : state;
}

export default createStore(reducer);
