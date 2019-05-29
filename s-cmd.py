
import boto3
from pprint import pprint

# #### ##### ##### #####


def ec2():
    client = boto3.client('ec2', region_name='us-west-2')
    return client


def list_inst():
    _filters = []
    _res = ec2().describe_instances(Filters=_filters)

    pprint(_res)


# #### ##### ##### #####


def test():
    print("init")
    list_inst()


if __name__ == "__main__":
    test()
