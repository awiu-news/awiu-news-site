export async function onRequestGet({env}){
  if(!env.DB)return new Response('{"rows":[]}',{status:503});
  const r=await env.DB.prepare('SELECT id,n FROM views ORDER BY n DESC').all();
  return new Response(JSON.stringify({rows:r.results}),{headers:{'content-type':'application/json','cache-control':'no-store'}});
}
