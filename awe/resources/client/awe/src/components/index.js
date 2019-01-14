import React from 'react';

import * as antd from 'antd';

import Table from './Table';
import Inline from './Inline';
import Grid from './Grid';
import Text from './Text'
import Chart from './Chart';

const nativeComponents = {
  div: div => (
    <div
      {...div.props}>
      {div.children}
    </div>
  )
};

const connectedComponents = {
  Text: text => (
    <Text
      {...text.props}
      text={text}
    />
  ),
  Card: card => (
    <antd.Card
      {...card.props}>
      {card.children.length > 0 ? card.children : card.data.text}
    </antd.Card>
  ),
  Table: table => (
    <Table
      {...table.props}
      table={table}
    />
  ),
  Grid: grid => (
    <Grid
      {...grid.props}
      grid={grid}
    />
  ),
  Divider: divider => (
    <antd.Divider
      {...divider.props}
    />
  ),
  Collapse: collapse => (
    <antd.Collapse
      {...collapse.props}>
      {collapse.children}
    </antd.Collapse>
  ),
  Panel: panel => (
    <antd.Collapse.Panel
      {...panel.props}>
      {panel.children}
    </antd.Collapse.Panel>
  ),
  Tab: tab => (
    <antd.Tabs.TabPane
      {...tab.props}>
      {tab.children}
    </antd.Tabs.TabPane>
  ),
  Tabs: tabs => (
    <antd.Tabs
      {...tabs.props}>
      {tabs.children || <div/>}
    </antd.Tabs>
  ),
  Button: button => (
    <antd.Button
      {...button.props}
      onClick={() => window.Awe.call(button.id)}>
      {button.data.text}
    </antd.Button>
  ),
  Input: input => (
    <antd.Input
      {...input.props}
      value={input.variables[input.id].value}
      onChange={(e) => window.Awe.updateVariable(input.id, e.target.value)}
      onPressEnter={() => input.data.enter ? window.Awe.call(input.id) : null}
    />
  ),
  Chart: chart => (
    <Chart
      {...chart.props}
      chart={chart}
    />
  ),
  Icon: icon => (
    <antd.Icon
      {...icon.props}
    />
  ),
  Inline: inline => (
    <Inline
      {...inline.props}
      inline={inline}
    />
  ),
  Raw: element => (
    React.createElement(
      element.data.tag,
      element.props,
      element.children.length > 0 ? element.children : undefined
    )
  )
};

const components = Object.assign({}, nativeComponents, connectedComponents);
export default components;
