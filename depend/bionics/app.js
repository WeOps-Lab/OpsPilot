const art = require('ascii-art');

class AppBootHook {
  constructor(app) {
    this.app = app;
  }

  async didReady() {
    const rendered = await art.font('BIONICS', 'Doom').completed();
    console.log(rendered);
  }

}

module.exports = AppBootHook;
