from time import perf_counter
from hx711_multi import HX711
import RPi.GPIO as GPIO

def main():

    # init GPIO (should be done outside HX711 module in case you are using other GPIO functionality)
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

    readings_to_average = 10
    sck_pin = 6
    dout_pins = [12,16, 21, 13, 19, 26]
    weight_multiples = [+1.0, +1.0, +1.0, +1.0, +1.0, +1.0]

    # create hx711 instance
    hx711 = HX711(dout_pins=dout_pins,
                sck_pin=sck_pin,
                channel_A_gain=128,
                channel_select='A',
                all_or_nothing=False,
                log_level='CRITICAL')
    # reset ADC, zero it
    hx711.reset()
    try:
        hx711.zero(readings_to_average=readings_to_average*3)
    except Exception as e:
        print(e)
    # uncomment below loop to see raw 2's complement and read integers
    # for adc in hx711._adcs:
    #     print(adc.raw_reads)  # these are the 2's complemented values read bitwise from the hx711
    #     print(adc.reads)  # these are the raw values after being converted to signed integers
    hx711.set_weight_multiples(weight_multiples=weight_multiples)

    # read until keyboard interrupt
    try:
        while True:
            start = perf_counter()

            # perform read operation, returns signed integer values as delta from zero()
            # readings aare filtered for bad data and then averaged
            raw_vals = hx711.read_raw(readings_to_average=readings_to_average)

            # request weights using multiples set previously with set_weight_multiples()
            # This function call will not perform a new measurement, it will just use what was acquired during read_raw()
            weights = hx711.get_weight()

            read_duration = perf_counter() - start
            sample_rate = readings_to_average/read_duration
            print('\nread duration: {:.3f} seconds, rate: {:.1f} Hz'.format(read_duration, sample_rate))
            print(
                'raw',
                ['{:.3f}'.format(x) if x is not None else None for x in raw_vals])
            print(' wt',
                ['{:.3f}'.format(x) if x is not None else None for x in weights])
            # uncomment below loop to see raw 2's complement and read integers
            # for adc in hx711._adcs:
            #     print(adc.raw_reads)  # these are the 2's complemented values read bitwise from the hx711
            #     print(adc.reads)  # these are the raw values after being converted to signed integers
    except KeyboardInterrupt:
        print('Keyboard interrupt..')
    except Exception as e:
        print(e)

    # cleanup GPIO
    GPIO.cleanup()


if __name__ == "__main__":
    main()
