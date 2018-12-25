A page with a single chart.

The chart is initialized with a single data item and then updated every 5 seconds.

The chart has a moving time window of 3 minutes.

The data added to the chart is transformed by the `2to31` transformer. It builds charts from the different keys
of the 2nd level in the nested dictionary data items. It builds the chart series from the different combinations
of the 3rd and 1st levels in the nested dictionary data items.

In general, every `[Ns...]to[Ms...]` transformer is supported.
