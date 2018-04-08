from tqdm import tqdm
import k2plr
from glob import glob
from astropy.io import fits
from astropy.visualization import ZScaleInterval
import matplotlib.pyplot as pl
import os
import sys

def get_ra_dec(epicnum,verbose=False):
    client = k2plr.API()
    if verbose:
        print('\nquerying RA and DEC...\n')
    epic = client.k2_star(int(epicnum))
    ra = epic.k2_ra
    dec = epic.k2_dec
    return ra, dec


def get_fnames(foldername):
    file_list=glob(foldername+'/*.fits')
    file_list.sort()
    return file_list


def get_data(fname):
    if len(fname)==0:
        print('File does not exist!\n')
        sys.exit()
    elif os.path.exists(fname):
        try:
            hdulist=fits.open(fname)
            img=hdulist[0].data
            hdr=hdulist[0].header
        except Excetion as e:
            print(e)
    else:
        print('File does not exist!\n')
        sys.exit()
    return img, hdr


def sort_filternames(xlist):
    '''sort into grizy'''
    d = {}
    for i in xlist:
        ii = i.split('_')[2]
        if ii =='g':
            d[1] = i
        elif ii=='r':
            d[2] = i
        elif ii=='i':
            d[3] = i
        elif ii=='z':
            d[4] = i
        else:
            d[5] = i
    return d


def parse_kwargs(kwargs):
    if kwargs is not None:
        textloc=kwargs['textloc']
        fontsize=kwargs['fontsize']
        pad=kwargs['pad']
        cmap=kwargs['cmap']
        contrast=kwargs['contrast']
        figsize=kwargs['figsize']
    else:
        textloc, fontsize, pad, cmap, contrast, figsize = (30,30), 20, 0, 'gray', 0.25, (8.27,11.69)

    return textloc, fontsize, pad, cmap, contrast, figsize


def plot(img,hdr,epic,rad,aperture,kwargs,show_centroid=True):
    '''
    rad: aperture radius in pixels
    '''
    #there were 240 pixels in 60 arcsec
    pix_size = 0.25 #arcsec/pix

    textloc, fontsize, pad, cmap, contrast, figsize = parse_kwargs(kwargs)

    assert img.shape[0] == img.shape[1] #square?

    interval = ZScaleInterval(contrast=contrast)
    zmin,zmax = interval.get_limits(img)

    fig, ax = pl.subplots()

    img, hdr = get_data(fname)
    filter = hdr['HIERARCH FPA.FILTER']
    band = filter.split('.')[0]

    ax.imshow(img, vmin=zmin, vmax=zmax)
    if aperture is not None:
        assert aperture.size == img.size
        ax.matshow(aperture, cmap=cmap, alpha=0.1, label='K2 aperture')
    else:
        rad = img.shape[0]*pix_size
        ax.set_title('EPIC{}'.format(epic),fontsize=20)

        x, y = img.shape[0]/2, img.shape[0]/2
        circ = pl.Circle((x,y), rad, linewidth=3, alpha=0.5, edgecolor='w')
        ax.add_artist(circ)
        #centroid
        if show_centroid:
            ax.text(x,y, '+', color='r', fontsize=fontsize)
    pl.show()
    fig.tight_layout()
    return fig


def plot_multi(file_list,epic,kwargs,aperture=None,show_centroid=True):
    textloc, fontsize, pad, cmap, contrast, figsize = parse_kwargs(kwargs)

    if figsize is not None:
        fig, ax = pl.subplots(1,len(file_list),figsize=figsize)
    else:
        fig, ax = pl.subplots(1,len(file_list))

    #there were 240 pixels in 60 arcsec
    pix_size = 0.25 #arcsec/pix

    d = sort_filternames(file_list)
    file_list = [d[i] for i in sorted(d)]

    for n,fname in enumerate(file_list):
        img, hdr = get_data(fname)
        filter = hdr['HIERARCH FPA.FILTER']
        band = filter.split('.')[0]

        assert img.shape[0] == img.shape[1] #square?

        interval = ZScaleInterval(contrast=contrast)
        zmin,zmax = interval.get_limits(img)

        ax[n].imshow(img,label='${}$'.format(band), cmap='gray', vmin=zmin, vmax=zmax)
        ax[n].yaxis.set_major_locator(pl.NullLocator())
        ax[n].xaxis.set_major_formatter(pl.NullFormatter())
        xpos,ypos=textloc
        ax[n].text(xpos,ypos,band,fontsize=fontsize,color='w')
        if aperture is not None:
            assert aperture.size == img.size
            ax[n].matshow(aperture, cmap=cmap, alpha=0.1, label='K2 aperture')
        else:
            rad = img.shape[0]*pix_size
            x, y = img.shape[0]/2, img.shape[0]/2
            #aperture
            circ = pl.Circle((x,y), rad, linewidth=2, alpha=0.4, edgecolor='w')
            ax[n].add_artist(circ)
            #centroid
            if show_centroid:
                ax[n].text(x,y, '+', color='r', fontsize=fontsize)
    ax[n//2].set_title('{}'.format(epic),fontsize=fontsize)#, pad=pad)
    pl.show()
    fig.tight_layout()
    return fig


def plot_epics(ids, kwargs=None):
    '''
    ids: epic ids
    '''
    #there were 240 pixels in 60 arcsec
    pix_size = 0.25 #arcsec/pix

    textloc, fontsize, pad, cmap, contrast, figsize = parse_kwargs(kwargs)

    rows = len(ids)
    cols = len(filters)

    if figsize is not None:
        fig, ax = pl.subplots(rows,cols,figsize=figsize)
    else:
        fig, ax = pl.subplots(rows,cols)

    for m,epic in enumerate(ids):
        foldername = str(epic)+'_'+str(filters)
        file_list=glob(foldername+'/*.fits')

        d = sort_filternames(file_list)
        file_list = [d[i] for i in sorted(d)]
        #print(file_list)

        interval = ZScaleInterval(contrast=contrast)
        for n,f in enumerate(file_list):
            #open fits file
            img,hdr = get_data(f)
            band = hdr['HIERARCH FPA.FILTER'].split('.')[0]
            #get limits
            zmin,zmax = interval.get_limits(img)

            ax[m,n].imshow(img,label='${}$'.format(band), cmap=cmap, vmin=zmin, vmax=zmax)
            ax[m,2].set_title('{}'.format(epic),fontsize=fontsize, pad=pad)
            ax[m,n].yaxis.set_major_locator(pl.NullLocator())
            ax[m,n].xaxis.set_major_formatter(pl.NullFormatter())
            xpos,ypos=textloc
            ax[m,n].text(xpos,ypos,band,fontsize=fontsize,color='w')
            rad = img.shape[0]/pix_size
            x, y = img.shape[0]/2, img.shape[0]/2
            circ = pl.Circle((x,y), rad, linewidth=2, alpha=0.4, edgecolor='w')
            ax[m,n].add_artist(circ)
    #fig.tight_layout()
    pl.show()
    return fig
