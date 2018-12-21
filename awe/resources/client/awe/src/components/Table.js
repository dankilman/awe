import React, {Component} from 'react';
import AntTable from 'antd/lib/table/Table';

class Table extends Component {
  render() {
    const table = this.props.table;
    const {headers, rows} = table.data;
    const columns = headers.map((header) => ({title: header, dataIndex: header, key: header}));
    const dataSource = rows.map((row) => {
      const {data, id} = row;
      const pairs = data.map((e, i) => [headers[i], e]);
      const result = {key: id};
      for (let [key, value] of pairs) {
        result[key] = value;
      }
      return result;
    });
    return (
      <AntTable
        {...table.props}
        dataSource={dataSource}
        columns={columns}
      />
    );
  }
}

export default Table;
