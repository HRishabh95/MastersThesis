import git
#url=git://github.com/olivergierke/repositories-deepdive.git
def commit_message(url,di, n)
    repo=git.Repo.clone_from(url,di)
    heads = repo.heads
    master = heads.master
    committs = list(repo.iter_commits('master', max_count=n))
    f=open("Commit.txt",'w')
    for i in committs:
        f.write(i.message.encode("latin1", 'ignore').replace("\n"," ")+"\n")
    f.close()

commit_message("git://github.com/olivergierke/repositories-deepdive.git", "C:/Rishabh/Masters Thesis/Github/xx",100)

