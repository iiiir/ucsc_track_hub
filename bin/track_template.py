#!/bin/env python

def big_track():
    return '''
track %s
bigDataUrl %s
parent %s on
subGroups %s
shortLabel  %s
longLabel %s
type %s %s
visibility pack
'''

def group_track():
    return '''
track SJGROUP
compositeTrack on
subGroup1 subgroups SubGroups GROUP3=GROUP3 GROUP4=GROUP4 SHH=SHH UNKNOWN=UNKNOWN WNT=WNT
subGroup2 assay Assay H3K27Ac=H3K27Ac LHX2=LHX2 LMX1A=LMX1A HLX=HLX
dimensions dimX=subgroups dimY=assay
sortOrder subgroups=+ assay=+
type bigWig
shortLabel Read count
longLabel H3K27Ac and TF ChIP-Seq read count for each medulloblastoma sample
visibility dense
'''

def assay_track():
    return '''
track SJSE
compositeTrack on
subGroup1 subgroups SubGroups GROUP3_SE=GROUP3 GROUP4_SE=GROUP4 GROUP3_GROUP4_SE=GROUP3_GROUP4 SHH_SE=SHH WNT_SE=WNT SHH_WNT_SE=SHH_WNT CONSERVED_SE=CONSERVED
dimensions dimX=subgroups
sortOrder subgroups=+
type bigBed
shortLabel Super enhancer
longLabel Super enhancer called from each medulloblastoma subgroup
visibility dense
'''

def ucsc_txt():
    return '''\
hub SJEPD
shortLabel MB super enhancer
longLabel Subgroup-specific regulatory landscape of medulloblastoma
genomesFile genomes.txt
email shuoguo.wang@stjude.org
descriptionUrl https://www.stjude.org
'''

def genomes_txt():
    return '''\
genome hg19
trackDb hg19/trackDb.txt
'''