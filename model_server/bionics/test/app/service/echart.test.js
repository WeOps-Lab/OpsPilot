const { app } = require('egg-mock/bootstrap');

describe('echart.test.js', () => {
  it('服务端生成Echart图片', async () => {
    const ctx = app.mockContext();

    const lineOptions = {
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ],
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          data: [ 820, 932, 901, 934, 1290, 1330, 1320 ],
          type: 'line',
          areaStyle: {},
        },
      ],
    };

    await ctx.service.echart.generate(200, 200, lineOptions);
  });
});
