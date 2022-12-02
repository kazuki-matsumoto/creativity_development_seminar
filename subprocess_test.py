import subprocess

def julius_subprocess():
  julius      = "dictation-kit-v4.3.1-linux/julius"
  main        = "dictation-kit-v4.3.1-linux/main.jconf"
  am_gmm      = "dictation-kit-v4.3.1-linux/am-dnn.jconf" 
  
  
  args = [julius, "-C", main, "-C", am_gmm, "-module", "charconv", "utf-8", "sjis"]
  
  p = subprocess.run(args)

julius_subprocess()