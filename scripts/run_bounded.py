#!/usr/bin/env python3
"""Supervise a single-process Python transform on macOS/Linux. No GUI or workers."""
from pathlib import Path
import argparse, json, math, os, resource, runpy, signal, subprocess, sys, tempfile, time


def stop(process):
    if process.poll() is None:
        try:os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:pass
    process.wait(timeout=3)


def supervise(command,rss_mib=192,seconds=20):
    started=time.monotonic();peak=0;reason=None
    with tempfile.TemporaryFile() as log:
        p=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
        try:
            while p.poll() is None:
                if time.monotonic()-started>seconds:reason='wall_time';stop(p);break
                sample=subprocess.run(['/bin/ps','-o','rss=','-p',str(p.pid)],capture_output=True,text=True,timeout=1)
                if sample.stdout.strip():
                    rss=int(sample.stdout.strip())*1024;peak=max(peak,rss)
                    if rss>rss_mib*1024**2:reason='rss';stop(p);break
                time.sleep(.02)
            p.wait(timeout=3)
        except BaseException:
            stop(p);raise
        log.seek(0);raw=log.read(16385)
    return {'returncode':p.returncode,'stop_reason':reason,'sampled_peak_rss_bytes':peak,
            'wall_seconds':round(time.monotonic()-started,3),'output':raw[:16384].decode(errors='replace'),
            'output_truncated':len(raw)>16384}


def limit(kind,value):
    _,hard=resource.getrlimit(kind)
    if hard!=resource.RLIM_INFINITY:value=min(value,hard)
    resource.setrlimit(kind,(value,value))


def worker(args):
    limit(resource.RLIMIT_CPU,max(1,math.ceil(args.seconds)))
    limit(resource.RLIMIT_FSIZE,int(args.file_mib*1024**2))
    limit(resource.RLIMIT_CORE,0)
    script=Path(args.script[0]).resolve()
    sys.argv=[str(script),*args.script[1:]]
    sys.path.insert(0,str(script.parent))
    try:runpy.run_path(str(script),run_name='__main__')
    finally:
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform!='darwin':rss*=1024
        print(json.dumps({'worker_peak_rss_bytes':rss}),flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rss-mib',type=float,default=192);p.add_argument('--seconds',type=float,default=20)
    p.add_argument('--file-mib',type=float,default=8);p.add_argument('--worker',action='store_true',help=argparse.SUPPRESS)
    p.add_argument('script',nargs=argparse.REMAINDER)
    args=p.parse_args()
    if args.script and args.script[0]=='--':args.script=args.script[1:]
    if not args.script or not Path(args.script[0]).is_file():p.error('Provide an existing Python script after --')
    if not all(math.isfinite(v) and v>0 for v in (args.rss_mib,args.seconds,args.file_mib)):p.error('Limits must be positive and finite')
    if args.worker:worker(args);return
    command=[sys.executable,str(Path(__file__).resolve()),'--worker','--seconds',str(args.seconds),
             '--file-mib',str(args.file_mib),'--',*args.script]
    # SIGTERM to the supervisor must also clean up the supervised process.
    def terminate(signum,frame):raise KeyboardInterrupt('Supervisor terminated')
    signal.signal(signal.SIGTERM,terminate)
    result=supervise(command,args.rss_mib,args.seconds)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result['returncode'] or result['stop_reason']:raise SystemExit(1)

if __name__=='__main__':main()
