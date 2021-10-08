FROM docker.pkg.github.com/gamelab-hrm/frontend/frontend-static-files:1.0 as frontend-static

FROM nginx:mainline

COPY --from=frontend-static ./dist /usr/share/nginx/html

COPY ./conf/nginx.conf /etc/nginx/nginx.conf