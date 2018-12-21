import React from 'react';
import Card from 'antd/lib/card';
import Divider from 'antd/lib/divider';
import Tabs from 'antd/lib/tabs';
import Button from 'antd/lib/button';
import Input from 'antd/lib/input';
import Table from './Table';
import Grid from './Grid';
import Text from './Text'
import Chart from './Chart';
import {instance} from '../Pages';

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
    <Card
      {...card.props}>
      {card.children.length > 0 ? card.children : card.data.text}
    </Card>
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
    <Divider
      {...divider.props}
    />
  ),
  Tab: tab => (
    <Tabs.TabPane
      {...tab.props}>
      {tab.children}
    </Tabs.TabPane>
  ),
  Tabs: tabs => (
    <Tabs
      {...tabs.props}>
      {tabs.children || <div/>}
    </Tabs>
  ),
  Button: button => (
    <Button
      {...button.props}
      onClick={() => instance.call(button.id)}>
      {button.data.text}
    </Button>
  ),
  Input: input => (
    <Input
      {...input.props}
      value={input.variables[input.id].value}
      onChange={(e) => input.updateVariable(input.id, e.target.value)}
      onPressEnter={() => input.data.enter ? instance.call(input.id) : null}
    />
  ),
  Chart: chart => (
    <Chart
      {...chart.props}
      chart={chart}
    />
  )
};

const components = Object.assign({}, nativeComponents, connectedComponents);
export default components;
