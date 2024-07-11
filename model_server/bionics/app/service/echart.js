require('echarts-themes-js/src/chalk');
require('echarts-themes-js/src/essos');
require('echarts-themes-js/src/halloween');
require('echarts-themes-js/src/infographic');
require('echarts-themes-js/src/macarons');
require('echarts-themes-js/src/purple-passion');
require('echarts-themes-js/src/roma');
require('echarts-themes-js/src/romantic');
require('echarts-themes-js/src/shine');
require('echarts-themes-js/src/vintage');
require('echarts-themes-js/src/walden');
require('echarts-themes-js/src/westeros');
require('echarts-themes-js/src/wonderland');

const Service = require('egg').Service;
const echarts = require('echarts');
const { createCanvas } = require('canvas');
const { Readable } = require('stream');

class EchartService extends Service {
  async generateDataUrl(width, height, options, theme = 'westeros', fontSize = 12) {
    const canvas = await this.generate(width, height, options, theme, fontSize);
    return canvas.toDataURL('image/png');
  }

  async generateDataStream(width, height, options, theme = 'westeros', fontSize = 12) {
    const canvas = await this.generate(width, height, options, theme, fontSize);
    const buffer = canvas.toBuffer();
    return Readable.from(buffer);
  }


  async generate(width, height, options, theme = 'westeros', fontSize = 12) {
    const canvas = createCanvas(width, height);
    const canvasContext = canvas.getContext('2d');
    canvasContext.fontSize = fontSize;
    echarts.setPlatformAPI(() => canvas);
    const chart = echarts.init(canvas, theme);
    options.animation = false;
    chart.setOption(options);
    return canvas;
  }
}

module.exports = EchartService;
