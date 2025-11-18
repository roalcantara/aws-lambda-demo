<!-- markdownlint-disable -->
# aws-lambda-demo

This [demo][9] demonstrates a simple AWS SAM app

[![MIT license](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=flat-square)](LICENSE) [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg?style=flat-square)][2] [![Editor Config](https://img.shields.io/badge/Editor%20Config-1.0.1-crimson.svg?style=flat-square)][3] [![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)][4] [![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?logo=conventional-commits&style=flat-square)][9]

## INSTALL

```sh
git clone https://github.com/roalcantara/aws-lambda-demo
```

### DEPENDENCIES

- [Git][5]
- [Mise][6]
  - [AWS SAM CLI][13]
- [Pre-Commit][7]
- [Gitlint][8]
- [Docker Desktop][14]

#### RECOMMENDATIONS

> 💡 AWS Toolkit is an open source plug-in for popular IDEs
>
> - It uses the AWS SAM CLI to build, deploy and debug serverless apps

- [CLion][10]
- [GoLand][10]
- [IntelliJ][10]
- [WebStorm][10]
- [Rider][10]
- [PhpStorm][10]
- [PyCharm][10]
- [RubyMine][10]
- [DataGrip][10]
- [VS Code][11]
- [Visual Studio][12]

## OVERVIEW

- This demo demonstrates how to:
  - Define AWS resources in a [SAM template file](template.yaml)
  - Deploy Lambda functions
  - Deploy API Gateway REST APIs automatically created based on the Lambda function's Event mapping.

### STRUCTURE

  ```tree
  ├── README.md
  ├── events
  │   └── event.json                       # Invocation event to invoke the function
  ├── example-pattern.json
  ├── hello_world                          # Code for the Lambda function
  │   ├── __init__.py
  │   ├── app.py
  │   └── requirements.txt
  ├── mise.toml
  ├── samconfig.toml                       # Configuration file for the AWS SAM CLI
  └── template.yaml                        # File that defining the application
  ```

## USAGE

### 0. SETUP

Install all dependencies

```bash
mise install
```

### 1. BUILDING

To build and deploy your application for the first time, run:

  ```bash
  # build the source of your application.
  sam build --use-container

  # package and deploy your application to AWS, with a series of prompts
  sam deploy --guided
  ```

- **Stack Name**:
  The name of the stack to deploy to CloudFormation.
  This should be unique to your account and region, and a good starting point would be something matching your project name.
- **AWS Region**:
  The AWS region you want to deploy your app to.
- **Confirm changes before deploy**:
  If yes, any change sets will be shown to you before execution for manual review.
  If no, the AWS SAM CLI will automatically deploy application changes.
- **HelloWorldFunction has no authentication. Is this okay? `[y/N]`:**:
  - Select `y` for the purposes of this sample application.
    As a result, anyone will be able to call this example REST API without any form of authentication.
  - If `N` is selected for this question, this deployment will not succeed.
- **Allow AWS SAM CLI IAM role creation**:
  - Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services.
  - By default, these are scoped down to minimum required permissions.
  - To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided.
  - If permission isn't provided through this prompt, to deploy this example pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
- **Save arguments to samconfig.toml**:
  - Set `yes`, to save your choices to a configuration file inside the project.

> **NOTE:** For production applications
>   - enable authentication for the [API Gateway][15] using one of several available options
>   - follow the [API Gateway][15] [best practices][16].

For future deploys, you can run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway endpoint URL in the output values displayed after deployment.

### 2. TESTING and INVOKING LOCALLY

- The AWS SAM CLI:
  - Installs dependencies defined in `hello_world/package.json`
  - Creates a deployment package
  - Saves it in the `.aws-sam/build` folder.
- You can test a single function by invoking it directly with a test event.
- An event is a JSON document that represents the input that the function receives from the event source.
- Test events are included in the `events` folder in this project.
- Run functions locally and invoke them with command:

  ```bash
  sam local invoke HelloWorldFunction --event events/event.json
  ```

### 3. EMULATING API GATEWAY REST LOCALLY

1. Given a template file containing:

  ```yaml
  Resources:
    HelloWorldFunction:
      Type: AWS::Serverless::Function
      Properties:
        Handler: hello_world.app.lambda_handler
        Runtime: python3.8
        Events:
          HelloWorld:
            Type: Api
            Properties:
              Path: /hello
              Method: get

2. When you want to serve the API locally on port 3000, run:

  ```bash
  #!/bin/sh

  # start the API locally on port 3000
  sam local start-api
  ```

4. Then AWS SAM CLI reads the template file to:
   - Determine API`s routes
   - Determine functions they invoke
   - Determine the routes and methods for each function's path defined in the `Events` property
   - Serve the API locally on port 3000.

5. And check if the API is running

  ```bash
  curl http://localhost:3000/hello
  ```

### 4. DEPLOYING to REMOTE

1. Given that you have already built your application

2. When deploying your application to AWS, run:

    ```bash
    sam deploy
    # alternatively
    sam deploy --guided
    ```

  - When the app is packaged as `.zip`
    Then it compacts the files and uploads them to an Amazon S3 bucket.
    And the bucket is created if necessary.

  - When the app is packaged as `container`
    Then the image is uploaded to Amazon ECR.
    And the repository is created if necessary.

3. Then an AWS CloudFormation change set is created
   And the app is deployed as a stack.

4. And the SAM template is updated
   And the new CodeUri value for your Lambda functions is set.

5. And the API Gateway endpoint URL of your application is displayed.

### 5. INVOKING REMOTELY

- After the app has been deployed, invoke functions remotely by running:

  ```bash
  sam remote invoke HelloWorldFunction --event-file events/event.json
  ```

- Alternatively, go to the API Gateway endpoint URL outputed after the app deployment
  Which will similarly invoke your deployed Lambda function.

### 6. FETCH, TAIL, AND FILTERING [LOGS][17]

> 💡 Fetch logs several nifty features of Lambda functions from the command line

  ```sh
  sam logs

  # To fetch logs generated by your deployed Lambda function from the command line run
  sam logs -n HelloWorldFunction --stack-name "YOUR_STACK_NAME_HERE" --tail
  ```

> `NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using AWS SAM.

### 7. CLEANUP

> 💡 To delete apps using AWS CLI.

  ```bash
  # If the project name for the stack name was used during deployment:
  sam delete

  # Otherwise, specify your stack name:
  sam delete --stack-name YOUR_STACK_NAME_HERE
  ```

## ACKNOWLEDGEMENTS

- [Standard Readme][4]
- [Conventional Commits][9]
- [Serverless application concepts][20]
- [AWS SAM developer guide][18]
- [AWS SAM CLI][19]
- [Invoking Lambda functions with API Gateway][21]
- [Amazon API Gateway REST API][22]

## CONTRIBUTING

- Bug reports and pull requests are welcome on [GitHub][0]
- Do follow [Editor Config][3] rules.
- Everyone interacting in the project's codebases, issue trackers, chat rooms and mailing lists is expected to follow the [Contributor Covenant][2] code of conduct.

## LICENSE

The project is available as open source under the terms of the [MIT][1] [License](LICENSE)

[0]: https://github.com/roalcantara/aws-lambda-demo 'Yet another app'
[1]: https://opensource.org/licenses/MIT 'Open Source Initiative'
[2]: https://contributor-covenant.org 'A Code of Conduct for Open Source Communities'
[3]: https://editorconfig.org 'EditorConfig'
[4]: https://github.com/RichardLitt/standard-readme 'Standard Readme'
[5]: https://git-scm.com 'Distributed version control system'
[6]: https://mise.jdx.dev 'Manages dev tools like node, python, cmake, terraform, and hundreds more'
[7]: https://pre-commit.com 'Framework for managing and maintaining multi-language pre-commit hooks'
[8]: https://jorisroovers.com/gitlint 'Git commit message linter'
[9]: https://conventionalcommits.org 'Conventional Commits'
[10]: https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html 'AWS Toolkit for JetBrains - Welcome'
[11]: https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html 'AWS Toolkit for VS Code - Welcome'
[12]: https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html 'AWS Toolkit for Visual Studio - Welcome'
[13]: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html 'AWS SAM CLI install guide'
[14]: https://hub.docker.com/search/?type=edition&offering=community 'Docker Desktop'
[15]: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html 'API Gateway access control'
[16]: https://docs.aws.amazon.com/apigateway/latest/developerguide/security-best-practices.html 'API Gateway security best practices'
[17]: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html 'AWS SAM CLI logging'
[18]: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html 'What is AWS SAM?'
[19]: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html 'Getting started with AWS SAM Hello World'
[20]: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-concepts.html 'Serverless application concepts'
[21]: https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html 'Invoking Lambda functions with API Gateway'
[22]: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-rest-api.html 'Amazon API Gateway REST API'
