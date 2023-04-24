# linkerdchecker
This script is designed to check for errors in a Linkerd service mesh and notify Slack channels of any relevant errors that are not ignored by the user. The script requires a Slack webhook and a locally installed Linkerd CLI as prerequisites.

To use the script, run it from the command line with the Slack webhook specified as a command line argument using the -s or --slack option.

The script reads the Linkerd check output in JSON format using the linkerd check -ojson command and the name of the cluster using the kubectl config view --minify -ojson command. It then checks for errors in the output and filters out any ignored errors specified in an ignore.json file. Finally, it sends a notification to the Slack webhook for any relevant errors that are not ignored.

To ignore specific errors, add them to the ignore.json file in the following format:

```
{
    "clusters": [
        {
            "clusterName": "<name of the cluster>",
            "category_name": "<name of the error category>",
            "check_error": "<error message>"
        },
        ...
    ]
}
```

Note that the clusterName and category_name values are case-sensitive and must match the output of the kubectl config view --minify -ojson and linkerd check -ojson commands, respectively.

Logging output is set to the INFO level by default, but can be adjusted by modifying the logging.basicConfig call.

To create the binary file for this script, you can use the provided Makefile.
The Makefile contains two targets:
* `clean`: This target removes the dist directory where the binary will be created. You can run it with the following command:

```
make clean
```
* `build`: This target creates a binary file in the dist directory using the PyInstaller package. You can run it with the following command:
```
make build
```

After running the build target, you will find the binary file in the dist directory. You can run it using the following command:
```
.dist/main/main -s $SLACK_WEBHOOK
```
