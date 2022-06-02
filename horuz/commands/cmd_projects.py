import click

from horuz.cli import pass_environment
from horuz.utils.es import HoruzES
from horuz.utils.style import rtable


@click.group()
def cli():
    """
    Manage your ElasticSeach Projects
    """
    pass


@cli.command("rm")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.option('-p', '--project', required=True, help='Specify the project to delete.')
@pass_environment
def projects_rm(ctx, verbose, project):
    """
    Delete ElasticSeach Project
    """
    ctx.verbose = verbose
    click.confirm(
        "Are you sure you want to delete {}?".format(project),
        abort=True,
        default=True)
    # Delete the Index Project
    hes = HoruzES(project, ctx)
    deleted = hes.delete()
    if deleted:
        ctx.log("Project {} was deleted.".format(project))


@cli.command("ls")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def projects_ls(ctx, verbose):
    """
    List all your ElasticSearch Projects
    """
    ctx.verbose = verbose
    hes = HoruzES("", ctx)
    indexes = hes.indexes()
    if indexes:
        rtable.add_column("Projects", style="cyan", no_wrap=True)
        for i in indexes:
            rtable.add_row(i)
        ctx.log(rtable)


@cli.command("describe")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.option('-p', '--project', required=True, help='Specify the project to delete.')
@pass_environment
def projects_describe(ctx, verbose, project):
    """
    Project fields
    """
    ctx.verbose = verbose
    hes = HoruzES(project, ctx)
    mapping = hes.project_mapping()
    if mapping:
        rtable.add_column("{} fields".format(project), style="cyan", no_wrap=True)
        for i in mapping:
            rtable.add_row(i)
        ctx.log(rtable)
    else:
        ctx.log("Project does not exist!")
