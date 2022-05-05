# Aridac
final project for CMU 15-712

How to run:
1. Obtain root access before running any code.
3. Launch containers, check provided shell scripts under /src and /environment, and you can also refer to Project/environment/README.md.
4. Run "python3 Project/src/stats.py N", replace N with the number of stats data you want to use for your policy. Recommanded value: 30.

Tools:
1. You can use Project/src/limiter.py to check/update the current quota for given containers. Run "python3 Project/src/limiter.py --help" for usage.
2. You can use Project/src/install_docker.sh to install and setup proxy on PDL Narwhal Bare Metal Machine.
