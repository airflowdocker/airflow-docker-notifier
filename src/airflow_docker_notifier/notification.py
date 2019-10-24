import os
from urllib.parse import urlencode

from airflow_docker_notifier.client import SectionItem, SlackClient, TextSection


def emit_slack_notification(
    message,
    api_token,
    channel,
    message_type=None,
    dag_id=None,
    task_id=None,
    execution_date=None,
    base_url=None,
    links=None,
    mentions=None,
):
    text_sections = []
    client = SlackClient.from_config(api_token=api_token, channel=channel)

    if base_url:
        env = os.environ.get("ENV", "n/a")
        dag_params = {"dag_id": dag_id, "execution_date": execution_date}
        log_params = {**dag_params, "task_id": task_id}
        text_sections.append(
            TextSection(
                name="Info",
                items=[
                    SectionItem(display_name=f"Env: {env}", text=base_url),
                    SectionItem(
                        display_name=f"DAG: {dag_id}",
                        text=f"{base_url}/graph?{urlencode(dag_params)}",
                    ),
                    SectionItem(
                        display_name=f"Task logs: {task_id}",
                        text=f"{base_url}/log?{urlencode(log_params)}",
                    ),
                ],
            )
        )

    if links:
        link_items = [SectionItem.from_raw(link) for link in links]
        text_sections.append(TextSection(name="Links", items=link_items))

    client.post_message(
        message,
        message_type=message_type,
        text_sections=text_sections,
        mentions=mentions,
    )
