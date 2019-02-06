import json
import sys
from functools import partial

import click
import six
import yaml

from awe import Page, APIClient
from awe.page import DEFAULT_WIDTH, DEFAULT_TITLE
from awe.api_client import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_WEBSOCKET_PORT


option = partial(click.option, show_default=True)


@click.group()
@option('-h', '--host', default=DEFAULT_HOST, help='Server host.')
@option('-p', '--port', type=int, default=DEFAULT_PORT, help='Server port.')
@option('-o', '--output-format', default='json', type=click.Choice(['json', 'yaml']),
        help='Command output format. (choices: json, yaml)')
@option('-l', '--output-line', is_flag=True, help='Compact single line JSON output.')
@option('-q', '--quiet', is_flag=True, help='Silence all command output.')
@click.pass_context
def cli(ctx, host, port, output_format, output_line, quiet):
    """
    A CLI to start, query and manipulate ``awe`` pages.
    """
    ctx.obj = Context(
        client=APIClient(host=host, port=port),
        output_format=output_format,
        output_line=output_line,
        quiet=quiet
    )


@cli.command()
@option('-t', '--title', default=DEFAULT_TITLE, help='Page title.', show_default=True)
@option('-w', '--width', type=int, default=DEFAULT_WIDTH, help='Page width.')
@option('-b', '--open-browser', is_flag=True, help='Open a browser with the newly created page.')
@option('-o', '--obj', help='Optional top level element definition.')
@option('-p', '--params', help='Keyword arguments to use when creating ``obj`` if supplied.')
@option('-s', '--style', help='Customize root element style.')
@option('--host', default=DEFAULT_HOST, help='Start page on a custom webserver host (interface).')
@option('--port', type=int, default=DEFAULT_PORT, help='Start page on a custom webserver port.')
@option('--websocket-port', type=int, default=DEFAULT_WEBSOCKET_PORT, help='Start page on a custom websocket port.')
@click.pass_obj
def start(ctx, title, width, open_browser, obj, params, style, host, port, websocket_port):
    """
    Start a new page.
    """
    try:
        page = Page(
            title=title,
            width=width,
            host=host,
            port=port,
            websocket_port=websocket_port,
            style=ctx.parse_object(style)
        )
        page.start(open_browser=open_browser)
        if obj:
            obj = ctx.parse_object(obj)
            params = ctx.parse_object(params)
            page.new(obj, **params)
        page.block()
    except Exception:
        if ctx.quiet:
            sys.exit(1)
        else:
            raise


@cli.command()
@click.pass_obj
def status(ctx):
    """
    Get server status.
    """
    ctx.verify_alive()
    ctx.echo('Server is alive')


@cli.command()
@option('-d', '--include-data', is_flag=True, help='Include element data in output.')
@option('-p', '--include-props', is_flag=True, help='Include element props in output.')
@click.pass_obj
def ls(ctx, include_data, include_props):
    """
    List all elements.
    """
    ctx.verify_alive()
    result = ctx.client.get_elements(
        include_data=include_data,
        include_props=include_props
    )
    ctx.echo_object(result)


@cli.command()
@option('-e', '--element-id', required=True, help='Element ID.')
@click.pass_obj
def get(ctx, element_id):
    """
    Get a registered element.
    """
    ctx.verify_alive()
    result = ctx.client.get_element(element_id)
    ctx.echo_object(result)


@cli.command()
@option('-o', '--obj', required=True, help='Element definition.')
@option('-p', '--params', help='Keyword arguments to use when creating ``obj``.')
@option('-e', '--element-id', help='Optionally specify an element ID. (one will be generated otherwise)')
@option('-r', '--root-id', help='Optionally specify a different root to creat the element under. '
                                'If not specified, and ``parent_id`` is not supplied, the main ``page`` root '
                                'will be used.')
@option('-c', '--parent-id', help='Optionally specify the element create the new element under.')
@option('-n', '--new-root', is_flag=True, help='Create element under a new root.')
@click.pass_obj
def new(ctx, obj, params, element_id, root_id, parent_id, new_root):
    """
    Create a new element.
    """
    ctx.verify_alive()
    result = ctx.client.new_element(
        obj=ctx.parse_object(obj),
        params=ctx.parse_object(params),
        element_id=element_id,
        root_id=root_id,
        parent_id=parent_id,
        new_root=new_root
    )
    ctx.echo_object(result)


@cli.command()
@option('-e', '--element-id', required=True, help='Element ID.')
@click.pass_obj
def remove(ctx, element_id):
    """
    Remove an element.
    """
    ctx.verify_alive()
    result = ctx.client.remove_element(element_id)
    ctx.echo_object(result)


@cli.command('new-prop')
@option('-e', '--element-id', required=True, help='Element ID.')
@option('-n', '--name', required=True, help='Prop name.')
@click.pass_obj
def new_prop(ctx, element_id, name):
    """
    Create a new prop child.
    """
    ctx.verify_alive()
    result = ctx.client.new_prop(
        element_id=element_id,
        name=name
    )
    ctx.echo_object(result)


