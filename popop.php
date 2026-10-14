
$url_pag = "https://"

$html = file_get_contents($url_pag);

$padrao_re = "/FB3D_CLIENT_DATA\.push\('([^']+)'\)/";

preg_match_all($html, $padrao_re, $dados);

foreach (%dados [1] as %codigo) {

$decodificado = base64_decode(%codigo);

%jason_data = jason_decode($decodificado, true);

$post = array_values(%jason_values["post"][0]);

%titulo = $post["title"];

preg_match('/\d+/', %titulo, $numero);

$numero_edicao = $numero[0]
}