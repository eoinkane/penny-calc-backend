# __Penny-Calc Backend__

This project helps a user complete the 1p saving challenges:

* The 1p Savings Challenge
[*more info*](https://monzo.com/blog/1p-savings-challenge-2020 'link')  
* The Reverse 1p Savings Challenge
[*more info*](https://monzo.com/blog/2019/06/04/reverse-1p-savings-challenge-monzo 'link')

__This project has 2 sections:__  

* __Backend Code__
* __Infrastructure as Code (CDK)__

## __Backend Code__

The logic code is written in python and stored in `./app`

### __List of Scripts__

* __`calculate/full_amount`__

    This lambda calculates how many days till next payday then returns that quantity multiplied by 3.66 (the daily saving amount)  
    The file is `app/src/calculate/full_amount/app.py`  
    The entrypoint is `lambda_handler`

## __Infrastructure as Code (CDK)__

The CDK is written in TypeScript  

This project has been built using AWS CDK version __1.61.1__  
The cdk cli tool requires aws credentials.  
I use an AWS educate account [more info](https://aws.amazon.com/education/awseducate/students/ 'link')  
But any account that has these credentials: *aws_access_key_id*; *aws_secret_access_key*; *aws_session_token*; will do

If you have not used CDK in your AWS account before please run `cdk bootstrap` before starting

### __Components__

The CDK includes 2 components

* __API Gateway__
* __Lambda Function__

### __Lambda Function__

The Serverless function allows us to call our Scripts

#### __List of Lambdas__  

* __`penny-calc-full-amount-lambda`__  
    This lambda runs the `calculate/full_amount` script  

### __API Gateway__

The API Gateway provides access to the backend through Rest API calls.  

#### __Endpoints__

* __`/next-date/calculate/full-amount`__
    This endpoint is a GET method endpoint  
    Using an AWS_PROXY lamdba integration  
    This endpoint links up to `penny-calc-full-amount-lambda` lambda

## __Comands__

It is reccommended to install the packages required  
*run these commands to get started*  
`PIPENV_VENV_IN_PROJECT=1 pipenv install --dev`  
`PIPENV_VENV_IN_PROJECT=1 pipenv install`  
`npm install`

A number of the commands rely on the cdk cli and so please have a valid session/token from AWS

### __List of Comands__

* __`npm run build`__
    Runs the following commands

  * `build-python`
  * `build-cdk`

* __`npm run build-python`__  
    This command builds the python code with the packages installed
* __`npm run build-cdk`__  
    This command builds the CDK stack
* __`npm run cdk-synth`__  
    This command builds a cloudformation template from the CDK stack
* __`npm run cdk-diff`__  
    This command shows the difference between the latest template and the previous one
* __`npm run cdk-deploy`__  
    This command deploys the cloudformation stack  
    *Prequisite: `ckd-synth`*
* __`npm run cdk-deploy-ci`__  
    Follows the same behaviour as `cdk-deploy` but does not ask for confirmation  
    *Prequisite: `ckd-synth`*
* __`npm run test-cdk`__  
    Tests the CDK stack
    *Refer to the Testing Section*
* __`npm run test-python`__  
    Tests the Python scripts
    *Refer to the Testing Section*
* __`npm run tsc`__  
    Runs the typescript complier
* __`npm run clean`__  
    Runs the following commands

  * `clean-tests`
  * `clean-build`
  * `clean-cdk`

* __`npm run clean-tests`__  
    Removes temporary test files
* __`npm run clean-build`__  
    Removes temporary build files
* __`npm run clean-cdk`__  
    Removes temporary cdk files
* __`npm run run-lambda-local`__  
    Runs the lambda locally

## __Testing__

There are tests for both the cdk stack and backend code  

* __CDK tests__
    __`npm run test-cdk`__
    Written in TypeScript and using jest as the test runner
* __Python tests__
    __`npm run test-python`__
    Written in python and using pytest as the test runner


## Welcome to your CDK TypeScript project

This is a blank project for TypeScript development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
