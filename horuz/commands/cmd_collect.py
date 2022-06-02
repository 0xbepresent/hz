import getpass
import os
import time

import click

from horuz.cli import pass_environment
from horuz.utils.cli import execute_command, log_session, get_sessions
from horuz.utils.es import HoruzES
from horuz.utils.files import collect
from horuz.utils.generators import get_random_name


@click.command("collect", short_help="Collect data from external sources")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
@click.option('-p', '--project', required=True, help='Project name')
@click.option('-s', '--session', required=False, help="Custom session name", autocompletion=get_sessions)
@click.option('-c', '--cmd', required=False, help='Generate data from external command')
@click.option('-f', '--filename', required=False, type=click.File('r'), help="JSON file")
@click.option('-fd', '--filter-dups', required=False, help="Filter by duplicates. Put the fields separated with commas that are constantly repeated, you will not keep repeated data")
@click.option('-rfd', '--remove-filter-dups', required=False, help="Only available if -fd is specified. Remove the duplicate fields, save only the data you need, if the option is not specified, the duplicate tuple will be removed. Example usage -rfd html,resultfile")
@pass_environment
def cli(ctx, verbose, project, session, cmd, filename, filter_dups, remove_filter_dups):
    """
    Collect Data from external sources
    """
    ctx.verbose = verbose
    session = session if session else get_random_name()
    log_session(session)
    if cmd and "ffuf" in cmd:
        # Creating all the neccesary paths
        tmp_path = "/tmp/ffuf_{}/{}".format(
            getpass.getuser(), int(time.time()))
        tmp_output = "{}/ffuf_http.json".format(tmp_path)
        os.popen("mkdir -p {} 2>/dev/null".format(tmp_path))
        os.popen("touch {}".format(tmp_output))
        # Adding output location and raw html path
        cmd = "{} -c -o='{}' -od {}".format(cmd, tmp_output, tmp_path)
        executed = execute_command(cmd)
        if executed:
            ctx.log("Command execution done! :sparkles:")
            is_command_done = True
            # Collecting files in ElasticSeach
            ctx.vlog("Getting the JSON Files.")
            ffuf_files = collect(path=tmp_path, prefix="ffuf_http")
            ctx.vlog("Uploading info to ElasticSeach.")
            hes = HoruzES(project, ctx)
            hes.save_json(
                files=ffuf_files,
                session=session,
                filter_dups=filter_dups,
                remove_filter_dups=remove_filter_dups)
            # Deleting remainign files
            os.popen("rm -rf {}".format(tmp_path))
        else:
            ctx.log("Command execution fail! :collision:")
    if filename:
        hes = HoruzES(project, ctx)
        ctx.vlog("Uploading file info to ElasticSeach.")
        hes.save_json(
            files=[filename.name],
            session=session,
            filter_dups=filter_dups,
            remove_filter_dups=remove_filter_dups)
