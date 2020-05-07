from solarTracker.ota import OTAUpdater

def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/OperationAzura/solarTracker')
    o.check_for_update_to_install_during_next_reboot()
    o.download_and_install_update_if_available('YOUR SSID', 'YOUR PASSWORD')

def start():
    import solarTracker.solarTrackerMain as stm
    stm.run()
    # your custom code goes here. Something like this: ...
    # from main.x import YourProject
    # project = YourProject()
    # ...


def boot():
    download_and_install_update_if_available()
    start()

boot()