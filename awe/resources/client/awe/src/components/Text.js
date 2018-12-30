import React, {Component} from 'react';

class Text extends Component {
  render() {
    const {data, props} = this.props.text;
    const {text} = data;
    const lines = (text || '').split('\n');
    return (
      <div>
        {lines.map((line, i) => {
          if (line) {
            return <div {...props} key={i.toString()}>{line}</div>;
          } else {
            return <br {...props} key={i.toString()}/>
          }
        })}
      </div>
    );
  }
}

export default Text;
