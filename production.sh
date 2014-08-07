aws s3 cp project.html s3://kickstarter.spokepoint.com/ --grants read=uri="http://acs.amazonaws.com/groups/global/AllUsers"
aws s3 sync css/ s3://kickstarter.spokepoint.com/ --grants read=uri="http://acs.amazonaws.com/groups/global/AllUsers"
aws s3 sync Charts/ s3://kickstarter.spokepoint.com/ --grants read=uri="http://acs.amazonaws.com/groups/global/AllUsers"