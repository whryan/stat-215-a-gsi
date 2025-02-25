import shutil
import subprocess
import os
import tempfile
import argparse
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

gsi_dir = "/accounts/campus/omer_ronen/Documents/215a/stat-215-a-gsi"
git_at = open(os.path.join(gsi_dir, "215a", ".git_at")).readlines()[0]


def _get_args():
    parser = argparse.ArgumentParser(description='Testing 215A labs')
    parser.add_argument('lab_number', type=int, help='lab number to test')

    args = parser.parse_args()
    return args


def _get_repos():
    return [r.split("\n")[0] for r in open(os.path.join(gsi_dir, "data/repos"), "r").readlines()]


def _get_data_path(lab_number):
    return os.path.join(gsi_dir, f"lab{lab_number}", "data")


def _get_test_script(lab_number):
    return os.path.join(gsi_dir, f"lab{lab_number}", "test.sh")


def clone_repo(git_user, local_directory):
    cmd = f"git clone https://OmerRonen:{git_at}@github.com/{git_user}/stat-215-a.git  {local_directory}"
    LOGGER.info(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    # if err:
    #     raise OSError('The process raised an error:', err.decode())


def test_lab(git_user, lab_number):
    d = os.path.join("/accounts/campus/omer_ronen/Documents/215a", git_user)
    LOGGER.info(f"Testing {git_user}")
    clone_repo(git_user, d)
    LOGGER.info(f"files are {os.listdir(d)}")
    shutil.copyfile(_get_test_script(lab_number), os.path.join(d, "test.sh"))
    shutil.copytree(_get_data_path(lab_number), os.path.join(d, "data"))
    subprocess.Popen(f"bash test.sh", cwd=d, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.isfile(os.path.join(d, "md_log.txt")):
        LOGGER.warning(f"{git_user} failed the test!!!")


def main():
    args = _get_args()
    lab_number = args.lab_number
    repos = _get_repos()
    for student in repos:
        test_lab(student, lab_number)


if __name__ == '__main__':
    main()
