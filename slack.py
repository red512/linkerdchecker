
from slack_sdk.webhook import WebhookClient

def send_linkerd_slack_message(webhook_url, cluster, category_name, check_result, check_decription, check_hint, check_error):
    # Send the request
    webhook = WebhookClient(webhook_url)
    response = webhook.send(
        text="fallback",
        blocks=[
{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Linkerd check failed on cluster {cluster} *"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*category_name:*\n{category_name}"
				},
				{
					"type": "mrkdwn",
					"text": f"*check_result:*\n{check_result}"
				},
				{
					"type": "mrkdwn",
					"text": f"*check_decription:*\n{check_decription}"
				},
				{
					"type": "mrkdwn",
					"text": f"*check_hint:*\n`{check_hint}`"
				},
				{
					"type": "mrkdwn",
					"text": f"*check_error:*\n{check_error}"
				},
			]
		}
        ]
    )

    # Check the response status code
    if response.status_code != 200:
        raise ValueError(
            f'Request to slack returned an error {response.status_code}, the response is:\n{response.text}'
        )
