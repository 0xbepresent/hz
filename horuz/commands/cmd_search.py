import click
import json
import time
import datetime

from horuz.cli import pass_environment
from horuz.utils.formatting import beautify_query
from horuz.utils.es import HoruzES
from horuz.utils.style import rtable


@click.command("search", short_help="Search data in ES.")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.option('-p', '--project', required=True, help='Project name')
@click.option('-q', '--query', required=True, help='Query to ElasticSeach')
@click.option('-f', '--fields', help='Specify the fields you want.')
@click.option('-s', '--size', default=100, type=click.IntRange(1, 10000), help='Specify the output size. Range 1-10000')
@click.option('-o', '--order', default="time:desc", help='Specify the sorting of the query. Default time:desc')
@click.option('-oJ', is_flag=True, help="JSON Output")
@click.option('-tl', '--tail', is_flag=True, help="Get the last live info from ElasticSearch. Based on your custom order flag.")
@pass_environment
def cli(ctx, verbose, project, query, fields, size, order, oj, tail):
    """
    Get data from ElasticSeach.
    """
    ctx.verbose = verbose
    hes = HoruzES(project, ctx)
    fields = fields.split(",") if fields else []
    if oj:
        # JSON Output
        data = beautify_query(
            hes.query(term=query, size=size, order=order, fields=fields),
            fields,
            output="json")
        click.echo(data)
    elif tail:
        # Get the last infor from elasticsearch
        if not fields:
            fields = ["_id", "time", "session"]
        showed_ids = []
        while True:
            data = beautify_query(
                hes.query(term=query, size=1, order=order, fields=fields),
                fields,
                output="interactive")
            if data and data[0]['_id'] not in showed_ids:
                showed_ids.append(data[0]['_id'])
                click.echo(json.dumps(data[0]))
            time.sleep(2)
    else:
        # Interactive Output
        # Default fields if nothing were introduced
        if not fields:
            fields = ["_id", "time", "session"]
        data = beautify_query(
            hes.query(term=query, size=size, order=order, fields=fields),
            fields,
            output="interactive")
        # Adding columns
        if data:
            for column in data[0].keys():
                rtable.add_column(column, style="cyan")
            for i in data:
                rtable.add_row(*i.values())
            ctx.log(rtable, pager=True)
