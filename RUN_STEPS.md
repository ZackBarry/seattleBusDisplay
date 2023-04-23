
Hardware setup:
https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard/wiki

Software setup:
https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard#software-installation

Disable sound card:
https://www.instructables.com/Disable-the-Built-in-Sound-Card-of-Raspberry-Pi/

Test matrix: 
https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices



```
cd /etc/modprobe.d
sudo vi alsa-blacklist.conf
## add text: `blacklist snd_bcm2835`
## then save and run next line
sudo reboot
```

```
cd seattleBusDisplay
python
> from metro.context import download_context
> download_context()
pip install -r requirements.txt
sudo python3 test.py --led-gpio-mapping="adafruit-hat"

curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh
## Bonnet, option 2 (no sound, no soldering)

sudo vi /boot/config.txt
# comment out arm_boost=1
sudo reboot

vi ~/.bashrc
# insert the following
BUS_ARGS="--led-gpio-mapping=adafruit-hat --led-cols=64 --led-rows=32 --led-slowdown-gpio=4 --led-limit-refresh-hz=60 --led-brightness=65"
source ~/.bashrc

sudo python run.py $BUS_ARGS
```


To test
```
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh
cd rpi-rgp-led-matrix/examples-api-use
sudo ./demo D0 --led-rows=32 --led-cols=64 --led-limit-refresh-rate=60 --led-slowdown-gpio=4
```

Test python scripts:
https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python/samples
