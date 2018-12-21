import React, {Component} from 'react';
import {Row, Col} from 'antd/lib/grid';

class Grid extends Component {
  render() {
    const {props, data, children} = this.props.grid;
    delete props.key;
    const {columns, childColumns} = data;
    const singleColumnSpan = 24 / columns;
    const rows = [];
    let currentRow = [];
    let currentRowSpan = 0;
    for (let i = 0; i < children.length; i++) {
      const key = i.toString();
      const childComponent = children[i];
      const childColumnSpan = singleColumnSpan * childColumns[i];
      if (currentRowSpan + childColumnSpan > 24) {
        rows.push(currentRow);
        currentRowSpan = 0;
        currentRow = [];
      }
      currentRowSpan += childColumnSpan;
      currentRow.push(
        <Col
          {...props}
          key={key}
          span={childColumnSpan}>
          {childComponent}
        </Col>
      )
    }
    if (currentRow.length > 0) {
      rows.push(currentRow);
    }
    const paddingBottom = props.gutter || 0;
    return rows.map((row, i) => (
      <Row
        {...props}
        key={i.toString()}
        style={{paddingBottom}}>
        {row}
      </Row>
    ));
  }
}

export default Grid;
