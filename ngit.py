
import tempfile
from git import Repo
from datetime import datetime

# #### ##### ##### #####


def get_branch_info(url):
    _git = url
    with tempfile.TemporaryDirectory() as dname:
        repo = Repo.init(dname)
        repo.create_remote("origin", _git)
        repo.git.fetch()
        remote_branches = []
        for row in repo.git.branch('-r').splitlines():
            _branch_name = row.strip().replace("origin/", "")
            _last = last_commit(repo, _branch_name)
            _tmp = {
                "branchname": _branch_name,
                "lastcommid": _last,
            }
            remote_branches.append(_tmp)
        return remote_branches


def last_commit(repo, branch_name):
    _logs = repo.git.log("origin/{}".format(branch_name)).splitlines()
    if len(_logs) < 3:
        return {}

    _last = {
        "hash": _logs[0][7:],
        # Wed MAy 29 22:08:45 2019 +0000
        "datetime": datetime.strptime(_logs[2][8:], '%a %b %d %H:%M:%S %Y %z'),
    }
    return _last

# #### ##### ##### #####


def test():
    print("> get_branch_info")
    _url = "https://github.com/naihsi/test-server.git"
    _branches = get_branch_info(_url)
    print(_branches)


if __name__ == "__main__":
    test()
