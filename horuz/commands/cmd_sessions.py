import click

from horuz.cli import pass_environment
from horuz.utils.es import HoruzES
from horuz.utils.style import rtable


@click.group()
def cli():
    """
    Manage your Sessions
    """


@cli.command("ls")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.option('-p', '--project', required=True, help='Specify the project.')
@pass_environment
def sessions_ls(ctx, verbose, project):
    """
    List all your sessions
    """
    ctx.verbose = verbose
    hes = HoruzES(project, ctx)
    data = hes.query(term="""
        {
            "size": 0,
            "aggs" : {
                "sessions" : {
                    "terms" : { "field" : "session.keyword", "size": 1000 }
                }
            }
        }
        """, raw=True)
    rtable.add_column("Session", style="cyan", no_wrap=True)
    rtable.add_column("Count", style="cyan")
    for i in data["aggregations"]["sessions"]["buckets"]:
        rtable.add_row(i['key'], str(i['doc_count']))
    ctx.log(rtable)
