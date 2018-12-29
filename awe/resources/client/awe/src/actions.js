export default {
  updateVariable: (id, value) => ({type: 'updateVariable', id, value}),
  displayOptions: {type: 'displayOptions', displayOptions: true},
  hideOptions: {type: 'displayOptions', displayOptions: false},
  startExportLoading: {type: 'exportLoading', exportLoading: true},
  endExportLoading: {type: 'exportLoading', exportLoading: false},
  displayError: (error) => ({type: 'displayError', error}),
  hideError: {type: 'displayError', error: false},
  displayExportObjectResult: (result) => ({type: 'displayExportObjectResult', displayExportObjectResult: result}),
  hideExportObjectResult: {type: 'displayExportObjectResult', displayExportObjectResult: false},
}
