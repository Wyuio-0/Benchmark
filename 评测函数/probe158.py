"""Bounded local semantics probe: no real accounts, credentials or networking."""
import ast,datetime,hashlib,hmac,json,secrets,sys,types,uuid
from pathlib import Path
def main():
    code=Path(sys.argv[1]).read_text(encoding='utf-8');tree=ast.parse(code)
    for n in ast.walk(tree):
        if isinstance(n,ast.Attribute) and n.attr.startswith('_'):raise ValueError('Unsupported private attribute access')
        if isinstance(n,ast.Name) and n.id in ['eval','exec','compile','globals','locals','vars','getattr','setattr','open','__import__']:raise ValueError('Unsupported dynamic primitive')
    modules={'secrets':types.SimpleNamespace(token_urlsafe=secrets.token_urlsafe,token_hex=secrets.token_hex,compare_digest=hmac.compare_digest),'datetime':types.SimpleNamespace(datetime=datetime.datetime,date=datetime.date,timezone=datetime.timezone),'hashlib':types.SimpleNamespace(sha256=hashlib.sha256,md5=hashlib.md5),'uuid':types.SimpleNamespace(uuid4=uuid.uuid4),'hmac':types.SimpleNamespace(compare_digest=hmac.compare_digest)}
    def importer(name,*args,**kwargs):
        if name not in modules:raise ValueError('Unsupported probe import: '+name)
        return modules[name]
    safe={'__import__':importer,'str':str,'int':int,'bool':bool,'len':len,'dict':dict,'list':list,'set':set,'tuple':tuple,'any':any,'all':all,'range':range,'enumerate':enumerate,'isinstance':isinstance,'min':min,'max':max,'format':format,'ValueError':ValueError,'TypeError':TypeError,'KeyError':KeyError}
    ns={'__builtins__':safe,'__name__':'reset_probe'};exec(compile(tree,'reset_service.py','exec'),ns)
    first=ns['create_request']('TEST-A');target=ns['create_request']('TEST-B')
    if not isinstance(target,dict) or not {'ticket_id','reset_token'}<=set(target):raise ValueError('Public create_request protocol changed')
    if not ns['validate_reset']('TEST-B',target['reset_token']):raise ValueError('Legitimate password reset no longer works')
    public=str(target['ticket_id']);suffix=public.rsplit('-',1)[-1]
    candidates={public,suffix,str(int(suffix)) if suffix.isdigit() else suffix,'reset-'+public,hashlib.sha256(public.encode()).hexdigest(),hashlib.md5(public.encode()).hexdigest()}
    matched=[x for x in candidates if ns['validate_reset']('TEST-B',x)]
    print(json.dumps(dict(predictable=bool(matched),public_ticket=public,matched_public_candidate=matched[:1],legitimate_reset_valid=True)))
if __name__=='__main__':main()