@cli.command('update-data')
@option('-e', '--element-id', required=True, help='Element ID.')
@option('-d', '--data', required=True, help='New data to set on element.')
@click.pass_obj
def update_data(ctx, element_id, data):
    """
    Update element data.
    """
    ctx.verify_alive()
    result = ctx.client.update_data(
        element_id=element_id,
        data=ctx.parse_object(data)
    )
    ctx.echo_object(result)


@cli.command('update-props')
@option('-e', '--element-id', required=True, help='Element ID.')
@option('-p', '--props', required=True, help='New props to set on element.')
@click.pass_obj
def update_props(ctx, element_id, props):
    """
    Update element props.
    """
    ctx.verify_alive()
    result = ctx.client.update_props(
        element_id=element_id,
        props=ctx.parse_object(props)
    )
    ctx.echo_object(result)


@cli.command('update-prop')
@option('-e', '--element-id', required=True, help='Element ID.')
@option('-p', '--path', required=True, help='Prop path.')
@option('-v', '--value', required=True, help='Prop new value.')
@click.pass_obj
def update_prop(ctx, element_id, path, value):
    """
    Update an element prop.
    """
    ctx.verify_alive()
    result = ctx.client.update_prop(
        element_id=element_id,
        path=ctx.parse_object(path),
        value=ctx.parse_object(value)
    )
    ctx.echo_object(result)


@cli.command()
@option('-e', '--element-id', required=True, help='Element ID.')
@option('-m', '--method', required=True, help='Method name.')
@option('-k', '--kwargs', help='Keyword arguments passed to method invocation.')
@click.pass_obj
def call(ctx, element_id, method, kwargs):
    """
    Call an element method.
    """
    ctx.verify_alive()
    result = ctx.client.call_method(
        element_id=element_id,
        method_name=method,
        kwargs=ctx.parse_object(kwargs)
    )
    ctx.echo_object(result)


@cli.command('ls-variables')
@click.pass_obj
def ls_variables(ctx):
    """
    List all variables.
    """
    ctx.verify_alive()
    result = ctx.client.get_variables()
    ctx.echo_object(result)


@cli.command('get-variable')
@option('-v', '--variable-id', required=True, help='Variable ID.')
@click.pass_obj
def get_variable(ctx, variable_id):
    """
    Get a registered variable.
    """
    ctx.verify_alive()
    result = ctx.client.get_variable(variable_id)
    ctx.echo_object(result)


@cli.command('new-variable')
@option('-v', '--variable-id', help='Optionally supply a variable ID, one will be generated otherwise.')
@option('-d', '--value', required=True, help='Initial variable value.')
@click.pass_obj
def new_variable(ctx, variable_id, value):
    """
    Create a new variable.
    """
    ctx.verify_alive()
    result = ctx.client.new_variable(
        variable_id=variable_id,
        value=ctx.parse_object(value)
    )
    ctx.echo_object(result)


@cli.command('update-variable')
@option('-v', '--variable-id', required=True, help='Variable ID.')
@option('-d', '--value', required=True, help='Variable new value.')
@click.pass_obj
def update_variable(ctx, variable_id, value):
    """
    Update a variable.
    """
    ctx.verify_alive()
    result = ctx.client.update_variable(
        variable_id=variable_id,
        value=ctx.parse_object(value)
    )
    ctx.echo_object(result)


@cli.command('call-function')
@option('-f', '--function-id', required=True, help='Function ID.')
@option('-k', '--kwargs', help='Keyword arguments passed to function invocation.')
@click.pass_obj
def call_function(ctx, function_id, kwargs):
    """
    Call a registered function.
    """
    ctx.verify_alive()
    result = ctx.client.call_function(
        function_id=function_id,
        kwargs=ctx.parse_object(kwargs)
    )
    ctx.echo_object(result)


class Context(object):

    def __init__(self, client, output_format, output_line, quiet):
        self.client = QuietClient(client=client) if quiet else client
        self.output_format = output_format
        self.output_line = output_line
        self.quiet = quiet

    def verify_alive(self):
        try:
            result = self.client.get_status()
            if not result['status'] == 'alive':
                raise RuntimeError
        except Exception:
            if self.quiet:
                sys.exit(1)
            else:
                raise click.exceptions.ClickException('Server seems down')

    def parse_object(self, obj):
        try:
            if obj is None:
                obj = {}
            if isinstance(obj, six.string_types):
                if obj.startswith('@'):
                    with open(obj[1:]) as f:
                        obj = f.read()
                obj = yaml.safe_load(obj)
            return obj
        except Exception:
            if self.quiet:
                sys.exit(1)
            else:
                raise

    def echo(self, message):
        if self.quiet:
            return
        click.echo(message)

    def echo_object(self, obj):
        if self.quiet:
            return
        if self.output_format == 'json':
            if self.output_line:
                output = json.dumps(obj, separators=(',', ':'))
            else:
                output = json.dumps(obj, sort_keys=True, indent=2)
        else:
            output = yaml.safe_dump(obj, default_flow_style=False)
        click.echo(output)


class QuietClient(object):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def quiet_callable(fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception:
                sys.exit(1)
        return wrapper

    def __getattr__(self, item):
        maybe_callable = getattr(self.client, item)
        if not callable(maybe_callable):
            return maybe_callable
        return self.quiet_callable(maybe_callable)


if __name__ == '__main__':
    cli()
