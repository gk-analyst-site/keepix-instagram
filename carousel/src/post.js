// post.js — publish a 2-10 image carousel to Instagram via the Graph API.
// Flow: create child item containers -> wait FINISHED -> create CAROUSEL parent
// -> wait FINISHED -> media_publish. Transient errors (esp. code 9007) are retried.
const GV = process.env.GRAPH_API_VERSION || "v21.0";
const BASE = `https://graph.facebook.com/${GV}`;
const TOKEN = process.env.IG_ACCESS_TOKEN;
const IG = process.env.IG_USER_ID;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function requireEnv() {
  if (!TOKEN) throw new Error("IG_ACCESS_TOKEN is not set");
  if (!IG) throw new Error("IG_USER_ID is not set");
}

async function graph(method, pathPart, params, query) {
  let url = `${BASE}${pathPart}`;
  const opts = { method };
  if (method === "GET") {
    url += `?${new URLSearchParams({ ...query, access_token: TOKEN })}`;
  } else {
    opts.body = new URLSearchParams({ ...params, access_token: TOKEN });
  }
  let res, json;
  try {
    res = await fetch(url, opts);
    json = await res.json();
  } catch (e) {
    const err = new Error(`network: ${e.message}`);
    err.transient = true;
    throw err;
  }
  if (!res.ok || json.error) {
    const g = json.error || {};
    const err = new Error(g.message || `HTTP ${res.status}`);
    err.code = g.code;
    err.subcode = g.error_subcode;
    // 9007 = "Media ID is not available" (transient); 1/2/4/17/613 = transient/rate.
    err.transient = [9007, 1, 2, 4, 17, 613].includes(g.code);
    throw err;
  }
  return json;
}

async function withRetry(fn, label, { tries = 5, base = 3000 } = {}) {
  let last;
  for (let i = 1; i <= tries; i++) {
    try {
      return await fn();
    } catch (e) {
      last = e;
      if (i === tries || !e.transient) throw e;
      const wait = base * i;
      console.error(`  [retry ${label}] ${e.message} (code=${e.code ?? "-"}); wait ${wait}ms (${i}/${tries})`);
      await sleep(wait);
    }
  }
  throw last;
}

async function waitFinished(id, label, { tries = 30, interval = 4000 } = {}) {
  for (let i = 0; i < tries; i++) {
    const s = await withRetry(() => graph("GET", `/${id}`, null, { fields: "status_code" }), `${label}-status`);
    if (s.status_code === "FINISHED") return;
    if (s.status_code === "ERROR") throw new Error(`container ${id} reported ERROR`);
    await sleep(interval);
  }
  throw new Error(`container ${id} did not reach FINISHED in time`);
}

export async function postCarousel({ imageUrls, caption }) {
  requireEnv();
  if (imageUrls.length < 2 || imageUrls.length > 10) {
    throw new Error(`a carousel needs 2-10 images, got ${imageUrls.length}`);
  }
  const childIds = [];
  for (const url of imageUrls) {
    const r = await withRetry(
      () => graph("POST", `/${IG}/media`, { image_url: url, is_carousel_item: "true" }),
      "child",
    );
    childIds.push(r.id);
  }
  for (const id of childIds) await waitFinished(id, "child");

  const parent = await withRetry(
    () => graph("POST", `/${IG}/media`, { media_type: "CAROUSEL", children: childIds.join(","), caption }),
    "parent",
  );
  await waitFinished(parent.id, "parent");

  const pub = await withRetry(
    () => graph("POST", `/${IG}/media_publish`, { creation_id: parent.id }),
    "publish",
  );
  return pub.id;
}
