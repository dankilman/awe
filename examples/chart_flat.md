A page with a single chart.

The chart is initialized with a single data item and then updated every 0.7 seconds with a new data item.

The chart has a moving time window of 3 minutes.

The data added to the chart is transformed by the `flat` transformer. It builds charts from the different combinations
of the `chart_mapping` list. It builds the chart series from the different combinations
of the `series_mapping` list. The values are extracted from the `value_key` key.
