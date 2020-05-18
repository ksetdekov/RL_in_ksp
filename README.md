# RL_in_ksp

1) Install requirements:<br />
`pipenv install`

2) Add project src folder to PYTHONPATH:<br />
`export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"`

3) 
- Start no ML no PID simulation: <br />
`python src/engineering_approach/no_pid.py` 
Telemetry plots are saved in `src/engineering_approach/plots`

- Start no ML simulation with PID used for rcs:<br />
`python src/engineering_approach/rcs_pid.py` 

- Generate random train data for rewards:<br />
`python src/RL/generate_train.py` 