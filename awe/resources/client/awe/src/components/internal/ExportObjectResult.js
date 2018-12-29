import React, {Component} from 'react';
import Modal from 'antd/lib/modal';
import Table from 'antd/lib/table';
import {connect} from 'react-redux';
import actions from '../../actions';

function createTableProps(object) {
  const columns = ['Name', 'Value'].map((h) => ({title: h, dataIndex: h, key: h}));
  const dataSource = [];
  for (const [key, value] of Object.entries(object)) {
    dataSource.push({Name: key, Value: value, key: dataSource.length.toString()});
  }
  return {columns, dataSource};
}

class ExportObjectResult extends Component {
  render() {
    let tableComponent = null;
    const {hideExportObjectResult} = this.props;
    let {displayExportObjectResult} = this.props;
    if (displayExportObjectResult) {
      displayExportObjectResult = displayExportObjectResult.toJS();
      const tableProps = createTableProps(displayExportObjectResult);
      tableComponent = <Table {...tableProps} pagination={false}/>
    }
    return (
      <Modal
        onCancel={hideExportObjectResult}
        visible={!!displayExportObjectResult}
        title="Export Result"
        width={1200}
        footer={null}>
        {tableComponent}
      </Modal>
    )
  }
}

export default connect(
  state => ({
    displayExportObjectResult: state.get('displayExportObjectResult')
  }),
  dispatch => ({
    hideExportObjectResult: () => dispatch(actions.hideExportObjectResult)
  })
)(ExportObjectResult);
