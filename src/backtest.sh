for i in $(seq 0 1 1000)
do
        d=`date --date now-${i}day  +%Y%m%d`
        echo $d
        mkdir -p log
	python3 RoboMain.py -dt $d | sort -n -r | tee log/robo-$d.cmd
done
