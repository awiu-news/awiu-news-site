export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const cookie = (request.headers.get('Cookie') || '').match(/oauth_state=([^;]+)/);
  let msg, status;
  if (!code || !cookie || cookie[1] !== state) { status = 'error'; msg = { message: 'invalid state' }; }
  else {
    const r = await fetch('https://github.com/login/oauth/access_token', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ client_id: env.GITHUB_CLIENT_ID, client_secret: env.GITHUB_CLIENT_SECRET, code }) });
    const d = await r.json();
    if (d.access_token) { status = 'success'; msg = { token: d.access_token, provider: 'github' }; } else { status = 'error'; msg = d; }
  }
  const body = `<!doctype html><script>(function(){function recv(e){window.opener.postMessage('authorization:github:${status}:'+JSON.stringify(${JSON.stringify(msg)}),e.origin);window.removeEventListener('message',recv,false);}window.addEventListener('message',recv,false);window.opener.postMessage('authorizing:github','*');})();</script>`;
  return new Response(body, { headers: { 'Content-Type': 'text/html;charset=UTF-8' } });
}
