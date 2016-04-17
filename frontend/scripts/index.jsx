import React from 'react';
import ReactDOM from 'react-dom';

import EventHandler from 'event-handler';

window.events = new EventHandler();
window.onhashchange = function() {
  window.events.trigger('hashchange');
};

let NavItem = React.createClass({
  componentDidMount: function() {
    window.events.on('hashchange', () => {
      this.setState({view: location.hash.substr(3)});
    });
  },

  getInitialState: function() {
    return {
      view: location.hash.substr(3),
    };
  },

  render: function() {
    let selected = false;
    if (this.props.href.substr(3) === this.state.view) {
      selected = true;
    }

    return <li><a className={selected ? 'selected' : ''} {...this.props}>
      { this.props.children }
    </a></li>
  },
});

let Router = React.createClass({
  render: function() {
    let View = require('views/index');
    return <div>
      <View/>
    </div>;
  },
});

ReactDOM.render(<Router/>, document.getElementById('react-body'));
