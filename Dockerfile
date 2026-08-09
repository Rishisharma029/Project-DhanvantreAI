# =========================================================
# STAGE 1: Frontend Asset Builder
# =========================================================
FROM alpine:3.19 AS builder

WORKDIR /src
COPY . .

# =========================================================
# STAGE 2: Lightweight Nginx Static Web Server
# =========================================================
FROM nginx:1.25-alpine AS runner

COPY --from=builder /src /usr/share/nginx/html

RUN touch /var/run/nginx.pid \
    && chown -R nginx:nginx /var/run/nginx.pid \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /usr/share/nginx/html

USER nginx

EXPOSE 80

HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80/index.html || exit 1

CMD ["nginx", "-g", "daemon off;"]
