#!/bin/env python
import os
import argparse
import gzip
import collections
import sys
import track_template

p = argparse.ArgumentParser('generate_trackDb.py --path tracks --composite --table hub_table.csv')
p.add_argument('--bigfiles',nargs="+", help="big wig and big bed")
p.add_argument('--composite',action='store_true', help="big wig and big bed")
p.add_argument('--table',help="tabel file defines tracks and subgroups")
p.add_argument('--path', help="path for all big files, must in same folder")
args=p.parse_args()

def read_table(fn):
    f = open(fn)
    header=next(f).rstrip().split(',')
    hub = collections.namedtuple('Hub', header)
    hdict = {}
    for l in f:
        lis = l.rstrip('\n').split(',')
        hdict[lis[0]] = hub(*lis)
    return hdict

def find_type(f):
    return 'bigWig' if f.endswith('.bw') else 'bigBed'

def find_parent(track_info):
    type_s = track_info.subGroup
    f      = track_info.Track
    if f.endswith('.bb'):
        track_s = 'SJSE'
        sgline  = 'subgroups=%s' % type_s
    else:
        assay_s = track_info.Assay
        track_s = 'SJGROUP'
        sgline  = 'subgroups=%s assay=%s' % (type_s, assay_s) 
    return track_s, sgline

def trackDb_block(track_info):
    trackname  = track_info.Track
    bigDataUrl = os.path.join(args.path,trackname)
    shortLabel = track_info.shortLabel
    longlable  = track_info.longLabel
    type_s     = find_type(trackname)
    coords     = "6" if type_s=='bigBed' else "0 50"
    mom,subg   = find_parent(track_info)
    tracktxt   = track_template.big_track() % (trackname, bigDataUrl, mom, subg, shortLabel, longlable, type_s, coords)
    return tracktxt

def print_trackDb(args, f):
    if args.composite:
        print >>f, track_template.group_track()
        print >>f, track_template.assay_track()
    hdict = read_table(args.table)
    all_tracks=sorted(hdict.keys())
    bw  = [track for track in all_tracks if track.endswith('.bw')]
    bed = [track for track in all_tracks if not track.endswith('.bw')]
    for track in bw+bed:
        trackDb_txt = trackDb_block(hdict[track])
        print >>f, trackDb_txt

def print_wig_headers(args):
    for f in args.bigfiles:
        if f.endswith('.gz'):
            header = next(gzip.open(f,'rb'))
        else:
            header = next(open(f))
        print >>sys.stdout, header.rstrip('\n')

def main(args):
    if not os.path.exists('ucsc_hub/hg19/tracks'):
        os.makedirs('ucsc_hub/hg19/tracks')
    # write ucsc.txt
    print >>open('ucsc_hub/UCSC.txt','w'), track_template.ucsc_txt()
    # write genomes.txt
    print >>open('ucsc_hub/genomes.txt','w'), track_template.genomes_txt()
    # write hg19/trackDb.txt
    f = open('ucsc_hub/hg19/trackDb.txt','w')
    print_trackDb(args, f)
    # all tracks
    print >> sys.stderr, ">>> copy all tracks under %s" % os.path.abspath('ucsc_hub/hg19/tracks')
    
if __name__ == '__main__':
    main(args)
