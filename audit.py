"""Audit a supplied resource inventory without cloud credentials or API access."""
import argparse
import json
from pathlib import Path
import sys


def audit(config):
    required=config['required_tags'];allowed=config.get('allowed_values',{});resources=config['resources']
    if not isinstance(required,list) or any(not isinstance(k,str) or not k for k in required) or len(set(required))!=len(required):
        raise ValueError('required_tags must be unique nonempty strings')
    if not isinstance(allowed,dict) or any(not isinstance(v,list) or not v or any(not isinstance(x,str) for x in v) for v in allowed.values()):
        raise ValueError('allowed_values must map tag names to nonempty string lists')
    findings=[];ids=set();compliant=0
    for resource in resources:
        identifier=resource['id'];tags=resource['tags']
        if not isinstance(identifier,str) or not identifier or identifier in ids: raise ValueError('resource ids must be unique nonempty strings')
        ids.add(identifier)
        if not isinstance(tags,dict) or any(not isinstance(v,str) for v in tags.values()): raise ValueError('tags must map strings to strings')
        issues=[]
        for key in required:
            if not tags.get(key,'').strip(): issues.append({'tag':key,'reason':'missing_or_blank'})
        for key,choices in sorted(allowed.items()):
            if key in tags and tags[key].strip() and tags[key] not in choices: issues.append({'tag':key,'reason':'invalid_value'})
        if issues: findings.append({'resource':identifier,'issues':issues})
        else: compliant+=1
    return {'resources':len(resources),'compliant':compliant,'compliance_ratio':compliant/len(resources) if resources else None,
            'findings':sorted(findings,key=lambda f:f['resource'])}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('inventory');a=p.parse_args()
    try: result=audit(json.loads(Path(a.inventory).read_text()))
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as e:
        print(json.dumps({'error':str(e)}),file=sys.stderr);return 2
    print(json.dumps(result,indent=2));return int(bool(result['findings']))

if __name__=='__main__': sys.exit(main())
