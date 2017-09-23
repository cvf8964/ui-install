from ui_bundle import UIBundle
from file_stream import FileStream


class UIBundleInstaller:
    cached_installed = FileStream('library/installed.json')
    cached_repository = FileStream('library/repository.json')

    @classmethod
    def install(cls, bundle_list: list):
        installed = cls.cached_installed.to_set()
        repository = cls.cached_repository.to_set()
        # backing up new bundles
        for bundle_name in bundle_list:
            if bundle_name in repository:
                bundle_object = UIBundle(bundle_name)
                if bundle_name not in installed:
                    bundle_object.backup()
                bundle_object.install()
                installed.add(bundle_name)
        cls.cached_installed.overwrite(installed)
        cls.list_installed()

    @classmethod
    def uninstall(cls, bundle_list: list):
        installed = cls.cached_installed.to_set()
        for bundle_name in bundle_list:
            if bundle_name in installed:
                bundle_object = UIBundle(bundle_name)
                bundle_object.restore()  # install the backup to restore
                installed.remove(bundle_name)
        cls.cached_installed.overwrite(installed)
        cls.list_installed()

    @classmethod
    def list_installed(cls):
        installed = cls.cached_installed.to_set()
        if len(installed) > 0:
            print('\n Installed: {}'.format(', '.join(installed)))

    @classmethod
    def list_repository(cls):
        repository = cls.cached_repository.to_set()
        if len(repository) > 0:
            print('\n Repository: {}'.format(', '.join(repository)))

    @classmethod
    def run_command(cls, command: str, params):
        cmd = getattr(UIBundleInstaller, command)

        if len(params) > 0:
            cmd(params)
        else:
            cmd()
