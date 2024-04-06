USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like, Gecko) Chrome/46.0.2490.80 Safari/537.36'
CT_TEXT_HTML = 'text/html'
CT_FORM_URLE = 'application/x-www-form-urlencoded'
CT_JSON = 'application/json'

FORM_URLE_HEADERS = {
    'User-Agent': USER_AGENT,
    'Content-Type': CT_FORM_URLE
}

TEXT_HTML_HEADERS = {
    'User-Agent': USER_AGENT,
    'Content-Type': CT_TEXT_HTML
}

JSON_HEADERS = {
    'User-Agent': USER_AGENT,
    'Content-Type': CT_JSON
}