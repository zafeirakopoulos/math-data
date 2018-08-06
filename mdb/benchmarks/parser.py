import argparse
import psutil
import os
import shutil
import hashlib
import json
import subprocess
from multiprocessing import Process, Pipe
from sys import stdout, stdin


# Copied from myexception.py ###################################################
class RequiredFieldException(Exception):
    def __init__(self, filepath, field):
        super().__init__('File "{}" does not have field "{}"'.format(filepath, field))
        self.filepath = filepath
        self.field1 = field
        pass

    pass


class SelectionalFieldException(Exception):
    def __init__(self, filepath, field1, field2):
        super().__init__('File "{}" does not have field "{}" or "{}"'.format(filepath, field1, field2))
        self.filepath = filepath
        self.field1 = field1
        self.field2 = field2
        pass

    def __reduce__(self):
        return SelectionalFieldException, (self.filepath, self.field1, self.field2)
        pass

    pass
################################################################################

################################################################################
import os
import sys
from contextlib import contextmanager


def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd


@contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    if stdout is None:
        stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    # NOTE: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout  # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            # NOTE: dup2 makes stdout_fd inheritable unconditionally
            stdout.flush()
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied


#################################################################################


class DataSet:
    data_sets = {}

    def _run_dataset(self):
        for i in self.data:
            print(json.dumps(i))
            pass
        pass

    def _run_generator(self):
        subprocess.run([self.generator['executable'], *self.generator['parameters']])
        pass

    def __init__(self, filepath):
        DataSet.data_sets[os.path.basename(filepath)] = self

        with open(filepath, "r") as f:
            json_form = json.load(f)
            pass

        if 'data' in json_form:
            self.run = self._run_dataset
            self.data = json_form['data']
            pass
        elif 'generator' in json_form:
            self.run = self._run_generator
            self.generator = json_form['generator']
            pass
        else:
            raise SelectionalFieldException(filepath, "datas", "generator")
            pass
        pass

    pass


class Program:
    programs = {}

    def __init__(self, filepath):
        with open(filepath, "r") as f:
            json_form = json.load(f)
            pass

        if 'name' in json_form:
            self.name = json_form['name']
            pass
        else:
            raise RequiredFieldException(filepath, 'name')
            pass

        if 'version' in json_form:
            self.version = json_form['version']
            pass
        else:
            raise RequiredFieldException(filepath, 'version')
            pass

        if 'parameters' in json_form:
            self.parameters = json_form['parameters']
            pass
        else:
            raise RequiredFieldException(filepath, 'parameters')
            pass

        if 'executable' in json_form:
            self.executable = json_form['executable']
            pass
        else:
            raise RequiredFieldException(filepath, 'executable')
            pass

        if 'tests' in json_form:
            for test in json_form['tests']:
                if test['op'] == 'exists':
                    if shutil.which(test['value'], mode=os.F_OK) is None:
                        raise FileNotFoundError(test['value'])
                pass
            pass

        proghash = hashlib.sha256()
        proghash.update(self.name.encode())
        for ver in self.version:
            proghash.update(ver.encode())
            pass
        Program.programs[proghash.hexdigest()] = self
        pass

    def __str__(self):
        return str(
            {"name": self.name, "version": self.version, "parameters": self.parameters, "executor": self.executor})

    pass


class Method:
    methods = {}

    def __init__(self, filepath):
        with open(filepath, "r") as f:
            json_form = json.load(f)
            pass

        if 'title' in json_form:
            self.title = json_form['title']
            pass
        else:
            raise RequiredFieldException(filepath, 'title')
            pass

        if 'description' in json_form:
            self.description = json_form['description']
            pass

        if 'program' in json_form:
            proghash = hashlib.sha256()
            proghash.update(json_form['program']['name'].encode())
            for ver in json_form['program']['version']:
                proghash.update(ver.encode())
                pass
            self.program = Program.programs[proghash.hexdigest()]
            del proghash
            pass

        if 'parameters' in json_form:
            self.parameters = []
            for parameter in self.program.parameters:
                if parameter['name'] in json_form['parameters']:
                    if parameter['flag'] is not None:
                        self.parameters.append(parameter['flag'])
                    self.parameters.append(json_form['parameters'][parameter['name']])
                    pass
                elif parameter['required']:
                    raise RequiredFieldException(filepath, "parameters." + parameter['name'])
                    pass
                pass
            pass

        if 'input' in json_form:
            self.input = json_form['input']
            pass
        else:
            raise RequiredFieldException(filepath, "input")
            pass

        Method.methods[os.path.basename(filepath)] = self
        pass

    def run(self):
        ip = subprocess.Popen(self.input, stdout=subprocess.PIPE)
        proc = subprocess.Popen(
            [self.program.executable['name'], *self.program.executable['parameters'], *self.parameters],
            stdin=ip.stdout)

        ip.wait()
        proc.wait()
        pass

    def __str__(self):
        return str(
            {'title': self.title, 'description': self.description, 'program': self.program,
             'parameters': self.parameters, 'input': self.input})

    pass


def runtime_analysis(method: type(Method), outfile):
    p = psutil.Popen([method.program.executable['name'], *method.program.executable['parameters'],
                      *method.parameters])

    os.close(fileno(sys.stdout))
    os.close(fileno(sys.stdin))

    import datetime

    with open(outfile, "w") as f:
        while p.is_running() and p.status() != psutil.STATUS_ZOMBIE:
            print(datetime.datetime.now(), p.cpu_times, p.cpu_percent(0.1), *zip(["rss", "vms", "shared", "text", "lib", "data", "dirty"], p.memory_info()), file=f)

    p.wait()
    pass


# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("benchmarkfile")
    parser.add_argument("programsfolder")
    parser.add_argument("datasetsfolder")
    parser.add_argument("methodsfolder")

    args = parser.parse_args()

    h, t = os.path.split(args.benchmarkfile)
    args.programsfolder = os.path.join(h, args.programsfolder)
    args.datasetsfolder = os.path.join(h, args.datasetsfolder)
    args.methodsfolder = os.path.join(h, args.methodsfolder)

    for progconfig in os.listdir(args.programsfolder):
        try:
            filename, extension = os.path.splitext(progconfig)
            filepath = os.path.abspath(os.path.join(args.programsfolder, progconfig))
            if extension == '.json':
                Program(filepath)
                pass
            pass
        except (RequiredFieldException, SelectionalFieldException) as err:
            # silently ignore this for now
            pass
        pass

    for datasetconfig in os.listdir(args.datasetsfolder):
        try:
            filename, extension = os.path.splitext(datasetconfig)
            filepath = os.path.abspath(os.path.join(args.datasetsfolder, datasetconfig))
            if extension == '.json':
                DataSet(filepath)
                pass
            pass
        except (RequiredFieldException, SelectionalFieldException) as err:
            # silently ignore this for now
            pass
        pass

    for methodconfig in os.listdir(args.methodsfolder):
        try:
            filename, extension = os.path.splitext(methodconfig)
            filepath = os.path.abspath(os.path.join(args.methodsfolder, methodconfig))
            if extension == '.json':
                Method(filepath)
            pass
        except (RequiredFieldException, SelectionalFieldException) as err:
            # silently ignore this for now
            pass

    with open(args.benchmarkfile, "r") as f:
        benchmarkfile = json.load(f)
        pass

    datasets = []
    methods = []
    benchmarks = []

    for d in benchmarkfile['data-sets']:
        datasets.append(DataSet.data_sets[d])
        pass

    for m in benchmarkfile['methods']:
        methods.append(Method.methods[m])
        pass

    for b in benchmarkfile['benchmarks']:
        benchmark = {'data-sets': [], 'methods': [], 'tries': b['tries'], 'analysis': b['analysis']}

        for d in b['data-sets']:
            benchmark['data-sets'].append(datasets[d])
            pass

        for m in b['methods']:
            benchmark['methods'].append(methods[m])
            pass
        benchmarks.append(benchmark)
        pass

    for benchmark in benchmarks:
        for di, dataset in enumerate(benchmark['data-sets']):
            for mi, method in enumerate(benchmark['methods']):
                for i in range(benchmark['tries']):
                    pr0, pw0 = os.pipe()  # dataset - input provider
                    pr1, pw1 = os.pipe()  # input provider - input analyzer
                    pr2, pw2 = os.pipe()  # input analyzer - run-time analyzer(executable)
                    pr3, pw3 = os.pipe()  # run-time analyzer(executable) - output analyzer

                    procs = []

                    inlog = os.path.join(os.path.abspath("inlogs"), str(mi) + "_" + str(di) + "_" + str(i) + ".log")
                    outlog = os.path.join(os.path.abspath("outlogs"), str(mi) + "_" + str(di) + "_" + str(i) + ".log")
                    runlog = os.path.join(os.path.abspath("runlogs"), str(mi) + "_" + str(di) + "_" + str(i) + ".log")

                    # RUN DATASET
                    with stdout_redirected(pw0, stdout=sys.stdout):
                        os.close(pw0)
                        dproc = Process(target=dataset.run)
                        dproc.start()

                    # RUN INPUT PROVIDER
                    with stdout_redirected(pr0, stdout=sys.stdin):
                        os.close(pr0)
                        with stdout_redirected(pw1, stdout=sys.stdout):
                            os.close(pw1)
                            iproc = subprocess.Popen(method.input)

                    # RUN INPUT ANALYSIS
                    with stdout_redirected(pr1, stdout=sys.stdin):
                        os.close(pr1)
                        with stdout_redirected(pw2, stdout=sys.stdout):
                            os.close(pw2)
                            iaproc = subprocess.Popen([*benchmark['analysis'][0]['input'][:2], inlog, *benchmark['analysis'][0]['input'][2:]])

                    # RUN RUN-TIME ANALYSIS
                    with stdout_redirected(pr2, stdout=sys.stdin):
                        os.close(pr2)
                        with stdout_redirected(pw3, stdout=sys.stdout):
                            os.close(pw3)
                            rproc = Process(target=runtime_analysis, args=(method, runlog))
                            rproc.start()

                    # RUN OUTPUT ANALYSIS
                    with stdout_redirected(pr3, stdout=sys.stdin):
                        os.close(pr3)
                        oaproc = subprocess.Popen([*benchmark['analysis'][0]['output'][:2], outlog, *benchmark['analysis'][0]['output'][2:]])

                    dproc.join()
                    iproc.wait()
                    iaproc.wait()
                    rproc.join()
                    oaproc.wait()
                    print((di * len(benchmark['methods']) * benchmark['tries'] + mi * benchmark['tries'] + i) / (len(benchmark['data-sets']) * len(benchmark['methods']) * benchmark['tries']) * 100, flush=True)
                    pass
                pass
            pass
        pass
    pass

# methods requires a specific version of a program
# programs define fetching/building/running a specific version of a program
