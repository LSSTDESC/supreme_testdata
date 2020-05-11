#!/usr/bin/env python

import argparse

import numpy as np
import astropy.io.fits as fits

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Zero-out an exposure for space savings.')

    parser.add_argument('-f', '--filename', action='store', type=str, required=True,
                        help='File to zero out')
    parser.add_argument('-i', '--imagevalue', action='store', type=float, required=False,
                        default=0.0, help='Value to set image to.')
    parser.add_argument('-v', '--variancevalue', action='store', type=float, required=False,
                        default=0.0, help='Value to set variance to.')

    args = parser.parse_args()

    data = fits.open(args.filename)

    for hdu in data:
        try:
            exttype = hdu.header['EXTTYPE']
        except:
            continue

        if hdu.data is None:
            continue

        if exttype == 'IMAGE':
            print('Overwriting image with value = %.5f' % (args.imagevalue))
            hdu.data[:] = args.imagevalue
        elif exttype == 'VARIANCE':
            if args.variancevalue > 0.0:
                print('Overwriting variance with value = %.5f' % (args.variancevalue))
                hdu.data[:] = args.variancevalue
            else:
                var = np.median(hdu.data[:])
                print('Overwriting variance with value = %.5f' % (var))
                hdu.data[:] = var

    data.writeto(args.filename, overwrite=True)
