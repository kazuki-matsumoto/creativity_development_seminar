import subprocess
from subprocess import PIPE
 
julius      = "dictation-kit-v4.3.1/julius"
main        = "dictation-kit-v4.3.1/main.jconf"
am_gmm      = "dictation-kit-v4.3.1/am-dnn.jconf" 
 
 
args = [julius, "-C", main, "-C", am_gmm, "-demo", "-charconv", "utf-8", "sjis"]
 
p = subprocess.run(args, stdout=PIPE, text=True)
print(p.stdout)