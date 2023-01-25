# Example Usage of TinyTuya
import tinytuya

blinds_id = "50548253e8db8490af85"
blinds_ip = "10.0.0.2"
blinds_local_key = "ba907edeb0fb6bc6"

d = tinytuya.OutletDevice(blinds_id, blinds_ip, blinds_local_key)
d.set_version(3.3)
data = d.status()
d2 = d.detect_available_dps()


print('Device status: %r' % data)
print('Device DPS: %r' % d2)


# d.set_value(1, 'open', False)
# {'1': 'open', '2': 81,   '3': 0  , '5': True, '7': 'opening', '8': 'cancel', '9': 0, '10': 0, '11': 44025}

# d.set_value(1, 'close', False)
# {'1': 'close', '2': 81,  '3': 100, '5': True, '7': 'closing', '8': 'cancel', '9': 0, '10': 0, '11': 44025}

# d.set_value(2, 50, True)
# {'1': 'close', '2': 50,  '3': 50,  '5': True, '7': 'opening', '8': 'cancel', '9': 0, '10': 0, '11': 44025}

# d.set_value(2, 0, False)
# {'1': 'close', '2': 0,   '3': 0,   '5': True, '7': 'opening', '8': 'cancel', '9': 0, '10': 0, '11': 44025}

# d.set_value(2, 100, False)
# {'1': 'close', '2': 100, '3': 100, '5': True, '7': 'closing', '8': 'cancel', '9': 0, '10': 0, '11': 44025}


# DPID	    DP description	            Standard command
# 1	        Curtain switch 1	        Yes
# 2	        Percentage 1	            Yes
# 3	        Accurate calibration 1	    No
# ########################################################### 4	        Curtain switch 2	        Yes
# 5	        Percentage 2	            Yes
# ########################################################### 6	        Accurate calibration 2	    No
# 7	        Backlight switch	        No
# 8	        Motor rotation direction 1	No
# 9	        Motor rotation direction 2	No
# 10	    Quick calibration 1	        No
# 11	    Quick calibration 2	        No
# ########################################################### 14	    Indicator status	        No
