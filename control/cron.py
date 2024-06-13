from crontab import CronTab

PATH = "~/development/dildoproject/update.py"

def add_cron_job(t, tf):
    cron = CronTab(user='dx')
    job = cron.new(command=f"python3 -B {PATH} -p bybit -t {t} -tf {tf} -a 192.168.0.163:6379")

    if tf.startswith('M'):
        if len(tf) > 1:
            job.minute.every(int(tf[1:]))
        else:
            job.minute.every(1)
    elif tf.startswith('H'):
        job.hour.every(int(tf[1:]))
    elif tf.startswith('D'):
        job.day.every(1)
    elif tf.startswith('W'):
        job.dow.on('SUN')

    cron.write()

def remove_cron_job(ticker, timeframe):
    cron = CronTab(user='dx')
    jobs = cron.find_command(f"python3 -B {PATH} -p bybit -t {ticker} -tf {timeframe} -a 192.168.0.163:6379")
    for job in jobs:
        cron.remove(job)
    cron.write()

def is_cron_job_exists(ticker, timeframe):
    cron = CronTab(user='dx')
    jobs = cron.find_command(f"python3 -B {PATH} -p bybit -t {ticker} -tf {timeframe} -a 192.168.0.163:6379")
    return any(True for _ in jobs)

def manage_cron_jobs(state, all_tfs):
    for tik in state:
        for tf in all_tfs:
            if tf in state[tik]['recv_tf']:
                if not is_cron_job_exists(tik, tf):
                    add_cron_job(tik, tf)
            else:
                if is_cron_job_exists(tik, tf):
                    remove_cron_job(tik, tf)

