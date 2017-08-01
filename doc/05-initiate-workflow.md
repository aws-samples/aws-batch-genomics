## Initiate a workflow

Modify the file `workflow/test.input.json` to direct to the appropriate paths in your own account.

Next, execute the following CLI command:
```bash
aws stepfunctions start-execution --state-machine-arn <your-arn> --input file://workflow/test.input.json
```

You can then navigate to the AWS Step Functions console to monitor your workflow's progress.
![Step Functions workflow Progress](https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2017/06/02/stepfunctions_midworkflow.png)
