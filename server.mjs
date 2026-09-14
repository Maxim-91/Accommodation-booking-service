import http from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join } from "node:path";

const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8"
};

http.createServer(async (request, response) => {
  const url = request.url === "/" ? "/index.html" : request.url;
  const safePath = url.replace(/\.\./g, "");
  try {
    const body = await readFile(join(process.cwd(), safePath));
    response.writeHead(200, {
      "content-type": types[extname(safePath)] ?? "application/octet-stream"
    });
    response.end(body);
  } catch {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end("Not found");
  }
}).listen(Number(process.env.PORT ?? 8080));
