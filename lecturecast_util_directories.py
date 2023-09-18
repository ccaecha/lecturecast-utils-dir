import os, pwd, grp
import lecturecast_util_directories_owner as dir_owner

base_path = "/usr/local/bin/lecturecast"
subdirectory_paths = ["util/apps", "util/logs"]

def makeDirWithRights(path, owner, group, rights):
    if not os.path.exists(path):
        try:
            os.mkdir(path, mode = rights)
            os.path.exists(path)
            try :
                uid = pwd.getpwnam(owner).pw_uid
                gid = grp.getgrnam(group).gr_gid

                stat_info = os.stat(path)
                stat_uid = stat_info.st_uid
                stat_gid = stat_info.st_gid

                if stat_uid != uid or stat_gid != gid:
                    os.chown(path, uid, gid)
                return True
            except KeyError as exp:
                print(f"Error: Unable to set owner({uid})/group({gid}) to directory {path} :: {str(exp)}")
                return False
        except OSError as exp:
            print(f"Error: Unable to create directory {path} :: {str(exp)}")
            return False
    return False

def getParentsAndSelfPaths(path):
    allparts = []
    paths = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    for i in range(len(allparts)):
        joinparts = ""
        for j in range(i+1):
            joinparts = os.path.join(joinparts, allparts[j])
        paths.append(joinparts)
    return paths


if makeDirWithRights(base_path):
    for sd_path in subdirectory_paths:
        sd_path = os.path.normpath(sd_path)
        sd_combinations = getParentsAndSelfPaths(sd_path)
        for sd_c in sd_combinations:
            if not makeDirWithRights(os.path.join(base_path, sd_c)):
                break
