# Table of Contents

* [Overview](#overview)
* [Installation](#installation)
* [License](#license)
* [Troubleshooting](#troubleshooting)

# Overview
Welcome to my repository torqueutils! This repository just contains a collection of code that is used by the [ICDS i-ASK center](https://www.icds.psu.edu/) on torque to retrieve information about users jobs on the Roar supercomputer. The tools have various usages, so I will describe them below:

* **getusersjobids:** Retrieve users job ids for processing and analyzation.
* **getjobinfo:** Query information about a job or multiple jobs.

# Installation
In order to install the torqueutils collection, simply use the following commands below:

```bash
$ module load anaconda3/2020.07
$ conda create --prefix /storage/work/dml129/sw7/python python=3.9
$ ssh torque01.util.production.int.aci.ics.psu.edu
$ export PATH=/storage/work/dml129/sw7/python/bin:$PATH
$ cd /storage/work/dml129/sw7
$ git clone https://github.com/NucciTheBoss/torqueutils.git
$ cd torqueutils
$ pip install -r requirements.txt
$ pip install pyinstaller
$ pyinstaller getusersjobids.py
$ cd /storage/work/dml129
$ ln -s /storage/work/dml129/sw7/torqueutils/dist/getusersjobids/getusersjobids /storage/work/dml129/getusersjobids
```

If all goes well, you should be able to run the following command in your terminal:

```
$ ./getusersjobids --help
Usage: getusersjobids [OPTIONS]

Options:
  -u, --user TEXT     User to query (example: jcn23).
  -d, --days INTEGER  Specify the number of days to check in the torque job
                      logs (default: 5).

  --xml               Print job ids in XML format.
  --json              Print job ids in JSON format.
  --yaml              Print job ids in YAML format.
  --csv               Print job ids in CSV format.
  --table             Print job ids in tabular format.
  -V, --version       Print version info.
  --license           Print licensing info.
  --help              Show this message and exit.
```

Congratulations! If you received the above output, you have successfully installed the torqueutils collection! Now have fun helping users with their research needs!

# License

![GitHub](https://img.shields.io/github/license/NucciTheBoss/torqueutils)

This repository is licensed under the GNU General Public License v3.0. 
For more information on what this license entails, please feel free to 
visit https://www.gnu.org/licenses/gpl-3.0.en.html.

# Troubleshooting
If you encounter any issues while using this utility on the Roar cluster then please open an issue, or contact Jason at the ICDS i-ASK center at either iask@ics.psu.edu or jcn23@psu.edu.
