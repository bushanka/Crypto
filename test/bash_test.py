if __name__ == "__main__":
    import subprocess
    s = subprocess.getstatusoutput(f'ps -ef | grep python3')
    print(s[1])
