import React from 'react';

let Index = React.createClass({
  next: function(next) {
    return event => {
      if (event.keyCode === 13) {
        event.preventDefault();
        this.refs[next].focus();
      }
    }
  },

  render: function() {
    return <div className="register-container">
      <div className="register">
        <div>
          <h1>Receba notificações do seu Fundo Imobiliário por e-mail</h1>
          <h4>
            Estamos monitorando notícias de fundos na Bovespa 24
            horas por dia, a cada 20 minutos.
          </h4>
        </div>
        <form>
          <input ref="fii" type="text" placeholder="Procure seus Fundos Imobiliários" onKeyDown={this.next('email')}/>
          <input ref="email" type="email" placeholder="Informe seu e-mail"/>
          <button ref="submit">Monitorar</button>
        </form>
      </div>
    </div>;
  },
});

module.exports = Index;
