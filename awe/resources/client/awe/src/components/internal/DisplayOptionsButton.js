import React, {Component} from 'react';
import {connect} from 'react-redux';
import Button from 'antd/lib/button';
import actions from '../../actions';

class DisplayOptionsButton extends Component {
  render() {
    return (
      <Button
        className="display-options-button"
        shape="circle"
        onClick={this.props.onDisplayOptions}
        icon="setting"/>
    );
  }
}

export default connect(
  null,
  dispatch => ({
    onDisplayOptions: () => dispatch(actions.displayOptions)
  })
)(DisplayOptionsButton);
