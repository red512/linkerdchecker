import argparse
import json
import subprocess
import logging
import slack

logging.basicConfig(level=logging.INFO)


def check_linkerd_errors(cluster, webhook_url, json_dict):
    if not json_dict.get("success", False):
        for category in json_dict.get("categories", []):
            for check in category.get("checks", []):
                if check["result"] == "error" and check_ignore(cluster, category["categoryName"],check["error"] ):
                    logging.warning("Error found in linkerd check")
                    slack.send_linkerd_slack_message(webhook_url,cluster,category["categoryName"],check["result"],check["description"],check["hint"],check["error"])
                elif check["result"] == "error" and not check_ignore(cluster, category["categoryName"],check["error"] ):
                    logging.info("Acknowledged error")
    else:
        logging.info("No errors found")



def get_cluster_name(json_dict):
    for cluster in json_dict.get("clusters", []):
        return cluster["name"]
    logging.warning("Cluster not found")
    return None

def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
    )
    return json.loads(result.stdout)


def check_ignore(clusterName,category_name,check_error):
    f = open("ignore.json")
    # returns JSON object as a dictionary
    data = json.load(f)
    f.close()
    # Iterating through the json list
    for i in data["clusters"]:
        if i["clusterName"]==clusterName and i["category_name"]==category_name and i["check_error"]==check_error:
            return False
        else:        
            return True
    
def main():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-s','--slack', help='Slack webhook', required=True)
    args = vars(parser.parse_args())
    slack_webhook = args['slack']
    
    linkerd_output = run_command("linkerd check -ojson")
    cluster_name_output = run_command("kubectl config view --minify -ojson")
    cluster = get_cluster_name(cluster_name_output)
    check_linkerd_errors(cluster, slack_webhook, linkerd_output)

if __name__ == "__main__":
    main()
