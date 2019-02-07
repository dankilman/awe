import time

from awe import Page, APIClient


def main():
    chart_id = 'chart1'

    # normally, when using the API client, the page is started elsewhere.
    # for the sake of keeping this example simple, the page is started here.
    page = Page()
    page.new_chart(data=[[0]], transform='numbers', id=chart_id)
    page.start()

    # create an API client instance
    client = APIClient()

    # add points to the chart in a loop
    for i in range(10):
        # data is a list of entries. in this case, because we are using the numbers transformer,
        # each entry is a list of numbers itself.
        client.call_method(chart_id, 'add', {'data': [[i]]})
        time.sleep(1)


if __name__ == '__main__':
    main()
