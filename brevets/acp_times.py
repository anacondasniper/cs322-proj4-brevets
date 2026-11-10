"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    control = min(control_dist_km, brevet_dist_km)
    start = arrow.get(brevet_start_time)
    if control <= 200:
        hours = control / 34
    elif control <= 400:
        hours = 200/34 + (control - 200)/32
    elif control <= 600:
        hours = 200/34 + 200/32 + (control - 400)/30
    else:
        hours = 200/34 + 200/32 + 200/30 + (control - 600)/28
    minutes = round(hours * 60)
    return start.shift(minutes=minutes).isoformat()

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    control = min(control_dist_km, brevet_dist_km)
    start = arrow.get(brevet_start_time)
    if control < 60:
        hours = control / 20 + 1
    elif control <= 200:
        hours = control / 15
    elif control <= 400:
        hours =  200/15 + (control - 200)/15
    elif control <= 600:
        hours = 200/15 + 200/15 + (control - 400)/15
    else:
        hours = 200/15 + 200/15 + 200/15 + (control - 600)/11.428
    minutes = round(hours * 60)
    return start.shift(minutes=minutes).isoformat()
