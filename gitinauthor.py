import os
import git
import json
from pygithub3 import Github
import shutil
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def versions(path, dire, name, branch='master'):
    A=[]
    for i in range(0,5):
        if not os.path.exists(dire+name[i]):
            os.makedirs(dire+name[i])
        repo=git.Repo.clone_from(path[i],dire+name[i])
        k=0
        for commit in repo.iter_commits(branch):
            parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
            diffs  = {
                diff.a_path: diff for diff in commit.diff(parent)
            }

        # The stats on the commit is a summary of all the changes for this
        # commit, we'll iterate through it to get the information we need.
            for objpath, stats in commit.stats.files.items():

            # Select the diff for the path in the stats
                diff = diffs.get(objpath)

            # If the path is not in the dictionary, it's because it was
            # renamed, so search through the b_paths for the current name.
                if not diff:
                    for diff in diffs.values():
                        if diff.b_path == path and diff.renamed:
                            break

            # Update the stats with the additional information
                stats.update({
                    'object': os.path.join(path[i], objpath),
                    'commit': commit.hexsha,
                    'author': commit.author.email,
                    'name':commit.author.name,
                    'message':commit.message,
                    'timestamp': commit.authored_datetime.strftime(DATE_TIME_FORMAT),
                    'size': diff_size(diff),
                    'type': diff_type(diff),
                })
                A.append(stats)
    with open('data.txt', 'wb') as outfile:
        for i in A:
            json.dump(i, outfile)
            outfile.write('\n')


def diff_size(diff):
    """
    Computes the size of the diff by comparing the size of the blobs.
    """
    if diff.b_blob is None and diff.deleted_file:
        # This is a deletion, so return negative the size of the original.
        return diff.a_blob.size * -1

    if diff.a_blob is None and diff.new_file:
        # This is a new file, so return the size of the new value.
        return diff.b_blob.size

    # Otherwise just return the size a-b
    return diff.a_blob.size - diff.b_blob.size


def diff_type(diff):
    """
    Determines the type of the diff by looking at the diff flags.
    """
    #R-Remaned file, D-Deleted File, A-New file, M- No change in type.
    if diff.renamed: return 'R'
    if diff.deleted_file: return 'D'
    if diff.new_file: return 'A'
    return 'M'

hostname = '127.0.0.1'
username = 'admin'
password = '1234'
database = 'innometrics'

import time

def doQuery( conn ) :
    i=0
    cur = conn.cursor()
    cur.execute( "SELECT id FROM auth_user" )
    a=len(cur.fetchall())
    a_gid=cur.fetchall()
    time.sleep(43500)
    cur.execute( "SELECT id FROM auth_user" )
    b=len(cur.fetchall())
    ids=[]
    if b>a:
        for gid in cur.fetchall() :
            if gid not in a_gid:
                ids.append(gid)
    a=b
    a_gid=cur.fetchall()
    return ids
		
print "Using psycopg2"
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
i=0
while i==0:
    A=doQuery(myConnection)
    print "done"
    g = Github(login="HRishabh95", password=.......)
    for name in A:
        a=g.repos.list(user = name).all()
        na=[]
        C=[]
        for i in a:
            na.append(i.name)
            C.append(i.git_url)
        versions(C, "C:/Rishabh/Masters Thesis/Github/",na)
myConnection.close()


