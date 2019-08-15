API endpoints:

'/api/v1/challenge/solvepuzzle' --> POST method, in the body it gets an integer N, for the size of the matrix, and a grid
variable which is list of strings:

Example Body:

`{
	"N": 4,
	"grid": ["-p--",
			 "-x--",
			 "-m--",
			 "---x"]
}
`
in the grid variable, p is the end point, m the start point, - is a free cell and x a blocked cell

'/api/v1/challenge_log/getlogentries' --> GET method, it gets all the previous game executions in this format:

`[
{
        "error_flag": false,
        "grid": "['-p--', '-x--', '-m--', '---x']",
        "id": 19,
        "n": 4,
        "paths": "[['LEFT', 'UP', 'UP', 'RIGHT'], ['RIGHT', 'UP', 'UP', 'LEFT']]",
        "request_time": 1
}
]`