# panstarrs
Query multi-band (grizy) images of kepler/K2/TESS targets from PanSTARRS database.
`panstarrs` uses [`panstamps`](https://github.com/thespacedoctor/panstamps) in its core.

## Installation
Clone repo and install in a python 2 environment:
```shell
$ conda create new -s py2 python=2.7 && source activate py2
(py2) $ git clone https://github.com/jpdeleon/panstarrs
(py2) $ cd panstarrs
(py2) $ pip install .
```

## Usage

```shell
(py2) $ fetch_data --help

query PanSTARRS multi-band
                images of Kepler/K2/TESS targets using panstamps

positional arguments:
  epic                  EPIC ID of target star (e.g. 211319617)

optional arguments:
  -h, --help            show this help message and exit
  -r RAD, --rad RAD     aperture radius in arcmin (default=1)
  -f FIL, --fil FIL     panstarrs filters (default=grizy)
  -o OPT, --opt OPT     options (default=fJC; see 
                        https://github.com/thespacedoctor/panstamps)
  -s SHOWFIG, --showfig SHOWFIG
                        show downloaded images (True/False) using `panstarrs.inspect_data`
  -t TYPE, --type TYPE  image type (stack|warp)
```

To download grizy images of EPIC 201392505 as .fits and plot the result,
```shell
(py2) $ fetch_data 201392505 -r=1 -f=grizy -o=fJC -s=True -t=warp  
```
Note that the option "-o=fJC" follows the format of [`panstamps`](https://github.com/thespacedoctor/panstamps).
For comparison, the above script can be done using the following script using `panstamps`. 
However, the RA and DEC (instead of the EPIC id) must be specified instead.

```
(py2) $ panstamps -FJci --width=1 --filters=grizy stack 183.188556 -1.074821
```

To inspect the downloaded data,
```shell
(py2) $ inspect_data --help
usage: use "inspect_data --help" for more information

visualize downloaded panstarrs images

positional arguments:
  epic                  EPIC ID of target star (e.g. 211319617)
  folder                fname (.fits) or folder name

optional arguments:
  -h, --help            show this help message and exit
  -a APER, --aper APER  K2 aperture radius used in photometry
  -s, --save            save figure
  -f FMT, --fmt FMT     figure format (pdf|png)
  -cm CMAP, --cmap CMAP
                        color map (gray|viridis)
  -co CON, --con CON    contrast [0,1]
  -m, --mark            add cross mark to centroid
```

```shell
(py2) $ inspect_data 201392505 201392505_grizy
```

## To do: 
1. add custom K2 aperture used in photometry (currently using circular aperture)
2. fix bug in panstarrs.plot_epics
