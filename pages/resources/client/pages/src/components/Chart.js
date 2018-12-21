import lodash from 'lodash';
import React, {Component} from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';


function callback(chart) {
  const {movingWindow} = chart.userOptions.callbackOptions;
  if (movingWindow) {
    const fn = (e, init) => {
      const xAxis = chart.xAxis[0];
      const currentExtremes = xAxis.getExtremes();
      const {dataMax} = currentExtremes;
      const range = xAxis.minRange;
      xAxis.setExtremes(dataMax - range, dataMax + 8 * 1000, init);
    };
    fn(null, true);
    Highcharts.addEvent(chart, 'update', fn);
  }
}


class Chart extends Component {
  render() {
    const {chart} = this.props;
    const {data, options, movingWindow} = chart.data;
    const charts = [];
    for (const config of Object.values(data)) {
      const {series, title, type} = config;
      const defaultOptions = {
        callbackOptions: {
          movingWindow
        },
        chart: {
          type,
          height: 300
        },
        title: {text: title},
        plotOptions: {
          [type]: {
            marker: {
              enabled: false,
              symbol: 'circle'
            }
          }
        },
        time: {
          useUTC: false,
        },
        xAxis: {
          minRange: movingWindow ? movingWindow * 1000 : undefined,
          type: 'datetime',
        },
        yAxis: {
          title: {text: ''},
          tickPixelInterval: 36
        }
      };
      let finalOptions;
      if (Object.keys(options || {}).length > 0) {
        lodash.defaultsDeep(options, [defaultOptions]);
        finalOptions = options;
      } else {
        finalOptions = defaultOptions;
      }
      finalOptions.series = series;
      charts.push(finalOptions);
    }

    return (
      <div>
        {charts.map((chart, i) => (
          <HighchartsReact
            callback={callback}
            key={i.toString()}
            highcharts={Highcharts}
            options={chart}
          />
        ))}
      </div>
    );
  }
}

export default Chart;
