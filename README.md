# ACP Brevet Control Times Calculator

**Author:** Milo Reynolds, miloreyn@uoregon.edu
**Course:** CIS 322, Project 4 (Flask + Ajax)

A web calculator for randonneuring (long-distance cycling) brevets. An organizer picks the brevet length and start time, then types control (checkpoint) distances into the table. The open and close time for each control fill in automatically, without a page reload, using Ajax calls to a Flask server.

It reimplements the calculator at <https://rusa.org/octime_acp.html>, following the algorithm described at <https://rusa.org/pages/acp-brevet-control-times-calculator>.

## Running it

From the `brevets` directory:

```
docker build -t brevets .
docker run -p 5000:5000 brevets
```

Then open <http://localhost:5000>. (Use the port set in `credentials.ini` if you changed it.)

### Using the page

1. Choose the brevet distance (200, 300, 400, 600 or 1000 km) and the start date and time.
2. Type a distance in either the **Miles** or the **Km** column of a row. The other column and the **Open** and **Close** times fill in on their own.
3. Changing the brevet distance or start time recalculates every filled-in row.

### Running the tests

From the `brevets` directory:

```
nosetests
```

All tests should pass. They call `acp_times.open_time` and `acp_times.close_time` directly with known inputs. The expected values were checked by hand against the examples on the RUSA page and the RUSA online calculator.

## How the times are calculated

A control's **open time** is the earliest a rider may arrive: the start time plus the time to ride the control's distance at the *maximum* speeds. Its **close time** is the latest a rider may arrive, using the *minimum* speeds. All times are computed in `brevets/acp_times.py`.

### Speed table

| Control location (km) | Minimum speed (km/h) | Maximum speed (km/h) |
|---|---|---|
| 0 - 200 | 15 | 34 |
| 200 - 400 | 15 | 32 |
| 400 - 600 | 15 | 30 |
| 600 - 1000 | 11.428 | 28 |

(The 1000 - 1300 row on the RUSA page applies only to events longer than 1000 km, so it is not used.)

### Controls spanning several rows

The speeds depend on how far along the route each *portion* of the distance is. A control is **not** computed with the single row its distance falls in. The distance is split into the part inside each speed zone, each part is divided by that zone's speed, and the results are added.

Example: a control at 350 km.

- Open: 200/34 + 150/32 = 5.88 h + 4.69 h = 10.57 h = **10H34**
- Close: 350/15 = 23.33 h = **23H20**

Example: a control at 890 km on a 1000 km brevet.

- Open: 200/34 + 200/32 + 200/30 + 290/28 = 29.156 h = **29H09**
- Close: 600/15 + 290/11.428 = 65.378 h = **65H23**

The total hours are converted to minutes and rounded to the nearest minute, then added to the brevet start time.

### Special rules

- **Controls past the brevet distance.** A control located beyond the nominal brevet distance is calculated as if it were at the brevet distance. For example, a control at 205 km on a 200 km brevet is treated as 200 km.
- **Finish control close time.** The control at the end of the brevet closes at a fixed time limit rather than the formula result:

  | Brevet | Final close time |
  |---|---|
  | 200 km | 13H30 |
  | 300 km | 20H00 |
  | 400 km | 27H00 |
  | 600 km | 40H00 |
  | 1000 km | 75H00 |

  (For example, 200/15 = 13H20, but the 200 km limit is 13H30.)
- **Controls in the first 60 km.** The close time is distance/20 + 1 hour (the 2018 relaxed rule, also called the French variation). So the start control (0 km) closes 1 hour after the start, a control at 30 km closes after 2H30, and a control at 60 km closes after 4H00, which is the same as the standard 60/15.
- **Start control.** A control at 0 km opens at the start time.
- **Distances.** Kilometer values are used as entered. Miles entered in the Miles column are converted to km (1 mile = 1.609344 km) and shown to one decimal place.

## Project layout

- `brevets/acp_times.py`: `open_time` and `close_time`, the calculation logic.
- `brevets/flask_brevets.py`: the Flask app and the `/_calc_times` Ajax route.
- `brevets/templates/calc.html`: the page and its JavaScript.
- `brevets/test_acp_times.py`: the test suite.
- `brevets/Dockerfile`: builds and runs the app.

## Credits

Initial version of the starter code by Michal Young. Modified by Milo Reynolds.
