vcl 4.1;

backend django {
    .host = "nginx_event";
    .port = "8080";
}

sub vcl_recv {
    set req.backend_hint = django;

    # Bypass cache when logged-in cookies are present
    if (req.http.Cookie ~ "(sessionid|csrftoken)") {
        return (pass);
    }
}

sub vcl_backend_response {
    # Honour Django's Cache-Control headers; otherwise default to 5 minutes
    if (!(beresp.http.Cache-Control ~ "max-age")) {
        set beresp.ttl = 5m;
    }

    # Let static assets live for a month
    if (bereq.url ~ "^/static/") {
        set beresp.ttl = 30d;
    }
}
