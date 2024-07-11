const Controller = require('egg').Controller;


class EchartController extends Controller {

  async generate() {
    const ctx = this.ctx;

    this.logger.debug(`生成Echart图表,请求参数为[${ctx.request.body}]`);

    const options = ctx.request.body.options;
    const width = ctx.request.body.width || ctx.request.body.width || 500;
    const height = ctx.request.body.height || ctx.request.body.height || 200;
    const theme = ctx.request.body.theme || ctx.request.body.theme || 'westeros';
    const fontSize = ctx.request.body.fontSize || ctx.request.body.fontSize || 12;
    const mode = ctx.request.body.mode || ctx.request.body.mode || 'base64';

    let image;
    if (mode === 'stream') {
      ctx.set('Content-Type', 'image/png');
      image = await ctx.service.echart.generateDataStream(
        width, height, options, theme, fontSize
      );
      ctx.body = image;
    } else {
      image = await ctx.service.echart.generateDataUrl(
        width, height, options, theme, fontSize
      );
      ctx.body = image;
    }

    ctx.status = 200;
  }
}

module.exports = EchartController;
