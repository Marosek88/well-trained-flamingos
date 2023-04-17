import * as cdk from 'aws-cdk-lib';
import { LambdaRestApi } from 'aws-cdk-lib/aws-apigateway';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';


export class WtfJokeApi extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // define s3 bucket for storing jokes
    const bucket = new Bucket(this, 'joke-bucket', {
      bucketName: 'wtf-joke-bucket-dev'
    });

    // define lambda function that gets jokes and stores them in s3 bucket
    const handler = new Function(this, 'joke-api-handler', {
      functionName: 'wtf-joke-api-handler-dev',
      runtime: Runtime.PYTHON_3_9,
      code: Code.fromAsset('lambda-functions/joke-api'),
      handler: "joke_api_handler.lambda_handler",
      environment: {
        BUCKET: bucket.bucketName
      }
    });

    // allow lambda function to read from and store to the s3 bucket
    bucket.grantReadWrite(handler)

    // define API gateway that will 
    const api = new LambdaRestApi(this, 'joke-api', {
      handler: handler,
      proxy: false
    });

    // define API endpoints
    const jokes = api.root.addResource('jokes');
    jokes.addMethod('GET');  // GET /jokes
    jokes.addMethod('POST'); // POST /jokes

    const joke_details = jokes.addResource('{joke_id}');
    joke_details.addMethod('GET');   // GET /jokes/{joke_id}
    
  }
}
