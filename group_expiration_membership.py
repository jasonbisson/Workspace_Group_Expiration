import datetime 
import argparse
import googleapiclient.discovery

def get_arguments():
  parser = argparse.ArgumentParser()
  parser = argparse.ArgumentParser(description='Google Group Membership expiration arguments.')
  parser.add_argument("--group_id", help="The email address of Google Group.", required=True)
  parser.add_argument("--member_key", help="The email address of the Google user.", required=True)
  parser.add_argument("--hours", type=int, help="Hours until expiration of Group membership.", default=8)
  args = parser.parse_args()
  return (args)

def expiration_time(hours):
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    expire_time = now + datetime.timedelta(hours=hours)
    required_date_format = expire_time.isoformat().replace("+00:00", "Z")
    return (required_date_format)

def create_google_group_membership(service, group_id, member_key, required_date_format):
  param = "&groupKey.id=" + group_id
  try:
    lookupGroupNameRequest = service.groups().lookup()
    lookupGroupNameRequest.uri += param
    lookupGroupNameResponse = lookupGroupNameRequest.execute()
    groupName = lookupGroupNameResponse.get("name")
    # Create a membership object with a memberKey and a single role of type MEMBER
    membership = {
      "preferredMemberKey": {"id": member_key},
      "roles" : {
        "name" : "MEMBER",
        "expiryDetail": {
          "expireTime": required_date_format
        }
      }
    }
    response = service.groups().memberships().create(parent=groupName, body=membership).execute()
    print(response)
  except Exception as e:
    print(e)


def main():
    args = get_arguments()
    service = googleapiclient.discovery.build('cloudidentity', 'v1')
    required_date_format=expiration_time(args.hours)
    create_google_group_membership(service, args.group_id, args.member_key, required_date_format)
if __name__ == '__main__':
    main()