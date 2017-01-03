from fabric import api


@api.task
def uname():
    api.run('uname -a')
