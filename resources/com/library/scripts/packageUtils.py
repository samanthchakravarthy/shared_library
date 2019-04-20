import os
import zipfile
import sys



def main(**kwargs):
    snapshotfilename = kwargs['artifactName']
    dirnames = kwargs['folderName']

    snapshot_tar(snapshotfilename, dirnames)

def snapshot(snapshotfilename, dirnames):
  dirnames = dirnames.split(",")
  for dirname in dirnames:
    snapshot_tar(snapshotfilename, dirname)
  #manifestfile = 'manifest.txt'
  #snapshot_tar(snapshotfilename, manifestfile)

def snapshot_tar(snapshotfilename, dirname):
  zipobj = zipfile.ZipFile(snapshotfilename + '.zip', 'a', zipfile.ZIP_DEFLATED)
  for base, dirs, files in os.walk(dirname):
    for file in files:
      zipobj.write(os.path.join(base, file))
  if dirname.endswith('.txt'):
    zipobj.write(dirname)

if __name__ == '__main__':
    params = dict(arg.split('=') for arg in sys.argv[1:])
    main(**params)
