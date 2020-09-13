import os

path = os.getcwd()

def check_dir(path):
    dir_name = os.path.basename(os.path.normpath(path))
    if os.path.isdir(path):
        # print("Directory {} already exists.".format(dir_name))
        return None

    else:
        # print("Directory {} dose not exists.".format(dir_name))
        return dir_name

def creat_directory(path):
        temp = check_dir(path)
        if temp is None:
            pass

        else:
            dir_name = temp
            try:
                os.mkdir(path)

            except OSError:
                print("Creation of the directory %s failed." % dir_name)

            else:
                print("Successfully created the directory %s." % dir_name)
