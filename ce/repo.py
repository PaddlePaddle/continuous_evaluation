from ce.utils import __


def clone(repo_url, local_path):
    '''
    Git clone a repo to a local path.
    :param repo_url: str
    :param local_path: str
    :return: None
    '''
    __('git clone {url} {local}'.format(
        url=repo_url,
        local=local_path, ))
