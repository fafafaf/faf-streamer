export DISPLAY=:0
export WINEDEBUG=-all 
python ~/faf/src/main.py $(pwd)/$1 &>/dev/null
