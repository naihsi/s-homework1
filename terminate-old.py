
import s_cmd
from pprint import pprint
import ngit
from datetime import datetime
from datetime import timezone

# #### ##### ##### #####


def fetch_instances():
    _data = []
    _name = "role"
    _value = "service"
    for row in s_cmd.each_ec2_bytag(_name, _value):
#        pprint(row["InstanceId"])
#        pprint(row["State"]["Name"])
#        pprint(row["Tags"])
        _branch = ""
        for one in row["Tags"]:
            if one["Key"] == "branch":
                _branch = one["Value"]

        if _branch == "":
            print("no branch tag")
            continue

        _tmp = {
            "InstanceId": row["InstanceId"],
            "state": row["State"]["Name"],
            "branch": _branch,
        }
        _data.append(_tmp)
    return _data


# #### ##### ##### #####


def main():

    # init
    terminate_seconds = 86400
    git_url = "https://github.com/naihsi/test-server.git"

    # 1. fetch information from git
    _url = git_url
    _branches = ngit.get_branch_info(_url)
    print(_branches)

    # 2. get the instances to check
    _data = fetch_instances()
    pprint(_data)

    # 3. terminate the old(3 days) instances
    _now = datetime.now(timezone.utc)
    print("utcnow: {}".format(_now))
    print("now: {}".format(datetime.now()))
    for row in _data:
        _branch = _branches[row["branch"]]
        _seconds_diff = (_now - _branch["datetime"]).total_seconds()
        print("{} - {} = {}".format(_now, _branch["datetime"], _seconds_diff))

        if _seconds_diff > terminate_seconds:
            s_cmd.terminate_inst(row["InstanceId"])
            s_cmd.wait_for("terminated", row["InstanceId"])
            print("[INFO] {} terminated due to: last commit {} is older than {} seconds in branch {}".format(row["InstanceId"], _branch["hash"], _seconds_diff, row["branch"]))


if __name__ == "__main__":
    main()
