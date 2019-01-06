import React, {Component} from 'react';

class Inline extends Component {
  render() {
    const {data, props, children} = this.props.inline;
    delete props.key;
    const {text} = data;
    return (
      <span {...props}>
        {children.length > 0 ? children : text}
      </span>
    );
  }
}

export default Inline;
