#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
Commands for application tasks.
________________________________________________________________________________

Created by brightSPARK Labs
www.brightsparklabs.com
"""

# standard libraries
import sys

# vendor libraries
import click

# local libraries
from appcli.logger import logger
from appcli.models.configuration import Configuration

# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------


class TaskCli:

    # --------------------------------------------------------------------------
    # CONSTRUCTOR
    # --------------------------------------------------------------------------

    def __init__(self, configuration: Configuration):
        self.cli_configuration: Configuration = configuration
        self.orchestrator = configuration.orchestrator

        # ----------------------------------------------------------------------
        # PUBLIC METHODS
        # ----------------------------------------------------------------------

        @click.group(
            invoke_without_command=True,
            help="Commands for application tasks.",
        )
        @click.pass_context
        def task(ctx):
            if ctx.invoked_subcommand is not None:
                # subcommand provided
                return

            click.echo(ctx.get_help())

        @task.command(
            help="Runs a specified application task.",
            context_settings=dict(ignore_unknown_options=True),
        )
        @click.argument("service_name", required=True, type=click.STRING)
        @click.argument("extra_args", nargs=-1, type=click.UNPROCESSED)
        @click.pass_context
        def run(ctx, service_name, extra_args):
            logger.info(
                "Running task [%s] with args [%s] ...",
                service_name,
                extra_args,
            )
            result = self.orchestrator.task(ctx.obj, service_name, extra_args)
            logger.info("Task service finished with code [%i]", result.returncode)
            sys.exit(result.returncode)

        # expose the CLI commands
        self.commands = {
            "task": task,
        }
