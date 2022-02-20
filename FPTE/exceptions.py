"""custom exceptions
"""

class FolderNotClean(FileExistsError):
    def __init__(self, _folder):
        msg = f"""\n Folder {_folder} exists. You need to clean your folder,
        before running any additioanl calculations. \n
        -> You can do it with `FPTE --clean` in this folder.
        """
        super().__init__(msg)

