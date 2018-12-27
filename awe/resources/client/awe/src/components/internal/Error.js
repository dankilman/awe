import React, {Component} from 'react';
import Modal from 'antd/lib/modal';
import Icon from 'antd/lib/icon';
import {connect} from 'react-redux';
import actions from '../../actions';

class Error extends Component {
  render() {
    return (
      <Modal
        onCancel={this.props.hideError}
        visible={!!this.props.displayError}
        title={
          <div>
            <Icon type="exclamation-circle" style={{paddingRight: 10, color: 'red'}}/>
            <span>Error</span>
          </div>
        }
        footer={null}>
        <pre><code>{this.props.displayError}</code></pre>
      </Modal>
    )
  }
}

export default connect(
  state => ({
    displayError: state.get('displayError')
  }),
  dispatch => ({
    hideError: () => dispatch(actions.hideError)
  })
)(Error);
