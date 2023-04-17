# !/bin/sh
# pollutant
cd /opt/AirHongKong
source venv/bin/activate
which python3
python3 -m sg.fetch
# weather visibility
source venv38/bin/activate
python3 -m sg.observation