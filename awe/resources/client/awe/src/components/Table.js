import React, {Component} from 'react';
import * as antd from 'antd';


const sorter = (key) => (a, b) => {
  const aVal = a[key];
  const bVal = b[key];
  if (aVal === bVal) {
    return 0;
  }
  const isAStringOrNumber = typeof aVal === 'string' || typeof aVal === 'number';
  const isBStringOrNumber = typeof bVal === 'string' || typeof bVal === 'number';
  if (isAStringOrNumber && isBStringOrNumber) {
    return aVal < bVal ? -1 : 1
  }
  return 0;
};


class Table extends Component {
  render() {
    const table = this.props.table;
    const {process} = table;
    const {headers, rows} = table.data;
    const columns = headers.map((header) => ({
      title: header,
      dataIndex: header,
      key: header,
      sorter: sorter(header)
    }));
    const dataSource = rows.map((row) => {
      const {data, id} = row;
      const pairs = data.map((e, i) => [headers[i], e]);
      const result = {key: id};
      for (let [columnKey, value] of pairs) {
        result[columnKey] = process(value);
      }
      return result;
    });
    return (
      <antd.Table
        {...table.props}
        dataSource={dataSource}
        columns={columns}
      />
    );
  }
}

export default Table;
