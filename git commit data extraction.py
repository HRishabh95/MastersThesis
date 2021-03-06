import os
import git
import json

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def versions(path, dire, branch='master'):
    A=[]
    repo=git.Repo.clone_from(path,dire)
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
                'object': os.path.join(path, objpath),
                'commit': commit.hexsha,
                'name':commit.author.name,
                'message':commit.message,
                'author': commit.author.email,
                'timestamp': commit.authored_datetime.strftime(DATE_TIME_FORMAT),
                'size': diff_size(diff),
                #'type': diff_type(diff),
            })
            A.append(stats)
    with open('data.txt', 'wb') as outfile:
        for i in A:
            json.dump(i, outfile)
            outfile.write('\n')



versions("Project Link", "Directory")

# Project Link and Directory for saving the commits.
