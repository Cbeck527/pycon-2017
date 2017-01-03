#### Title
Weaving Together Python and Systems Administration with Fabric

#### Duration
30 minutes

#### Description
Fabric is a Python framework and CLI tool for writing scripts to make deployment
or systems administration tasks easy and fun! It allows us to ditch complicated
bash scripts, and allow us to work in the language we know best— Python. We'll
cover the basic structure, and slowly build up to writing a task that interacts
with an entire fleet of servers.

#### Who and Why (Audience)
This talked is geared towards intermediate programmers who are comfortable with
python— (modules, functions, context managers, decorators) and interested in
learning about automating basic systems administration tasks. After watching the
talk, the audience will leave with a grasp on writing fabric scripts that can
help speed up repetitive systems administration tasks that they do often. The
audience will also leave with ideas of more advanced projects relating to
dynamic cloud infrastructure, and how fabric fits into the cloud computing
puzzle.

#### Outline
  * Intro
    * about me
    * what I do at work
  * Introduction to Fabric
    * python library for automation
    * imperative programming paradigm (opposite of `ansible`)
    * fabric is organized around tasks
    * tasks are executed via the CLI
    
      ` $ fab TASK_NAME`
  * Writing Your First Task
    * tasks are just python functions
    
      ```
      def hello():
          print("Hello world!")
      ```
    * running your task
    
      `$ fab hello`
  * Taking Arguments
    * modify original hello world function
    
      ```
      def hello(name="world"):
        print("Hello {}!".format(name))
      ```
    * passing arguments in the CLI
    
      ```
      $ fab hello:name=Chris
      Hello, Chris!
      
      Done.
      ```
    * passing multiple arguments
    
      `$ fab hello_multiple:one=Chris,two=Jeff`
    * arguments with spaces
    
      `$ fab hello_multiple:one="Chris Becker",two=Jeff`
  * Doing Some "Real Work" with `run()`
    * getting the kernel information for our servers
      * `run('uname -a')`
    * specify host with CLI
      * `$ fab uname -H SERVER_HOST_OR_IP`
  * Capturing Output
    * variables can store the output of run() functions
    * passing in `capture=True` to the `local()` function behaves similarly
    * _"run `uname -a` on my servers and write the info to a file"_
    
    ```
    from fabric import api
    
    def uname():
        with open('info.txt', 'a') as f:
            output = api.run('uname -a')
            f.write(output)
    ```
    
  * Using `sudo`
    * write a program to `apt-get update && apt-get upgrade`
      * function to `apt-get update`
        * `api.sudo()`
      * function to `apt-get upgrade`
      * chain together tasks with `api.execute(TASK_NAME)`
  * Uploading Files
    * `api.put()`
  * Fabric Environment Dictionary
    * most of fabric’s behavior is controllable by modifying env variables,
      such as `env.colorize_errors`
    * `env.gateway` for using an SSH bastion host
  * Constructing a List of Hosts
    * easiest: `$ fab -H HOST_STRING task`
    * hard-code into fabfile by setting the `env` dictionary:
      `env.hosts = ['host1', 'host2']`
    * you can even set hosts on a a per-task basis:

      ```
      @hosts('user@host1', 'user@host2')
      def my_task():
      ...
      ```
    * group hosts together with roles: `env.roledefs = {'db': ['db1', 'db2']}`.
      roles are a convenient way to refer to multiple servers.
    * the act on roles in a similar way to hosts
    
      ```
      @roles('db')
      def my_task():
      ...
      ```
  * Advanced Topics to Explore
    * Template files with Python and `fabric.contrib.files.upload_template`
    * combining with other libraries (`boto`)
      * _"look up my EC2 instances with this tag and execute this function"_
    * piggy-backing off anisble inventory (yay python!)
    * improving the cli (with `click`)

#### Additional Notes
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

My personal website- http://becker.am/talks

At Warby Parker, I'm a one-person team that manages all of our development
tooling based on fabric. We utilize the `fabric` and `boto` libraries to create and
provision new cloud instances in our infrastructure. 

