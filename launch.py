
import s_cmd
from pprint import pprint
import ngit
import argparse

# #### ##### ##### #####


def info(msg):
    print("[INFO] {}".format(msg))


def arg_parse():
    parser = argparse.ArgumentParser(description='deploy from branch')
    parser.add_argument('-b', metavar="master", help='branch name to deploy', required=True)
    args = parser.parse_args()
#    print(args)
    return args

# #### ##### ##### #####


def main():

    # init
    git_url = "https://github.com/naihsi/test-server.git"

    # arg parse
    _branch_name = arg_parse().b

    # 1. fetch information from git
    _url = git_url
    _branches = ngit.get_branch_info(_url)

    if _branch_name not in _branches:
        info("[INFO] branch {} not in the git".format(_branch_name))
        return

    if s_cmd.pass_dryrun(s_cmd.create_inst, (_branch_name, True)):
        _inst_id = s_cmd.create_inst(_branch_name)
        s_cmd.wait_for("running", _inst_id)
        info("[INFO] {} was launched for branch {}".format(_inst_id, _branch_name))


if __name__ == "__main__":
    main()
