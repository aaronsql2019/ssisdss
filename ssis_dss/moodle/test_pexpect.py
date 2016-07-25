from ssis_dss.moodle.php import PHP

if __name__ == "__main__":
    p = PHP()
    here=""
    while here.strip() != "quit":
        here = input()
        p.command(here.strip(), '')
