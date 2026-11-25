const BOT=/bot|crawl|spider|slurp|bing|facebookexternalhit|whatsapp|telegram|preview|headless|python|curl|wget|monitor|lighthouse/i;
const J=(o,s=200)=>new Response(JSON.stringify(o),{status:s,headers:{'content-type':'application/json','cache-control':'no-store'}});
async function valid(env,request,id){
  if(!/^[a-z0-9-]{1,80}$/.test(id))return false;
  const r=await env.ASSETS.fetch(new URL('/news/'+id+'/',request.url));
  return r.status===200;
}
export async function onRequest({request,env}){
  const url=new URL(request.url);const id=url.searchParams.get('id')||'';
  if(!env.DB)return J({n:0,error:'no-db'},503);
  if(!(await valid(env,request,id)))return J({error:'bad-id'},400);
  if(request.method==='POST'){
    const ua=request.headers.get('user-agent')||'';
    const same=request.headers.get('sec-fetch-site');
    if(!BOT.test(ua)&&ua&&(!same||same==='same-origin')){
      await env.DB.prepare('INSERT INTO views(id,n) VALUES(?,1) ON CONFLICT(id) DO UPDATE SET n=n+1').bind(id).run();
    }
  }
  const row=await env.DB.prepare('SELECT n FROM views WHERE id=?').bind(id).first();
  return J({n:row?row.n:0});
}
