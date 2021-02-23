import click
from rich.console import Console
from rich.table import Table
import subprocess
import random
import os
from xml.dom import minidom
import json
import yaml
import csv


class dataFactory:
    def __init__(self, data):
        self.data = data
        self.console = Console()

    def toXML(self):
        pass

    def toJSON(self):
        pass

    def toYAML(self):
        pass

    def toCSV(self):
        pass

    def toTABLE(self):
        pass


def subprocess_cmd(command):
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    return process.stdout.strip("\n")


def findJobID(job_id, job_log_dir, log_dir):
    """Function to test if job id exists in the job_log directory on torque."""
    # Execute test command
    cat_exec = subprocess.Popen(["cat", "{}/{}".format(job_log_dir, log_dir)], stdout=subprocess.PIPE)
    grep_exec = subprocess.run(["grep", job_id], stdin=cat_exec.stdout, capture_output=True, text=True)
    cat_exec.stdout.close()

    # Verify if job id exists
    grep_exec.stdout.strip("\n").strip(" ")
    if grep_exec.stdout != "":
        return True

    else:
        return False


def retrieveJobInfo(job_id, days, output_file):
    """Retrieve the XML job info stored in the job_log directory on torque."""
     # Retreive past couple of job log directories
    job_log_dir = "/var/spool/torque/job_logs"
    job_logs = subprocess.Popen(["ls", job_log_dir, "-t"], stdout=subprocess.PIPE)
    logs = subprocess.run(["head", "-n", days], stdin=job_logs.stdout, capture_output=True, text=True)
    job_logs.stdout.close()

    # Convert logs.stdout to a list and remove any blank lines
    logs_list = logs.stdout.split("\n")
    logs_list.remove("")

    # Loop through job log to find job info
    found_job_id = False
    for log in logs_list:
        if findJobID(job_id, job_log_dir, log):
            # Get line 1 using commands in the shell
            line_1 = subprocess_cmd("cat {}/{} | grep -n {} | head -n 1 | cut -d: -f1".format(job_log_dir, log, job_id))

            # Get line 0 using commands in the shell
            line_0 = subprocess_cmd("head -n {} {}/{} | grep -n <Jobinfo> | tail -n1 | cut -d: -f1".format(line_1, job_log_dir, log))

            # Get line 3 using commands in the shell
            line_3 = subprocess_cmd("tail -n +{} {}/{} | grep -n </Jobinfo> | head -n 1 | cut -d: -f1".format(line_0, job_log_dir, log))

            # Reevaluate line 3
            line_3 = subprocess_cmd("expr {} + {}".format(line_3, line_0))

            # Get final output and write to temp file
            final_output = subprocess_cmd("sed -n {},{}p {}/{}".format(line_0, line_3, job_log_dir, log))
            output_file.write(final_output)
            found_job_id = True
            break

    if found_job_id is False:
        console = Console()
        console.print("[bold red]{} not found.[/bold red]".format(job_id))


@click.command()
@click.argument("jobid", nargs=-1)
@click.option("-f", "--file", default=None, help="Read job ids to query from an XML file instead.")
@click.option("-d", "--days", default=5, help="Specify the number of days to check in the torque job logs (default: 5).")
@click.option("--xml", is_flag=True, help="Print job info in XML format.")
@click.option("--json", is_flag=True, help="Print job info in JSON format.")
@click.option("--yaml", is_flag=True, help="Print job info in YAML format.")
@click.option("--csv", is_flag=True, help="Print job info in CSV format.")
@click.option("--table", is_flag=True, help="Print job info in tabular format.")
@click.option("-V", "--version", is_flag=True, help="Print version info.")
@click.option("--license", is_flag=True, help="Print licensing info.")
def main(jobid, file, days, xml, json, yaml, csv, table, version, license):
    if version:
        click.echo("getjobinfo v2.0  Copyright (C) 2021  Jason C. Nucciarone \n\n"
                   "This program comes with ABSOLUTELY NO WARRANTY; \n"
                   "for more details type \"getjobinfo --license\". This is free software, \n"
                   "and you are welcome to redistribute it under certain conditions; \n"
                   "go to https://www.gnu.org/licenses/licenses.html for more details.")
        return

    elif license:
        click.echo("""getjobinfo: Retrieve users job ids for processing and analyzation.\n
    Copyright (C) 2021  Jason C. Nucciarone

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.""")
        return

    else:
        console = Console()
        # Check if user specified any job ids
        if len(jobid) == 0:
            console.print("[bold red]No job ids specified![/bold red]")
            console.print("Enter [bold blue]getjobinfo --help[/bold blue] for help.")
            return

        elif len(jobid) == 1:
            temp = "/tmp/{}_get_job_info.xml".format(random.randint(1, 1000000))
            fout = open(temp, "at")
            retrieveJobInfo(str(jobid[0]), str(days), fout)
            fout.close()
            fin = open(temp, "rt")
            xml = fin.read()
            fin.close()
            print(xml)
            return

        else:
            print("Multiple!")
            return


if __name__ == "__main__":
    main()
