#### Title
Building a Completely Serverless Ecosystem with AWS Lambda and Chalice

#### Duration
25 minutes

#### Audience Level
Intermediate

#### Abstract
Reduce costs and server administration overhead by using on-demand compute
resources, pre-wired HTTP endpoints, and an AWS-built batteries-included web
framework. AWS Lambda, API Gateway, and Chalice are a winning combination for
hassle-free high-velocity development.

#### Description
In a cloud-first infrastructure, if you're paying for a traditional server and
not using 100% of the allocated resources, you're wasting money. AWS Lambda and
API Gateway are on-demand compute services where you only pay for what you
use. These products allow us to design applications without worrying about
maintaining expensive, always-running, and vulnerable servers.

This talk will explain the basics of serverless infrastructure and go over the
main high-level advantages such as reduced cost and no server administration
overhead.

We will then introduce Chalice, a web framework built by AWS Labs, go through
examples of designing a full-featured HTTP API, and deploy it... LIVE!

#### Notes

 * My [personal website](http://becker.am/talks)
 * I own/run [ismytrainfucked](http://ismytrainfucked.com), and decided to leave
   the profanity uncensored in the proposal for transparency reasons. But it can
   certainly be censored for the conference.
 * My only technical requirement is reliable Wifi for a live demo of an application
   deployment and `curl` commands.

I have given a few talks about small python applications and local NYC meetups;
the Amazon Alexa Meetup and Hack && Tell NYC. Two years ago, at PyGotham, I
co-presented a talk about basic Python containerization approaches on the three
most popular cloud platforms (at the time: Google Container Engine, Microsoft
Azure, AWS ECS).

Hack && Tell NYC-
[agenda](https://github.com/hackandtell/wrapup/blob/master/nyc/round-38-wrapup.md#chris-becker---is-my-train-fucked),
[slides](http://becker.am/talks/is_my_train_fucked.pdf)
 
NYC Alexa Meetup presentation-
[agenda](https://www.meetup.com/NYC-Amazon-Alexa-Meetup/events/232256046/),
[slides](http://becker.am/talks/dishwasher_alexa_meetup.pdf)
 
PyGotham 2015-
[agenda](https://2015.pygotham.org/talks/163/docker-containers-in-the/),
[video](https://www.youtube.com/watch?v=yT2H-H39284)

#### Tags
serverless, aws, lambda, web, framework, api

#### Outline
  * Intro (1min)
    * about me
    * what I do at work
  * Basics of Serverless Infrastructure (5min)
    * AWS Lambda - event-driven, serverless computing platform provided by
      Amazon. You can run small event-driven applications without maintaining a
      traditional computer (EC2) instance.
      * By themselves, Lambdas can respond to internal AWS Events (e.g. S3
        uploads or SQS queues) or be run on a recurring schedule (think cron)
        * Silly twitter bots?
    * AWS API Gateway - hosted service that wires HTTP requests to Lambda function(s)
      * This lets you expose lambda invocations to the WWW, via a RESTful interface
  * Advantages (3min)
    * Price
      * 1st million invocations free (seriously)
    * No server administration overhead
    * "Point-and-Click" interface, or an incredibly robust API
  * Introduce ismytrainfucked.com (3min)
    * Architecture
      * Lambda on recurring schedule (cron) writes HTML file to S3
      * Stores historical data in DynamoDB
      * Running for over a year, total cost <$5
    * I wanted to make an app... need an API!
      * API built with API Gateway and a fleet of lambdas
      * Managing/deploying multiple files was annoying
      * Lambda functions accumulate some extra cruft
        * You have to declare HTTP codes in your response, etc.
        
```
return {
    "statusCode": 200,
    'headers': {"Content-Type": "application/json"},
    "body": json.dumps(response_payload),
}
```

*... enter Chalice ...*

  * [Chalice](https://github.com/awslabs/chalice) ties it all together (12min)
    * A python serverless microframework for AWS allows you to quickly create
      and deploy applications that use Amazon API Gateway and AWS Lambda.
    * Main features:
      * command line tool for creating, deploying, and managing your app
      * familiar and easy to use API for declaring views in python code
  * Structure of a Chalice project
  
Start a new project
    
```
$ chalice new-project api
$ ls
total 16
-rw-r--r--  1 chris  staff   1.5K Jul 17 11:48 app.py
-rw-r--r--  1 chris  staff    13B Jul 17 11:48 requirements.txt
```

Set up the naming schema for the app and supporting resources (e.g. IAM
policies, API, etc):
    
```
app = Chalice(app_name='cool-amazing-api')
```

URL routes are Python functions with decorators;
    
```
@app.route('/')
def index():
    return {"message": "Hello, 
```

Framework looks identical to [flask](http://flask.pocoo.org/):
    
```
@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    return {"value": value}
```

Deployment is simple:
    
```
$ chalice deploy
...
...
https://ksdf93kdf9.execute-api.us-east-1.amazonaws.com/dev
```

Writing the ismytrainfucked API - less than 20 lines!
    
```
def _get_latest_train_status():
    print('"{"message": "Fetching latest status from dynamodb"')

    query_response = table.query(
        KeyConditionExpression=Key('date').eq(
            datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"))
        & Key('time').lte(decimal.Decimal(time.time())),
        ScanIndexForward=False,
        Limit=1,
    )
    statuses = query_response.get('Items')[0].get('data')
    return {x[0]: {'is_fucked': x[2], 'status': x[1]} for x in statuses}

@app.route('/latest')
def latest():
    latest_train_status = _get_latest_train_status()
    response = json.dumps({'data': latest_train_status})
    return response
```

Testing our API locally:

```
$ chalice local
$ curl localhost:8000
```

Deploy and test to our development environment!
    
```
$ chalice deploy
...
...
$ curl https://ksdf93kdf9.execute-api.us-east-1.amazonaws.com/dev/latest
{"data":
    {"123": 
        {"is_fucked": "YUP", "status": "SERVICE CHANGE"}
...
...
}
```

  * Further Reading (1min)
    * Google Cloud Functions
    * Managing Serverless Functions and Apps
      * [Apex](https://github.com/apex/apex)
      * [Serverless](https://github.com/serverless/serverless)
      * [Zappa](https://github.com/Miserlou/Zappa)
    
