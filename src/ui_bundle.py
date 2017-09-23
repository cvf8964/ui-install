import os
import shutil
from file_stream import FileStream


path = os.path
library_dir = path.join(path.dirname(path.abspath(__file__)), 'library')


class UIBundle:
    def __init__(self, bundle_name):
        self.installation_dict = FileStream(path.join('library', bundle_name, 'install.json')).to_dict()
        self.bundle_name = bundle_name

    def install_paths(self, node, base_dir) -> (str, str):
        for key in node:
            if isinstance(node[key], dict):
                yield from self.install_paths(node[key], path.join(base_dir, key))
            else:
                yield base_dir, node[key]

    def install(self):
        source_dir = path.join(library_dir, self.bundle_name)
        base_install_dir = path.expanduser(path.join(self.installation_dict['ApplicationPath'], 'Contents'))
        for install_dir, file_name in self.install_paths(self.installation_dict['Contents'], base_install_dir):
            self.install_source_file(source_dir, install_dir, file_name)

    def backup(self):
        base_source_dir = path.expanduser(path.join(self.installation_dict['ApplicationPath'], 'Contents'))
        install_dir = path.join(library_dir, 'backup', self.bundle_name)
        if not path.exists(install_dir):
            os.mkdir(install_dir)
        for source_dir, file_name in self.install_paths(self.installation_dict['Contents'], base_source_dir):
            self.install_source_file(source_dir, install_dir, file_name)

    def restore(self):
        pass

    @staticmethod
    def install_source_file(source_dir, install_dir, file_name):
        destination = path.join(install_dir, file_name)
        source_file = path.join(source_dir, file_name)

        stats = os.stat(destination)
        uid, gid = stats.st_uid, stats.st_gid
        if path.exists(destination):
            os.remove(destination)
        shutil.copy2(source_file, install_dir)
        os.chown(destination, uid, gid)

    # @staticmethod
    # def install_source_file(source_dir, install_dir, file_name):
    #     destination = path.join(install_dir, file_name)
    #     source_file = path.join(source_dir, file_name)
    #     if path.exists(destination):
    #         print('Removing file {}'.format(destination))
    #     print('Copying from \n{} to \n{}'.format(source_file, destination))
