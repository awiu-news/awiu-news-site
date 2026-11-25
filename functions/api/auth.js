export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const redirect = `${url.origin}/api/callback`;
  const state = crypto.randomUUID();
  const gh = `https://github.com/login/oauth/authorize?client_id=${env.GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(redirect)}&scope=repo,user&state=${state}`;
  return new Response(null, { status: 302, headers: { Location: gh, 'Set-Cookie': `oauth_state=${state}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600` } });
}
