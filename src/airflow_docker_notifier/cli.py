import functools
import logging
import sys

import click
from airflow_docker_notifier.notification import emit_slack_notification

logger = logging.getLogger(__name__)


def cli_command(fn):
    @functools.wraps(fn)
    def decorator(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
        except Exception as e:
            logger.exception(str(e))
            sys.exit(1)

        sys.exit(int(bool(result)))

    return decorator


@click.group(help="A utility for emitting notifications.")
def main():
    logging.basicConfig(level=logging.DEBUG)


@main.command()
@click.argument("message")
@click.option(
    "--api-token",
    help="The slack secret token used to authorize with slack, as a particular bot",
)
@click.option("--channel", help="The channel into which the message should be emitted")
@click.option(
    "--message-type",
    help="The kind of message being emitted: success, failure, warning",
)
@click.option("--dag-id", help="The id of the dag being run")
@click.option("--task-id", help="The id of the task being run")
@click.option("--execution-date", help="The execution date of the dag being run")
@click.option(
    "--base-url", help="The base url of the airflow instance on which the task is run"
)
@click.option("--link", multiple=True)
@click.option("--mention", multiple=True)
@cli_command
def slack(
    message,
    api_token,
    channel,
    message_type,
    dag_id,
    task_id,
    execution_date,
    base_url,
    link,
    mention,
):
    # Collect all the supplied links and split them by a delimeter "Display::http://link"
    links = [item.split("::", 1) for item in link]

    return emit_slack_notification(
        message=message,
        api_token=api_token,
        channel=channel,
        message_type=message_type,
        dag_id=dag_id,
        task_id=task_id,
        execution_date=execution_date,
        base_url=base_url,
        links=links,
        mentions=mention,
    )
